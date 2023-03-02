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

import json
import uuid

from bk_audit.constants.log import (
    AUDIT_EVENT_SIGNATURE,
    DEFAULT_EMPTY_VALUE,
    DEFAULT_RESULT_CODE,
    DEFAULT_SENSITIVITY,
    AccessTypeEnum,
    UserIdentifyTypeEnum,
)
from bk_audit.utils.time_tool import get_current_ms_ts


class AuditEvent(object):
    """
    审计事件
    """

    def __init__(
        self,
        event_id=None,
        event_content=DEFAULT_EMPTY_VALUE,
        request_id=DEFAULT_EMPTY_VALUE,
        username=DEFAULT_EMPTY_VALUE,
        user_identify_type=UserIdentifyTypeEnum.UNKNOWN,
        user_identify_tenant_id=DEFAULT_EMPTY_VALUE,
        start_time=0,
        end_time=0,
        bk_app_code=DEFAULT_EMPTY_VALUE,
        access_type=AccessTypeEnum.OTHER,
        access_source_ip=DEFAULT_EMPTY_VALUE,
        access_user_agent=DEFAULT_EMPTY_VALUE,
        action_id=DEFAULT_EMPTY_VALUE,
        resource_type_id=DEFAULT_EMPTY_VALUE,
        instance_id=DEFAULT_EMPTY_VALUE,
        instance_name=DEFAULT_EMPTY_VALUE,
        instance_sensitivity=DEFAULT_SENSITIVITY,
        instance_data=DEFAULT_EMPTY_VALUE,
        instance_origin_data=DEFAULT_EMPTY_VALUE,
        result_code=DEFAULT_RESULT_CODE,
        result_content=DEFAULT_EMPTY_VALUE,
        extend_data=DEFAULT_EMPTY_VALUE,
    ):
        """
        @type event_id: str
        @param event_id: 事件ID
        @type event_content: str
        @param event_content: 事件描述
        @type request_id: str
        @param request_id: 请求ID
        @type username: str
        @param username: 操作人用户名
        @type user_identify_type: int
        @param user_identify_type: 操作人账号类型
        @type user_identify_tenant_id: str
        @param user_identify_tenant_id: 操作人租户ID
        @type start_time: int
        @param start_time: 事件开始事件
        @type end_time: int
        @param end_time: 事件结束时间
        @type bk_app_code: str
        @param bk_app_code: 事件上报模块
        @type access_type: int
        @param access_type: 访问方式
        @type access_source_ip: str
        @param access_source_ip: 访问来源IP地址
        @type access_user_agent: str
        @param access_user_agent: 访问客户端类型
        @type action_id: str
        @param action_id: 操作ID
        @type resource_type_id: str
        @param resource_type_id: 资源类型ID
        @type instance_id: str
        @param instance_id: 实例ID
        @type instance_name: str
        @param instance_name: 实例名称
        @type instance_sensitivity: int
        @param instance_sensitivity: 实例敏感等级
        @type instance_data: dict
        @param instance_data: 实例数据
        @type instance_origin_data: dict
        @param instance_origin_data: 实例原始数据
        @type result_code: int
        @param result_code: 操作结果
        @type result_content: str
        @param result_content: 操作结果描述
        @type extend_data: dict
        @param extend_data: 拓展信息
        @rtype: AuditEvent
        """
        self.event_id = event_id or uuid.uuid1().hex
        self.event_content = event_content
        self.request_id = request_id
        self.username = username
        self.user_identify_type = int(user_identify_type)
        self.user_identify_tenant_id = user_identify_tenant_id
        self.start_time = int(start_time) or get_current_ms_ts()
        self.end_time = int(end_time) or get_current_ms_ts()
        self.bk_app_code = bk_app_code
        self.access_type = int(access_type)
        self.access_source_ip = access_source_ip
        self.access_user_agent = access_user_agent
        self.action_id = action_id
        self.resource_type_id = resource_type_id
        self.instance_id = instance_id
        self.instance_name = instance_name
        self.instance_sensitivity = instance_sensitivity
        self.instance_data = instance_data or {}
        self.instance_origin_data = instance_origin_data or {}
        self.result_code = int(result_code)
        self.result_content = result_content
        self.extend_data = extend_data or {}
        self.bk_log_scope = AUDIT_EVENT_SIGNATURE

    def __str__(self):
        """
        字符串函数
        @rtype: str
        """
        return self.event_id

    def _validate(self):
        """
        数据校验
        """
        key_params = ["event_id", "username", "start_time", "action_id"]
        errors = []
        for key in key_params:
            if not getattr(self, key, None):
                errors.append(key)
        assert not errors, "Audit Event Key Params Unset => %s" % ",".join(errors)

    def to_json_str(self):
        """
        获取JSON字符串
        @rtype: str
        """
        return json.dumps(self.to_json(), ensure_ascii=False)

    def to_json(self):
        """
        获取JSON内容
        @rtype: dict
        """
        self._validate()
        return {key: val for key, val in self.__dict__.items() if not key.startswith("_") and not callable(val)}


