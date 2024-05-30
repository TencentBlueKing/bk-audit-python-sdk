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

from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler, LogRecordProcessor
from opentelemetry.sdk._logs.export import SimpleLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from bk_audit.constants.utils import OT_LOGGER_NAME
from bk_audit.contrib.opentelemetry.processor import LazyBatchLogProcessor


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

    # init service config
    service_name = client.service_name
    bk_data_id = bk_data_id or int(os.getenv("BKAPP_OTEL_LOG_BK_DATA_ID", -1))
    bk_data_token = bk_data_token or os.getenv("BKAPP_OTEL_LOG_BK_DATA_TOKEN", "")

    # init log emitter
    logger_provider = LoggerProvider(
        resource=Resource.create(
            {
                "service.name": service_name,
                "bk_data_id": bk_data_id,
                "bk.data.token": bk_data_token,
            }
        )
    )
    set_logger_provider(logger_provider)

    # init exporter
    processor: Type[LogRecordProcessor] = LazyBatchLogProcessor
    if os.getenv("BKAPP_USE_SIMPLE_LOG_PROCESSOR"):
        processor = SimpleLogRecordProcessor
    exporter = OTLPLogExporter(endpoint=endpoint or os.getenv("BKAPP_OTEL_LOG_ENDPOINT"))
    logger_provider.add_log_record_processor(processor(exporter))

    # init logging
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logging.getLogger(OT_LOGGER_NAME).addHandler(handler)
