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

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import (
    LogEmitterProvider,
    LoggingHandler,
    set_log_emitter_provider,
)
from opentelemetry.sdk._logs.export import BatchLogProcessor
from opentelemetry.sdk.resources import Resource

from bk_audit.constants.utils import OT_LOGGER_NAME


def setup(client):
    """
    初始化OT日志
    @type client: bk_audit.client.BkAudit
    @param client: 审计Client
    """
    service_name = client.service_name
    bk_data_id = int(os.getenv("BKAPP_OTEL_LOG_BK_DATA_ID", -1))
    bk_data_token = os.getenv("BKAPP_OTEL_LOG_BK_DATA_TOKEN", "")
    log_emitter_provider = LogEmitterProvider(
        resource=Resource.create(
            {"service.name": service_name, "bk_data_id": bk_data_id, "bk.data.token": bk_data_token}
        )
    )
    set_log_emitter_provider(log_emitter_provider)
    exporter = OTLPLogExporter(endpoint=os.getenv("BKAPP_OTEL_LOG_ENDPOINT"))
    log_emitter_provider.add_log_processor(BatchLogProcessor(exporter))
    handler = LoggingHandler(
        level=logging.NOTSET,
        log_emitter=log_emitter_provider.get_log_emitter(service_name),
    )
    logging.getLogger(OT_LOGGER_NAME).addHandler(handler)
