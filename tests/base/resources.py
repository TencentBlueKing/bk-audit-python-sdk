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

from iam import Action

from bk_audit.contrib.django.resources import AuditMixinResource
from bk_audit.log.models import AuditContext, AuditInstance
from tests.base.exceptions import BlueError
from tests.base.models import Request


class EmptyResource(AuditMixinResource):
    @property
    def audit_action(self):
        return super().audit_action

    @property
    def name(self):
        return super().name

    def perform_request(self, validated_request_data):
        return


class Resource(EmptyResource):
    name = "Resource"
    audit_action = Action(id="test")

    def perform_request(self, validated_request_data):
        self.add_audit_instance_to_context(AuditInstance(object()))
        return

    def _before_add_event(self) -> None:
        super(Resource, self)._before_add_event()
        self._audit_event["audit_context"] = AuditContext(request=Request())


class ErrorResource(Resource):
    def perform_request(self, validated_request_data):
        raise Exception()


class BlueErrorResource(Resource):
    def perform_request(self, validated_request_data):
        raise BlueError()
