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

from packaging import version


class LoggingDefaultConfig:
    """Logging 默认配置"""

    HANDLER_CLS = "logging.handlers.RotatingFileHandler"
    FILE_MAX_BYTES = 1024 * 1024 * 100  # 10M
    FILE_BACKUP_COUNT = 5


class OTVersion:
    """OT 更新版本"""

    # _log release
    # https://github.com/open-telemetry/opentelemetry-python/releases/tag/v1.7.1
    v1_7_1 = version.parse("1.7.1")

    # Change OTLPHandler to LoggingHandler
    # https://github.com/open-telemetry/opentelemetry-python/pull/2528
    v1_11_0 = version.parse("1.11.0")
