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

from iam.model.models import Action, ResourceType

from bk_audit.log.models import AuditInstance


class ViewFileAction(Action):
    id = "view-file"


class HostResourceType(ResourceType):
    id = "host"


class User(object):
    username = "admin"


class Host:
    id = "host-01"
    name = "主机01"
    ip = "127.0.0.1"
    update_by = "admin"
    update_at = "2022-01-01 00:00:00"


class HostInstance:
    def __init__(self, host):
        """
        @type host: Host
        """
        self.instance_id = host.id
        self.instance_name = host.name
        self.instance_data = {
            "id": host.id,
            "name": host.name,
            "ip": host.ip,
            "update_by": host.update_by,
            "update_at": host.update_at,
        }

    @property
    def instance(self):
        return AuditInstance(self)
