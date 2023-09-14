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

import logging
import os
from typing import Type

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import (
    LogEmitterProvider,
    LogProcessor,
    set_log_emitter_provider,
)
from opentelemetry.sdk._logs.export import SimpleLogProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.version import __version__ as _ot_version
from packaging import version

from bk_audit.constants.contrib import OTVersion
from bk_audit.constants.utils import OT_LOGGER_NAME
from bk_audit.contrib.opentelemetry.processor import LazyBatchLogProcessor

OT_VERSION = version.parse(_ot_version)


def setup(
    client,
    bk_data_id=None,
    bk_data_token=None,
    endpoint=None,
):
    """
    初始化OT日志
    @type client: bk_audit.client.BkAudit
    @param client: 审计Client
    @type bk_data_id: int
    @param bk_data_id: Data ID
    @type bk_data_token: str
    @param bk_data_token: Data Token
    @type endpoint: str
    @param endpoint: 上报地址
    """

    if OT_VERSION < OTVersion.v1_11_0:
        from opentelemetry.sdk._logs import OTLPHandler as LoggingHandler
    else:
        from opentelemetry.sdk._logs import LoggingHandler

    # init service config
    service_name = client.service_name
    bk_data_id = bk_data_id or int(os.getenv("BKAPP_OTEL_LOG_BK_DATA_ID", -1))
    bk_data_token = bk_data_token or os.getenv("BKAPP_OTEL_LOG_BK_DATA_TOKEN", "")

    # init log emitter
    log_emitter_provider = LogEmitterProvider(
        resource=Resource.create(
            {"service.name": service_name, "bk_data_id": bk_data_id, "bk.data.token": bk_data_token}
        )
    )
    set_log_emitter_provider(log_emitter_provider)

    # init exporter
    processor: Type[LogProcessor] = LazyBatchLogProcessor
    if os.getenv("BKAPP_USE_SIMPLE_LOG_PROCESSOR"):
        processor = SimpleLogProcessor
    exporter = OTLPLogExporter(endpoint=endpoint or os.getenv("BKAPP_OTEL_LOG_ENDPOINT"))
    log_emitter_provider.add_log_processor(processor(exporter))

    # init logging
    handler = LoggingHandler(
        level=logging.NOTSET,
        log_emitter=log_emitter_provider.get_log_emitter(service_name),
    )
    logging.getLogger(OT_LOGGER_NAME).addHandler(handler)
