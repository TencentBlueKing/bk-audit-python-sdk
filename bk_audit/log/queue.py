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


class BaseQueue(object):
    """队列"""

    def __init__(self, max_limit=0):
        """
        @type max_limit: int
        @param max_limit: 队列最大长度
        @rtype: BaseQueue
        """
        self._max_limit = max_limit
        self._storage = list()

    def _check_limit(self):
        """
        检查是否超过最大长度
        """
        current = len(self._storage)
        if self._max_limit and current > self._max_limit:
            item = self.pop()
            warnings.warn("Exceed Queue Limit %d(>%d), Drop Item %s" % (current, self._max_limit, str(item)))
            self._check_limit()

    def set_limit(self, limit):
        """
        设置最大长度
        @type limit: int
        @param limit: 队列最大长度
        """
        assert isinstance(limit, int), "Limit Invalid (Not A Number)"
        self._max_limit = limit
        self._check_limit()

    def add(self, item):
        """
        添加
        @type item: object
        @param item: 对象
        """
        self._storage.append(item)
        self._check_limit()

    def bulk_add(self, items):
        """
        批量添加
        @type items: typing.List[object]
        @param items: 对象列表
        """
        self._storage.extend(items)
        self._check_limit()

    def pop(self):
        """
        获取单个
        @rtype: typing.List[object]
        """
        if self._storage:
            return [self._storage.pop(0)]
        return []

    def pop_all(self):
        """
        获取所有
        @rtype: typing.List[object]
        """
        items = list()
        flag = True
        while flag:
            _items = self.pop()
            if _items:
                items.extend(_items)
                continue
            flag = False
        return items

    def clear(self):
        """
        清空队列
        """
        self._storage = list()


class AuditEventQueue(BaseQueue):
    """审计事件队列"""

    pass
