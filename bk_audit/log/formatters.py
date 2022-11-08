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

import abc

from bk_audit.log.models import AuditEvent


class BaseFormatter(object):
    """
    事件处理
    """

    @abc.abstractmethod
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
        @rtype: AuditEvent
        """
        pass


class Formatter(BaseFormatter):
    """
    基础处理，直接转换为审计事件
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
        @rtype: AuditEvent
        """
        return AuditEvent(
            event_id=event_id,
            event_content=event_content,
            request_id=audit_context.request_id,
            username=audit_context.username,
            user_identify_type=audit_context.user_identify_type,
            user_identify_tenant_id=audit_context.user_identify_tenant_id,
            start_time=start_time,
            end_time=end_time,
            access_type=audit_context.access_type,
            access_source_ip=audit_context.access_source_ip,
            access_user_agent=audit_context.access_user_agent,
            action_id=action.id,
            resource_type_id=resource_type.id,
            instance_id=instance.instance_id,
            instance_name=instance.instance_name,
            instance_sensitivity=instance.instance_sensitivity,
            instance_data=instance.instance_data,
            instance_origin_data=instance.instance_origin_data,
            result_code=result_code,
            result_content=result_content,
            extend_data=extend_data,
        )
