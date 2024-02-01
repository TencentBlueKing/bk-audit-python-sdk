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
import uuid
from unittest import TestCase

from django.conf import settings
from django.core.mail.backends.locmem import EmailBackend
from django.test import override_settings

from bk_audit.constants.contrib import LoggingDefaultConfig
from bk_audit.constants.utils import LOGGER_NAME, OT_LOGGER_NAME
from bk_audit.contrib.django.formatters import DjangoFormatter
from bk_audit.contrib.django.loggers import LoggingConfigHandler
from bk_audit.log.models import AuditContext
from tests.base.client import init_client
from tests.base.constants import APP_CODE, REQUEST_IP, VIEW_FILE
from tests.base.models import Request


class TestDjango(TestCase):
    """测试Django集成"""

    def setUp(self):
        """初始化 Client"""
        self.client = init_client()
        self.client.set_formatter(DjangoFormatter())
        EmailBackend()

    def test_add_event(self):
        """测试添加事件"""
        # 常规事件
        request = Request()
        context = AuditContext(request=request)
        self.client.add_event(action=VIEW_FILE, audit_context=context)
        # APIGW事件
        setattr(request, "app", object())
        self.client.add_event(action=VIEW_FILE, audit_context=context)

    def test_meta_ip(self):
        """测试META IP"""
        # 常规Request
        request = Request()
        request.META = {}
        self.client.add_event(action=VIEW_FILE, audit_context=AuditContext(request=request))
        # HTTP_X_REAL_IP
        request.META = {"HTTP_X_REAL_IP": REQUEST_IP}
        self.client.add_event(action=VIEW_FILE, audit_context=AuditContext(request=request))
        # HTTP_X_FORWARDED_FOR
        request.META = {"HTTP_X_FORWARDED_FOR": REQUEST_IP}
        self.client.add_event(action=VIEW_FILE, audit_context=AuditContext(request=request))

    def test_logging(self):
        """测试LOGGING"""
        file_name = "test.log"
        logging_config = LoggingConfigHandler(file_name).set_logging({"handlers": {}, "formatters": {}, "loggers": {}})
        self.assertEqual(
            logging_config,
            {
                "handlers": {
                    "bk_audit": {
                        "class": LoggingDefaultConfig.HANDLER_CLS,
                        "formatter": LOGGER_NAME,
                        "filename": file_name,
                        "maxBytes": LoggingDefaultConfig.FILE_MAX_BYTES,
                        "backupCount": LoggingDefaultConfig.FILE_BACKUP_COUNT,
                    }
                },
                "formatters": {LOGGER_NAME: {"format": "%(message)s"}},
                "loggers": {LOGGER_NAME: {"handlers": [LOGGER_NAME], "level": logging.INFO, "propagate": True}},
            },
        )

    def test_auto_instrument(self):
        """测试自动注入"""

        settings.configure(
            APP_CODE=APP_CODE, SECRET_KEY=uuid.uuid1().hex, BK_AUDIT_SETTINGS={"ot_endpoint": "http://127.0.0.1"}
        )

        from bk_audit.contrib.bk_audit.apps import AuditConfig

        app_config = AuditConfig.create("bk_audit.contrib.bk_audit")
        app_config.ready()

        # 清理 Logger 避免影响其他的单元测试
        logging.getLogger(OT_LOGGER_NAME).handlers = []

    @override_settings()
    def test_auto_instrument_ot(self):
        """测试OT注入"""

        from bk_audit.contrib.bk_audit.settings import bk_audit_settings

        bk_audit_settings.ot_endpoint = ""

        from bk_audit.contrib.bk_audit.apps import AuditConfig

        app_config = AuditConfig.create("bk_audit.contrib.bk_audit")
        app_config.ready()

        # 清理 Logger 避免影响其他的单元测试
        logging.getLogger(OT_LOGGER_NAME).handlers = []

    @override_settings()
    def test_resource(self):
        """测试调用Resource"""

        # 初始化
        from bk_audit.contrib.bk_audit.apps import AuditConfig

        app_config = AuditConfig.create("bk_audit.contrib.bk_audit")
        app_config.ready()

        # 更新格式化器
        from bk_audit.contrib.bk_audit.client import bk_audit_client

        bk_audit_client.set_formatter(DjangoFormatter())

        # 测试正常、异常、标准异常、未实现三种状态

        from tests.base.resources import (
            BlueErrorResource,
            ErrorResource,
            NoAuditResource,
            Resource,
        )

        NoAuditResource().request()
        Resource().request()
        with self.assertRaises(Exception):
            ErrorResource().request()
        with self.assertRaises(Exception):
            BlueErrorResource().request()
