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

from opentelemetry.sdk._logs.export import BatchLogRecordProcessor


class LazyBatchLogProcessor(BatchLogRecordProcessor):
    """
    历史兼容类名保留。

    旧版本为规避 fork 后 worker 线程失效，通过操作 OTel 私有成员实现
    「首次 emit 才启动 worker」的懒启动行为；
    OTel >= 1.34 起 BatchLogRecordProcessor 内部重构并官方内建 fork 安全
    （os.register_at_fork + pid 变化自动重建 daemon worker），
    懒启动已无必要，本类行为等价于标准 BatchLogRecordProcessor。
    """
