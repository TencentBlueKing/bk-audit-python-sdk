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

from django.apps import AppConfig
from django.utils.translation import gettext_lazy

from bk_audit.contrib.bk_audit.settings import bk_audit_settings


class AuditConfig(AppConfig):
    name = "bk_audit.contrib.bk_audit"
    verbose_name = gettext_lazy("BK Audit")

    def ready(self):
        if not bk_audit_settings.ot_endpoint and not os.getenv("BKAPP_OTEL_LOG_ENDPOINT"):
            return

        from bk_audit.contrib.bk_audit.client import bk_audit_client
        from bk_audit.contrib.opentelemetry.setup import setup

        setup(
            bk_audit_client,
            bk_data_id=bk_audit_settings.bk_data_id,
            bk_data_token=bk_audit_settings.bk_data_token,
            endpoint=bk_audit_settings.ot_endpoint,
        )
