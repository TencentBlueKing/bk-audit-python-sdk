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
from dataclasses import dataclass, field
from typing import List

from django.conf import settings as django_settings
from django.utils.module_loading import import_string

from bk_audit.constants.contrib import DJANGO_SETTING_NAME
from bk_audit.constants.log import DEFAULT_QUEUE_LIMIT


@dataclass
class BKAuditSetting:
    """
    审计 SDK 配置
    """

    log_queue_limit: int = DEFAULT_QUEUE_LIMIT
    formatter: str = "bk_audit.log.formatters.Formatter"
    exporters: List[str] = field(
        default_factory=lambda: ["bk_audit.contrib.opentelemetry.exporters.OTLogExporter"]
        if os.getenv("BKAPP_OTEL_LOG_ENDPOINT")
        else ["bk_audit.log.exporters.LoggerExporter"]
    )
    service_name_handler: str = "bk_audit.contrib.opentelemetry.utils.ServiceNameHandler"
    ot_endpoint: str = ""
    bk_data_id: str = ""
    bk_data_token: str = ""

    def __post_init__(self):
        self.formatter = import_string(self.formatter)()
        self.exporters = [import_string(exporter)() for exporter in self.exporters]
        self.service_name_handler = import_string(self.service_name_handler)

    def get_app_code(self) -> str:
        return django_settings.APP_CODE

    def get_app_secret(self) -> str:
        return django_settings.SECRET_KEY


bk_audit_settings = BKAuditSetting(**getattr(django_settings, DJANGO_SETTING_NAME, {}))
