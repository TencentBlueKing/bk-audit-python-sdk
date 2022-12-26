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

import json
import logging

from bk_audit.constants.utils import OT_LOGGER_NAME
from bk_audit.log.exporters import BaseExporter


class OTLogExporter(BaseExporter):
    """
    OT日志输出
    """

    is_delay = False

    def _trans_json(self, data):
        for key, val in data.items():
            if isinstance(val, (dict, list)):
                try:
                    data[key] = json.dumps(val)
                except Exception:  # pylint: disable=broad-except
                    data[key] = str(val)
            elif isinstance(val, int):
                data[key] = val
            else:
                data[key] = str(val)
        return data

    def export(self, events):
        """
        实际输出方法
        @type events: typing.List[bk_audit.log.models.AuditEvent]
        @param events: 审计事件列表
        """
        ot_logger = logging.getLogger(OT_LOGGER_NAME)
        ot_logger.setLevel(logging.INFO)
        for event in events:
            ot_logger.info(event.event_content, extra=self._trans_json(event.to_json()))
