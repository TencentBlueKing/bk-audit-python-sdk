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

from unittest import TestCase
from unittest.mock import patch

from bk_audit.utils.decorators import ignore_wrapper
from bk_audit.utils.time_tool import get_current_ts
from tests.base.models import Datetime, Empty


class TestUtils(TestCase):
    """测试工具"""

    def test_ignore_wrapper(self):
        """测试忽略异常"""

        empty = Empty()

        @ignore_wrapper(default_return=empty, message=True)
        def func():
            raise Exception

        self.assertEqual(func(), empty)

    def test_get_current_ts(self):
        """测试获取时间戳"""
        self.assertEqual(type(get_current_ts()), float)

    @patch("bk_audit.utils.time_tool.datetime", Datetime())
    def test_get_current_ts_py2(self):
        """测试获取时间戳(Py2)"""
        self.assertEqual(type(get_current_ts()), float)
