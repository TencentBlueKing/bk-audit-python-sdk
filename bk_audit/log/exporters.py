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

import abc
import logging

from bk_audit.constants.utils import LOGGER_NAME


class BaseExporter(object):
    """
    审计事件导出
    """

    @property
    @abc.abstractmethod
    def is_delay(self):
        """
        True: 日志输入后直接导出
        False: 日志输入后，等待调用 BkAuditLog.export_events 时导出
        @rtype: bool
        """
        pass

    @abc.abstractmethod
    def export(self, events):
        """
        实际输出方法
        @type events: typing.List[bk_audit.log.models.AuditEvent]
        @param events: 审计事件列表
        """
        pass


class LoggerExporter(BaseExporter):
    """
    日志导出
    """

    is_delay = False

    def export(self, events):
        """
        直接输出到日志
        @type events: typing.List[bk_audit.log.models.AuditEvent]
        @param events: 审计事件列表
        """
        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.INFO)
        for event in events:
            logger.info(event.to_json_str())
