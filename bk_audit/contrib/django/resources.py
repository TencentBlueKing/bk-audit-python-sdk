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
import datetime
import sys
from typing import Optional, Union

from bk_resource import Resource
from bk_resource.base import Empty
from blueapps.core.exceptions import BlueException
from django.utils.module_loading import import_string
from iam import Action as SimpleAction
from iam import Resource as SimpleResourceType
from iam.model.models import Action, ResourceType
from rest_framework import status

from bk_audit.client import BkAudit
from bk_audit.constants.log import DEFAULT_EMPTY_VALUE, DEFAULT_RESULT_CODE
from bk_audit.log.models import (
    AuditAction,
    AuditContext,
    AuditInstance,
    AuditResourceType,
)

if sys.version_info >= (3, 8):
    from functools import cached_property
    from typing import TypedDict
else:
    cached_property = property
    from typing_extensions import TypedDict


# noinspection PyCompatibility
class AuditEvent(TypedDict):
    action: Union[AuditAction, SimpleAction, Action]
    resource_type: Optional[Union[AuditResourceType, SimpleResourceType, ResourceType]]
    instance: Optional[AuditInstance]
    audit_context: Optional[AuditContext]
    event_id: Optional[str]
    event_content: Optional[str]
    start_time: Optional[int]
    end_time: Optional[int]
    result_code: Optional[int]
    result_content: Optional[str]
    extend_data: Optional[dict]


# noinspection PyCompatibility
class AuditMixin(abc.ABC):
    """
    审计集成
    """

    _tmp_context: object
    _audit_event: AuditEvent
    _bk_audit_client_path = "bk_audit.contrib.bk_audit.client.bk_audit_client"
    name: str

    @cached_property
    def _bk_audit_client(self) -> BkAudit:
        return import_string(self._bk_audit_client_path)

    @property
    def audit_action(self) -> Optional[Union[AuditAction, SimpleAction, Action]]:
        """
        操作
        """

        return None

    @property
    def audit_resource_type(self) -> Optional[Union[AuditResourceType, SimpleResourceType, ResourceType]]:
        """
        资源类型
        """

        return None

    def _init_audit_event(self, request_data=None, **kwargs) -> AuditEvent:
        """
        初始化审计事件
        """

        return {
            "action": self.audit_action,
            "resource_type": self.audit_resource_type,
            "instance": None,
            "audit_context": None,
            "event_id": None,
            "event_content": str(self.name),
            "start_time": int(datetime.datetime.now().timestamp() * 1000),
            "end_time": None,
            "result_code": DEFAULT_RESULT_CODE,
            "result_content": DEFAULT_EMPTY_VALUE,
            "extend_data": {},
        }

    def _add_audit_event_error(self, error: Union[BlueException, Exception]) -> None:
        """
        添加异常信息到审计事件
        """

        if hasattr(error, "code") and hasattr(error, "message"):
            self._audit_event.update({"result_code": error.code, "result_content": str(error.message)})
            return
        self._audit_event.update({"result_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "result_content": str(error)})

    def _add_audit_event_response(self, response: any) -> None:
        """
        添加响应到审计事件
        """

        return

    def _add_audit_event_instance(self) -> None:
        """
        添加实例数据到审计事件
        """

        self._audit_event["instance"] = getattr(self._tmp_context, "_audit_instance", None)

    def add_audit_instance_to_context(self, instance: AuditInstance) -> None:
        """
        添加实例数据到上下文
        """

        setattr(self._tmp_context, "_audit_instance", instance)

    def _before_add_event(self) -> None:
        """
        上报前处理审计事件
        """

        self._audit_event["end_time"] = int(datetime.datetime.now().timestamp() * 1000)


# noinspection PyCompatibility
class AuditMixinResource(Resource, AuditMixin, abc.ABC):
    """
    集成审计日志上报的 Resource
    """

    def __init__(self, context=None):
        super().__init__(context=context)
        self._tmp_context = Empty()

    def request(self, request_data=None, **kwargs):
        """
        调用Resource
        """

        # 判定是否需要上报审计事件
        if not self._enabled_audit_report():
            return super().request(request_data=request_data, **kwargs)

        # 初始化审计事件
        self._audit_event = self._init_audit_event(request_data=request_data, **kwargs)

        try:
            # 调用Resource
            response_data = super().request(request_data=request_data, **kwargs)
            # 添加响应内容到审计事件
            self._add_audit_event_response(response=response_data)
            return response_data
        except Exception as err:
            # 添加异常到审计事件
            self._add_audit_event_error(error=err)
            raise err
        finally:
            # 添加实例数据到审计事件
            self._add_audit_event_instance()
            # 上报前处理审计事件
            self._before_add_event()
            self._bk_audit_client.add_event(**self._audit_event)

    def _enabled_audit_report(self) -> bool:
        """
        判定是否需要上报审计事件
        """

        return self.audit_action is not None
