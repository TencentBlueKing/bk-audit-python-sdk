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

from bk_audit.log.formatters import Formatter


class UserFormatter(Formatter):
    def build_event(
        self,
        audit_context,
        action,
        resource_type,
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
        @type audit_context: bk_audit.log.models.AuditContext
        @type action: bk_audit.log.models.AuditAction
        @type resource_type: bk_audit.log.models.AuditResourceType
        @type instance: bk_audit.log.models.AuditInstance
        @type event_id: str
        @type event_content: str
        @type start_time: int
        @type end_time: int
        @type result_code: int
        @type result_content: str
        @type extend_data: dict
        @rtype: AuditEvent
        """
        user = getattr(audit_context, "user", None)
        if user:
            audit_context.username = user.username
        return super(UserFormatter, self).build_event(
            audit_context=audit_context,
            action=action,
            resource_type=resource_type,
            instance=instance,
            event_id=event_id,
            event_content=event_content,
            start_time=start_time,
            end_time=end_time,
            result_code=result_code,
            result_content=result_content,
            extend_data=extend_data,
        )
