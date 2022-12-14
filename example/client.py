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

from bk_audit.client import BkAudit
from example.exporters import ConsoleExporter
from example.formatters import UserFormatter

app_code = os.getenv("BKAPP_APP_ID")
app_secret = os.getenv("BKAPP_APP_SECRET")
bk_audit_client = BkAudit(bk_app_code=app_code, bk_app_secret=app_secret)
bk_audit_client.add_exporter(ConsoleExporter())
bk_audit_client.set_formatter(UserFormatter())
