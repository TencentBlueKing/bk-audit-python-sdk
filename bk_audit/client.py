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

import uuid

from bk_audit.constants.log import (
    DEFAULT_EMPTY_VALUE,
    DEFAULT_QUEUE_LIMIT,
    DEFAULT_RESULT_CODE,
)
from bk_audit.log.base import BkAuditLog
from bk_audit.log.exporters import LoggerExporter
from bk_audit.log.formatters import Formatter
from bk_audit.log.models import (
    AuditAction,
    AuditContext,
    AuditInstance,
    AuditResourceType,
)
from bk_audit.utils.time_tool import get_current_ms_ts


class BkAudit(object):
    """审计SDK"""

    def __init__(self, bk_app_code, bk_app_secret, settings=None):
        """
        @type bk_app_code: str
        @param bk_app_code: App Code
        @type bk_app_secret: str
        @param bk_app_secret: App Secret
        @type settings: dict
        @param settings: 设置
        @rtype: BkAudit
        """
        self._bk_app_code = bk_app_code
        self._bk_app_secret = bk_app_secret
        self._settings = settings or {}
        self._log = BkAuditLog(self._bk_app_code, self._bk_app_secret)
        self.service_name = bk_app_code
        self._init_settings()

    def _init_settings(self):
        """
        从设置初始化
        """
        # 初始化审计日志队列长度
        queue_limit = self._settings.get("log_queue_limit", DEFAULT_QUEUE_LIMIT)
        self.set_queue_limit(queue_limit)
        # 初始化审计日志处理实例
        formatter = self._settings.get("formatter", Formatter())
        self.set_formatter(formatter)
        # 初始化审计日志输出实例
        exporters = self._settings.get("exporters", [LoggerExporter()])
        for exporter in exporters:
            self.add_exporter(exporter)
        # 初始化OT日志
        service_name_handler = self._settings.get("service_name_handler")
        if service_name_handler:
            self.service_name = service_name_handler(self.service_name).get_service_name()

    def set_queue_limit(self, limit):
        """
        设置队列长度
        @type limit: int
        @param limit: 审计事件队列最大长度
        """
        self._log.set_queue_limit(limit)

    def set_log(self, log):
        """
        设置审计日志实例
        @type log: BkAuditLog
        @param log: 审计日志实例
        """
        self._log = log

    def set_formatter(self, formatter):
        """
        设置审计事件处理实例
        @type formatter: bk_audit.log.formatters.BaseFormatter
        @param formatter: 审计事件处理器
        """
        self._log.set_formatter(formatter)

    def add_exporter(self, exporter):
        """
        添加审计事件输出实例
        @type exporter: bk_audit.log.exporters.BaseExporter
        @param exporter: 审计事件输出器
        """
        self._log.add_exporter(exporter)

    def add_event(
        self,
        action,
        resource_type=None,
        instance=None,
        audit_context=None,
        event_id=None,
        event_content=DEFAULT_EMPTY_VALUE,
        start_time=None,
        end_time=None,
        result_code=DEFAULT_RESULT_CODE,
        result_content=DEFAULT_EMPTY_VALUE,
        extend_data=DEFAULT_EMPTY_VALUE,
    ):
        """
        添加审计事件
        @type audit_context: bk_audit.log.models.AuditContext
        @param audit_context: 审计上下文
        @type action: bk_audit.log.models.AuditAction
        @param action: 操作
        @type resource_type: bk_audit.log.models.AuditResourceType
        @param resource_type: 资源类型
        @type instance: bk_audit.log.models.AuditInstance
        @param instance: 审计实例对象
        @type event_id: str
        @param event_id: 事件ID
        @type event_content: str
        @param event_content: 事件描述
        @type start_time: int
        @param start_time: 事件开始时间
        @type end_time: int
        @param end_time: 事件结束时间
        @type result_code: int
        @param result_code: 操作结果
        @type result_content: str
        @param result_content: 操作结果描述
        @type extend_data: dict
        @param extend_data: 拓展信息
        """
        if not audit_context:
            audit_context = AuditContext()
        if not instance:
            instance = AuditInstance(object())
        action = AuditAction(action) if action else AuditAction(object())
        resource_type = AuditResourceType(resource_type) if resource_type else AuditResourceType(object())
        self._log.add_event(
            audit_context=audit_context,
            action=action,
            resource_type=resource_type,
            instance=instance,
            event_id=event_id or uuid.uuid1().hex,
            event_content=event_content,
            start_time=start_time or get_current_ms_ts(),
            end_time=end_time or get_current_ms_ts(),
            result_code=result_code,
            result_content=result_content,
            extend_data=extend_data,
        )

    def export_events(self):
        """
        导出审计事件
        """
        self._log.export_events()
