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

from opentelemetry.sdk._logs.export import BatchLogProcessor


class LazyBatchLogProcessor(BatchLogProcessor):
    def __init__(self, *args, **kwargs):
        super(LazyBatchLogProcessor, self).__init__(*args, **kwargs)
        # shutdown
        self._shutdown = True
        with self._condition:
            self._condition.notify_all()
        self._worker_thread.join()
        # clean worker thread
        self._shutdown = False
        self._worker_thread = None

    def emit(self, log_data) -> None:
        # re init work thread
        if self._worker_thread is None:
            self._at_fork_reinit()
        # emit
        super(LazyBatchLogProcessor, self).emit(log_data)

    def shutdown(self) -> None:
        # shutdown
        self._shutdown = True
        with self._condition:
            self._condition.notify_all()
        # work thread exist
        if self._worker_thread:
            self._worker_thread.join()
        # shutdown exporter
        self._exporter.shutdown()

    def force_flush(self, timeout_millis=None):
        if self._shutdown or self._worker_thread is None:
            return True
        super().force_flush(timeout_millis)
