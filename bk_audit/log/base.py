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

import warnings

from bk_audit.log.exporters import BaseExporter
from bk_audit.log.formatters import BaseFormatter
from bk_audit.log.queue import AuditEventQueue, BaseQueue


class BkAuditLog(object):
    """
    处理审计日志
    """

    def __init__(self, bk_app_code, bk_app_secret, queue=None):
        """
        @type bk_app_code: str
        @param bk_app_code: App Code
        @type bk_app_secret: str
        @param bk_app_secret: App Secret
        @type queue: BaseQueue
        @param queue: 审计事件队列
        @rtype: BkAuditLog
        """
        self._bk_app_code = bk_app_code
        self._bk_app_secret = bk_app_secret
        self._queue = queue or AuditEventQueue()
        self._formatter = None
        self._sync_exporters = []
        self._delay_exporters = []
        self._exporter_class = []

    def _check_init(self):
        """
        确保必要的参数都已经设置
        """
        assert isinstance(self._queue, BaseQueue), "Queue Invalid"
        assert isinstance(self._formatter, BaseFormatter), "Formatter Invalid"
        assert self._delay_exporters or self._sync_exporters, "Exporter Unset"

    def set_queue_limit(self, limit):
        """
        设置队列长度
        @type limit: int
        @param limit: 审计事件队列最大长度
        """
        self._queue.set_limit(limit)

    def set_formatter(self, formatter):
        """
        设置事件处理器
        @type formatter: BaseFormatter
        @param formatter: 事件处理器
        """
        self._formatter = formatter

    def add_exporter(self, exporter):
        """
        添加事件输出
        @type exporter: BaseExporter
        @param exporter: 事件输出器
        """
        assert isinstance(exporter, BaseExporter), "Exporter Invalid"
        if exporter.__class__ in self._exporter_class:
            warnings.warn("Exporter Duplicate")
        self._exporter_class.append(exporter.__class__)
        if exporter.is_delay:
            self._delay_exporters.append(exporter)
        else:
            self._sync_exporters.append(exporter)

    def add_event(self, **kwargs):
        """
        新增审计事件
        """
        self._check_init()
        event = self._formatter.build_event(**kwargs)
        event.bk_app_code = self._bk_app_code
        # 存在延迟导出的则需要将日志添加到队列
        if self._delay_exporters:
            self._queue.add(event)
        # 同步导出的直接调用
        for exporter in self._sync_exporters:
            exporter.export([event])

    def export_events(self):
        """
        导出队列中的审计事件
        """
        self._check_init()
        events = self._queue.pop_all()
        for exporter in self._delay_exporters:
            exporter.export(events)
