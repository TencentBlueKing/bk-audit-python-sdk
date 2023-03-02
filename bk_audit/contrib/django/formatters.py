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
    AccessTypeEnum,
    UserIdentifyTypeEnum,
)
from bk_audit.log.formatters import Formatter
from bk_audit.utils.decorators import ignore_wrapper


class DjangoFormatter(Formatter):
    """
    Django事件处理
    """

    def build_event(
        self,
        action,
        resource_type,
        audit_context,
        instance,
        event_id,
        event_content,
        start_time,
        end_time,
        result_code,
        result_content,
        extend_data,
    ):
        """
        构造审计事件
        @type action: bk_audit.log.models.AuditAction
        @param action: 操作
        @type resource_type: bk_audit.log.models.AuditResourceType
        @param resource_type: 资源类型
        @type audit_context: bk_audit.log.models.AuditContext
        @param audit_context: 审计上下文
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
        @rtype: bk_audit.log.models.AuditEvent
        """
        request = getattr(audit_context, "request", None)
        if request:
            audit_context.username = self.get_request_username(request)
            audit_context.request_id = self.get_request_id(request)
            audit_context.access_type = self.get_access_type(request)
            audit_context.access_source_ip = self.get_access_source_ip(request)
            audit_context.access_user_agent = self.get_access_user_agent(request)
            audit_context.user_identify_type = UserIdentifyTypeEnum.UNKNOWN
            audit_context.user_identify_tenant_id = DEFAULT_EMPTY_VALUE
        return super(DjangoFormatter, self).build_event(
            action=action,
            resource_type=resource_type,
            audit_context=audit_context,
            instance=instance,
            event_id=event_id,
            event_content=event_content,
            start_time=start_time,
            end_time=end_time,
            result_code=result_code,
            result_content=result_content,
            extend_data=extend_data,
        )

    @ignore_wrapper(default_return=DEFAULT_EMPTY_VALUE)
    def get_request_id(self, request):
        return getattr(request, "request_id", uuid.uuid1().hex)

    @ignore_wrapper(default_return=DEFAULT_EMPTY_VALUE)
    def get_request_username(self, request):
        return request.user.username

    @ignore_wrapper(default_return=AccessTypeEnum.OTHER)
    def get_access_type(self, request):
        if hasattr(request, "app"):
            return AccessTypeEnum.API
        return AccessTypeEnum.WEB

    @ignore_wrapper(default_return=DEFAULT_EMPTY_VALUE)
    def get_access_source_ip(self, request):
        if request.META.get("HTTP_X_REAL_IP"):
            return request.META.get("HTTP_X_REAL_IP")
        if request.META.get("HTTP_X_FORWARDED_FOR"):
            return request.META.get("HTTP_X_FORWARDED_FOR").replace(" ", "").split(",")[0]
        return request.META.get("REMOTE_ADDR", DEFAULT_EMPTY_VALUE)

    @ignore_wrapper(default_return=DEFAULT_EMPTY_VALUE)
    def get_access_user_agent(self, request):
        return request.META.get("HTTP_USER_AGENT", DEFAULT_EMPTY_VALUE)
