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
from bk_audit.contrib.opentelemetry.exporters import OTLogExporter
from bk_audit.contrib.opentelemetry.setup import setup
from bk_audit.contrib.opentelemetry.utils import ServiceNameHandler
from bk_audit.log.formatters import Formatter
from bk_audit.log.models import AuditContext
from example.models import Host, HostInstance, HostResourceType, ViewFileAction


def report_audit_log():
    """
    通过 OT 上报审计日志
    """

    """
    Start 初始化步骤，全局只需要初始化一次
    """

    # BKAPP_USE_SIMPLE_LOG_PROCESSOR 为 True 时会阻塞当前进程，直到上报成功
    # 若脚本运行后就会退出需要添加此环境变量，否则可以不需要此环境变量
    os.environ["BKAPP_USE_SIMPLE_LOG_PROCESSOR"] = "True"

    # 初始化 Client
    bk_audit_client = BkAudit(
        bk_app_code=os.getenv("BKAPP_APP_CODE", ""),
        bk_app_secret=os.getenv("BKAPP_APP_SECRET", ""),
        settings={
            "formatter": Formatter(),
            "exporters": [OTLogExporter()],
            "service_name_handler": ServiceNameHandler,
        },
    )

    # 初始化 OT 上报
    setup(
        client=bk_audit_client,
        endpoint=os.getenv("BKAPP_OTEL_LOG_ENDPOINT", "http://127.0.0.1:4317"),
        bk_data_token=os.getenv("BKAPP_OTEL_LOG_BK_DATA_TOKEN", ""),
    )

    """
    End 初始化步骤
    """

    """
    Start 上报日志，调用 Client 进行上报，Client 可重复使用
    """

    # 上报日志
    bk_audit_client.add_event(
        action=ViewFileAction,
        resource_type=HostResourceType,
        instance=HostInstance(Host()).instance,
        audit_context=AuditContext(username="admin", scope_type="project", scope_id="bk-audit"),
    )

    """
    End 上报日志
    """


if __name__ == "__main__":
    report_audit_log()
