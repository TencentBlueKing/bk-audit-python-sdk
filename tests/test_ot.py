# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云 - 审计中心 (BlueKing - Audit Center) available.
Copyright (C) 2022 THL A29 Limited,
a Tencent company. All rights reserved.
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the
specific language governing permissions and limitations under the License.
We undertake not to change the open source license (MIT license) applicable
to the current version of the project delivered to anyone in the future.
"""

import logging
import multiprocessing
import os
import warnings
from unittest import TestCase
from unittest.mock import Mock, patch

from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    LogRecordExporter,
    LogRecordExportResult,
)

from bk_audit.constants.utils import OT_LOGGER_NAME
from bk_audit.contrib.opentelemetry.exporters import OTLogExporter
from bk_audit.contrib.opentelemetry.processor import LazyBatchLogProcessor
from bk_audit.contrib.opentelemetry.setup import setup
from bk_audit.contrib.opentelemetry.utils import (
    BaseServiceNameHandler,
    ServiceNameHandler,
)
from tests.base.client import init_client
from tests.base.constants import CONTEXT, SERVICE_NAME, VIEW_FILE

TEST_EVENT_CONTENT = "test-event-content"


def _noop_target():
    """模块级空函数，供 fork 测试用作子进程入口（forkserver/spawn 模式要求可 pickle）"""
    pass


class InMemoryLogExporter(LogRecordExporter):
    """内存 exporter：记录收到的批次，替代真实 OTLPLogExporter"""

    def __init__(self):
        self.records = []  # List[ReadableLogRecord]
        self.shutdown_called = False

    def export(self, batch):
        self.records.extend(batch)
        return LogRecordExportResult.SUCCESS

    def shutdown(self):
        self.shutdown_called = True


class TestOT(TestCase):
    """测试OT集成"""

    def setUp(self):
        """初始化 Client"""
        self.client = init_client([OTLogExporter()])
        self.memory_exporter = InMemoryLogExporter()

    def tearDown(self):
        """清理 Logger 避免影响其他的单元测试"""
        logging.getLogger(OT_LOGGER_NAME).handlers = []

    def _setup(self, client, env=None, **kwargs):
        """以内存 exporter 替换真实 OTLPLogExporter 执行 setup，返回 LoggerProvider"""
        with patch.dict(os.environ, env or {}, clear=False), patch(
            "bk_audit.contrib.opentelemetry.setup.OTLPLogExporter",
            return_value=self.memory_exporter,
        ):
            return setup(client, **kwargs)

    def test_setup(self):
        """测试OT初始化"""
        provider = self._setup(self.client)
        self.assertIsInstance(provider, LoggerProvider)
        self.assertTrue(logging.getLogger(OT_LOGGER_NAME).handlers)

    def test_ot_export_batch(self):
        """测试OT导出（默认批量模式）"""
        provider = self._setup(self.client)
        self.client.add_event(action=VIEW_FILE, audit_context=CONTEXT, event_content=TEST_EVENT_CONTENT)
        provider.force_flush()
        self.assertEqual(len(self.memory_exporter.records), 1)
        record = self.memory_exporter.records[0]
        self.assertEqual(record.log_record.body, TEST_EVENT_CONTENT)
        self.assertEqual(record.log_record.attributes["action_id"], VIEW_FILE.id)
        self.assertEqual(record.log_record.attributes["username"], CONTEXT.username)

    def test_ot_export_simple(self):
        """测试OT导出（同步直报模式）"""
        self._setup(self.client, env={"BKAPP_USE_SIMPLE_LOG_PROCESSOR": "1"})
        self.client.add_event(action=VIEW_FILE, audit_context=CONTEXT, event_content=TEST_EVENT_CONTENT)
        # 同步模式无需 force_flush 即已上报
        self.assertEqual(len(self.memory_exporter.records), 1)
        self.assertEqual(self.memory_exporter.records[0].log_record.body, TEST_EVENT_CONTENT)

    def test_resource_fields(self):
        """测试资源字段"""
        provider = self._setup(self.client)
        self.client.add_event(action=VIEW_FILE, audit_context=CONTEXT, event_content=TEST_EVENT_CONTENT)
        provider.force_flush()
        self.assertEqual(len(self.memory_exporter.records), 1)
        attributes = self.memory_exporter.records[0].resource.attributes
        self.assertIn("service.name", attributes)
        self.assertIn("bk_data_id", attributes)
        self.assertIn("bk.data.token", attributes)

    def test_lazy_processor_is_standard(self):
        """测试 LazyBatchLogProcessor 行为等价标准 BatchLogRecordProcessor"""
        self.assertTrue(issubclass(LazyBatchLogProcessor, BatchLogRecordProcessor))
        processor = LazyBatchLogProcessor(self.memory_exporter)
        # 仅此一处读私有成员做存在性断言：实例化即持有共享批量处理器
        self.assertTrue(hasattr(processor, "_batch_processor"))
        processor.shutdown()

    def test_processor_shutdown(self):
        """测试 force_flush/shutdown 及重复 shutdown 幂等"""
        processor = LazyBatchLogProcessor(self.memory_exporter)
        processor.force_flush()
        processor.shutdown()
        self.assertTrue(self.memory_exporter.shutdown_called)
        # 重复 shutdown 不应抛异常
        processor.shutdown()

    def test_no_deprecation_warning(self):
        """测试 setup 全程无 DeprecationWarning 透出"""
        with warnings.catch_warnings(record=True) as records:
            warnings.simplefilter("always")
            self._setup(self.client)
        deprecation_warnings = [r for r in records if issubclass(r.category, DeprecationWarning)]
        self.assertEqual(deprecation_warnings, [])

    # ---- fork 场景验证组 ----
    # LazyBatchLogProcessor 最初就是为解决 fork 后 worker 线程失效引入，
    # OTel 1.34+ 内建 fork 安全（os.register_at_fork + PID 检测）后行为应等价。
    # 以下 3 个测试覆盖该核心场景，验证改造未退化。

    @staticmethod
    def _fork_child_emit_and_flush(client, provider, memory_exporter, shared_list):
        """子进程入口：fork 后 emit 一条并强制 flush

        子进程通过 fork 继承父进程的 LoggerProvider，但 OTel 内部的
        daemon worker 线程在 fork 后必须重建（os.register_at_fork）才能正常 flush。
        memory_exporter 是父进程对象的 fork 副本，子进程 worker flush 后写入的是子进程的副本。
        """
        try:
            client.add_event(
                action=VIEW_FILE,
                audit_context=CONTEXT,
                event_content="fork-child-event",
            )
            # 触发子进程的 worker 线程 flush，超时 5s
            provider.force_flush(timeout_millis=5000)
            # 子进程的 memory_exporter 是父进程对象的 fork 副本，独立 append
            # 长度必须是 1（仅子进程 emit 的这一条），证明 fork 后 worker 正常工作
            shared_list.append(len(memory_exporter.records))
        except Exception as e:  # noqa: BLE001 - 子进程异常必须透出
            shared_list.append("error: %s" % e)

    def test_fork_child_can_emit_and_flush(self):
        """验证 fork 后子进程能正常 emit + flush（核心场景）

        改造前：LazyBatchLogProcessor 通过懒启动 + _at_fork_reinit 实现 fork 安全
        改造后：依赖 OTel 1.43 内建 os.register_at_fork + emit PID 检测
        本测试断言两者外部可观测行为一致 —— 子进程能 flush 出日志。
        """
        if not hasattr(os, "fork"):
            self.skipTest("platform does not support fork (Windows 走 spawn，无需此验证)")

        # Py3.14 Linux 默认 start method 改为 forkserver，会 pickle args；
        # 但 LoggerProvider 含 _thread.RLock 不可 pickle。
        # 本测试验证 fork 语义，显式用 fork context（子进程继承内存，无需 pickle）。
        ctx = multiprocessing.get_context("fork")

        # 用 Manager 共享 list 跨进程收集结果
        manager = multiprocessing.Manager()
        shared_list = manager.list()

        # 父进程完成 setup（**不要 emit**，避免子进程 exporter 继承到脏数据）
        provider = self._setup(self.client)

        p = ctx.Process(
            target=self._fork_child_emit_and_flush,
            args=(self.client, provider, self.memory_exporter, shared_list),
        )
        p.start()
        p.join(timeout=15)

        self.assertEqual(p.exitcode, 0, "子进程必须正常退出")
        self.assertEqual(len(shared_list), 1, "子进程必须上报结果")
        result = shared_list[0]
        self.assertEqual(
            result, 1,
            "子进程 force_flush 后必须收到 1 条日志（fork 安全未退化），实际: %r" % result,
        )

    def test_fork_parent_still_works_after_fork(self):
        """验证 fork 后父进程仍能正常上报（不应被影响）"""
        if not hasattr(os, "fork"):
            self.skipTest("platform does not support fork")

        # Py3.14 Linux 默认 forkserver 会 pickle target；显式用 fork context
        ctx = multiprocessing.get_context("fork")

        provider = self._setup(self.client)

        p = ctx.Process(target=_noop_target)
        p.start()
        p.join(timeout=5)
        self.assertEqual(p.exitcode, 0)

        # fork 之后父进程继续 emit 应正常（父进程 worker 线程不受影响）
        self.client.add_event(
            action=VIEW_FILE,
            audit_context=CONTEXT,
            event_content="post-fork-parent-event",
        )
        provider.force_flush(timeout_millis=5000)
        self.assertEqual(len(self.memory_exporter.records), 1)

    def test_lazy_processor_pid_detection_mechanism_present(self):
        """验证改造后 LazyBatchLogProcessor 走的是 OTel 1.43 的 PID 检测路径

        不直接读 OTel 私有成员（避免测试本身依赖私有 API），
        而是验证共享基类 BatchProcessor 的关键属性存在：
        _batch_processor（OTel 1.34+ 共享基类引入）/ _pid（PID 检测标记）。
        """
        processor = LazyBatchLogProcessor(self.memory_exporter)
        # 1. 持有 OTel 1.34+ 引入的共享 BatchProcessor 实例
        self.assertTrue(hasattr(processor, "_batch_processor"))
        # 2. 共享基类有 _pid 字段（PID 检测的标记，emit 会比对 os.getpid()）
        self.assertTrue(hasattr(processor._batch_processor, "_pid"))
        # 3. _pid 当前等于本进程 PID
        self.assertEqual(processor._batch_processor._pid, os.getpid())
        processor.shutdown()

    def test_json_decode_error(self):
        """测试JSON转换失败"""
        result_content = object()
        self.client.add_event(action=VIEW_FILE, audit_context=CONTEXT, result_content={"content": result_content})

    def test_service_name(self):
        """测试基类"""
        self.assertEqual(BaseServiceNameHandler(str()).get_service_name(), None)

    @patch("bk_audit.contrib.opentelemetry.utils.ServiceNameHandler.is_celery_beat", Mock(return_value=True))
    def test_service_name_beat(self):
        """测试服务名处理Beat"""
        self.assertEqual(ServiceNameHandler(SERVICE_NAME).get_service_name(), "%s_celery_beat" % SERVICE_NAME)

    @patch("bk_audit.contrib.opentelemetry.utils.ServiceNameHandler.is_celery", Mock(return_value=True))
    def test_service_name_worker(self):
        """测试服务名处理Worker"""
        self.assertEqual(ServiceNameHandler(SERVICE_NAME).get_service_name(), "%s_celery_worker" % SERVICE_NAME)
