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
from unittest import TestCase

from bk_audit.constants.contrib import LoggingDefaultConfig
from bk_audit.constants.utils import LOGGER_NAME
from bk_audit.contrib.django.formatters import DjangoFormatter
from bk_audit.contrib.django.loggers import LoggingConfigHandler
from bk_audit.log.models import AuditContext
from tests.base.client import init_client
from tests.base.constants import REQUEST_IP, VIEW_FILE
from tests.base.models import Request


class TestDjango(TestCase):
    """测试Django集成"""

    def setUp(self):
        """初始化 Client"""
        self.client = init_client()
        self.client.set_formatter(DjangoFormatter())

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
