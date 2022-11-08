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

AUDIT_EVENT_SIGNATURE = "bk_audit_event"
AUDIT_EVENT_CONTEXT = "bk_audit_event_context"

DEFAULT_RESULT_CODE = 0
DEFAULT_SENSITIVITY = 0
DEFAULT_EMPTY_VALUE = str()

DEFAULT_QUEUE_LIMIT = 10000


class AccessTypeEnum(object):
    WEB = 0  # 网页
    API = 1  # API网关
    CONSOLE = 2  # 控制台
    OTHER = -1  # 未知


class UserIdentifyTypeEnum(object):
    PERSONAL = 0  # 个人账号
    PLATFORM = 1  # 平台账号
    UNKNOWN = -1  # 未知
