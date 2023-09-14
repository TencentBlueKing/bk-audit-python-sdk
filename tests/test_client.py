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

import os
import uuid
from unittest import TestCase

from bk_audit.log.base import BkAuditLog
from bk_audit.log.exporters import BaseExporter, LoggerExporter
from bk_audit.log.formatters import BaseFormatter, Formatter
from bk_audit.log.models import AuditContext, AuditEvent
from tests.base.client import app_code, app_secret, init_client
from tests.base.constants import CONTEXT, HOST, HOST_INSTANCE, VIEW_FILE
from tests.base.exporters import DelayExporter


class TestClient(TestCase):
    """测试Client"""

    def setUp(self):
        """初始化 Client"""
        self.client = init_client()

    def test_add_event(self):
        """测试新增审计事件"""
        self.client.add_event(action=VIEW_FILE, audit_context=CONTEXT)
        self.client.export_events()
        with self.assertRaises(AssertionError):
            self.client.add_event(action=VIEW_FILE)

    def test_set_formatter(self):
        """测试设置事件处理器"""
        # 设置处理器
        formatter = BaseFormatter()
        self.client.set_formatter(formatter)
        # 判断处理器设置成功
        self.assertEqual(self.client._log._formatter, formatter)
        # 设置处理器
        formatter = Formatter()
        self.client.set_formatter(formatter)
        # 判断处理器设置成功
        self.assertEqual(self.client._log._formatter, formatter)

    def test_add_exporter(self):
        """测试添加事件输出"""
        # 添加输出
        self.client.add_exporter(LoggerExporter())
        self.client.add_exporter(DelayExporter())
        self.assertEqual(len(self.client._log._exporter_class), 4)

    def test_set_queue_limit(self):
        """测试设置队列长度"""
        # 清空队列
        self.client._log._queue.clear()
        # 添加数据
        self.client.add_event(action=VIEW_FILE, audit_context=CONTEXT)
        self.client.add_event(action=VIEW_FILE, audit_context=CONTEXT)
        # 判断队列长度
        self.assertEqual(len(self.client._log._queue._storage), 2)
        # 设置最大长度为 1
        self.client.set_queue_limit(1)
        # 判断队列长度
        self.assertEqual(len(self.client._log._queue._storage), 1)

    def test_set_log(self):
        """测试设置日志类"""
        self.client.set_log(BkAuditLog(app_code, app_secret))

    def test_bulk_add(self):
        """测试批量添加"""
        self.client = init_client()
        event = AuditEvent()
        self.client._log._queue.bulk_add([event])
        self.assertEqual(len(self.client._log._queue._storage), 1)

    def test_base_formatter(self):
        """测试基础事件处理"""
        formatter = BaseFormatter()
        formatter.build_event(
            action=VIEW_FILE,
            resource_type=HOST,
            audit_context=AuditContext(),
            instance=HOST_INSTANCE,
            event_id=uuid.uuid1().hex,
            event_content=str(),
            start_time=int(),
            end_time=int(),
            result_code=int(),
            result_content=str(),
            extend_data=dict(),
        )

    def test_base_exporter(self):
        """测试基础导出"""
        exporter = BaseExporter()
        exporter.export([])
        self.assertEqual(exporter.is_delay, None)

    def test_model_str(self):
        """测试ModelStr"""
        event_id = uuid.uuid1().hex
        self.assertEqual(str(AuditEvent(event_id=event_id)), event_id)

    def test_setup_simple(self):
        """测试生成同步上报"""
        os.environ["BKAPP_USE_SIMPLE_LOG_PROCESSOR"] = "True"
        client = init_client()
        client.add_event(action=VIEW_FILE, audit_context=CONTEXT)