class AuditInstance(object):
    """
    审计对象
    """

    def __init__(self, instance):
        """
        @type instance: object
        @param instance: 实例对象
        @rtype: AuditInstance
        """
        self.instance = instance

    @property
    def instance_id(self):
        """
        实例ID
        @rtype: str
        """
        return getattr(self.instance, "instance_id", DEFAULT_EMPTY_VALUE)

    @property
    def instance_name(self):
        """
        实例名
        @rtype: str
        """
        return getattr(self.instance, "instance_name", DEFAULT_EMPTY_VALUE)

    @property
    def instance_sensitivity(self):
        """
        实例风险等级
        @rtype: int
        """
        return getattr(self.instance, "instance_sensitivity", DEFAULT_SENSITIVITY)

    @property
    def instance_data(self):
        """
        实例信息 JSON
        @rtype: dict
        """
        return getattr(self.instance, "instance_data", DEFAULT_EMPTY_VALUE)

    @property
    def instance_origin_data(self):
        """
        实例修改前内容
        @rtype: dict
        """
        return getattr(self.instance, "instance_origin_data", DEFAULT_EMPTY_VALUE)


class AuditAction(object):
    """
    操作
    """

    def __init__(self, action):
        """
        @type action: iam.model.models.Action|object
        @param action: 审计操作
        @rtype: AuditAction
        """
        self.action = action

    @property
    def id(self):
        """
        操作ID
        @rtype: str
        """
        return getattr(self.action, "id", DEFAULT_EMPTY_VALUE)


class AuditResourceType(object):
    """
    资源类型
    """

    def __init__(self, resource_type):
        """
        @type resource_type: iam.model.models.ResourceType|object
        @param resource_type: 审计资源类型
        @rtype: AuditResourceType
        """
        self.resource_type = resource_type

    @property
    def id(self):
        """
        资源类型ID
        @rtype: str
        """
        return getattr(self.resource_type, "id", DEFAULT_EMPTY_VALUE)


class AuditContext(object):
    """
    上下文
    """

    def __init__(
        self,
        username=DEFAULT_EMPTY_VALUE,
        request_id=DEFAULT_EMPTY_VALUE,
        access_type=AccessTypeEnum.OTHER,
        access_source_ip=DEFAULT_EMPTY_VALUE,
        access_user_agent=DEFAULT_EMPTY_VALUE,
        user_identify_type=UserIdentifyTypeEnum.UNKNOWN,
        user_identify_tenant_id=DEFAULT_EMPTY_VALUE,
        **kwargs
    ):
        """
        @type username: str
        @param username: 操作人用户名
        @type request_id: str
        @param request_id: 请求ID
        @type access_type: int
        @param access_type: 访问方式
        @type access_source_ip: str
        @param access_source_ip: 访问来源IP地址
        @type access_user_agent: str
        @param access_user_agent: 访问客户端类型
        @type user_identify_type: int
        @param user_identify_type: 操作人账号类型
        @type user_identify_tenant_id: str
        @param user_identify_tenant_id: 操作人租户ID
        @rtype: AuditContext
        """
        self.username = username
        self.request_id = request_id
        self.access_type = access_type
        self.access_source_ip = access_source_ip
        self.access_user_agent = access_user_agent
        self.user_identify_type = user_identify_type
        self.user_identify_tenant_id = user_identify_tenant_id
        for key, val in kwargs.items():
            setattr(self, key, val)
