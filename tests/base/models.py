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

import datetime

from iam.model.models import Action as IAMAction
from iam.model.models import ResourceType as IAMResourceType


class Action(IAMAction):
    """操作"""

    def __init__(self, id):
        super(Action, self).__init__(
            id,
            name=None,
            name_en=None,
            description=None,
            description_en=None,
            type=None,
            related_resource_types=None,
            related_actions=None,
            version=None,
        )


class ResourceType(IAMResourceType):
    """资源类型"""

    def __init__(self, id):
        super(ResourceType, self).__init__(
            id,
            name=None,
            name_en=None,
            description=None,
            description_en=None,
            parents=None,
            provider_config=None,
            version=None,
        )


class Request(object):
    """请求Mock"""

    META = {}

    @property
    def user(self):
        return self

    @property
    def username(self):
        return "admin"


class Empty(object):
    """空对象"""

    pass


class Datetime(object):
    """时间对象"""

    @property
    def datetime(self):
        return self

    def now(self):
        return self

    def timestamp(self):
        raise AttributeError

    def timetuple(self):
        return datetime.datetime.now().timetuple()

    @property
    def microsecond(self):
        return datetime.datetime.now().microsecond
