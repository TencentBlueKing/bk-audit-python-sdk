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
from unittest import TestCase
from unittest.mock import Mock, patch

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LogData, LogRecord
from opentelemetry.sdk.util.instrumentation import InstrumentationScope

from bk_audit.constants.contrib import OTVersion
from bk_audit.contrib.opentelemetry.exporters import OTLogExporter
from bk_audit.contrib.opentelemetry.processor import LazyBatchLogProcessor
from bk_audit.contrib.opentelemetry.setup import setup
from bk_audit.contrib.opentelemetry.utils import (
    BaseServiceNameHandler,
    ServiceNameHandler,
)
from tests.base.client import init_client
from tests.base.constants import CONTEXT, SERVICE_NAME, VIEW_FILE


class TestOT(TestCase):
    """测试Client"""

    def setUp(self):
        """初始化 Client"""
        self.client = init_client([OTLogExporter()])

    def test_ot_export(self):
        """测试OT导出"""
        setup(self.client)
        self.client.add_event(action=VIEW_FILE, audit_context=CONTEXT)

    def test_json_decode_error(self):
        """测试JSON转换失败"""
        result_content = object()
        self.client.add_event(action=VIEW_FILE, audit_context=CONTEXT, result_content={"content": result_content})

    def test_setup(self):
        """测试OT初始化"""
        setup(self.client)

    @patch("bk_audit.contrib.opentelemetry.setup.OT_VERSION", OTVersion.v1_7_1)
    def test_setup_1_7_1(self):
        """测试OT初始化(v1.7.1)"""
        with self.assertRaises(ImportError):
            setup(self.client)

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

    def test_processor_shutdown(self):
        """测试停止进程"""
        exporter = OTLPLogExporter(endpoint=os.getenv("BKAPP_OTEL_LOG_ENDPOINT"))
        # shutdown normally
        processor = LazyBatchLogProcessor(exporter)
        processor.force_flush()
        processor.shutdown()
        # shutdown with work thread
        processor = LazyBatchLogProcessor(exporter)
        processor.emit(LogData(LogRecord(), InstrumentationScope(self.client._bk_app_code)))
        processor.force_flush()
        processor.shutdown()
