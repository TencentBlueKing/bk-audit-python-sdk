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
from functools import wraps

from bk_audit.constants.utils import LOGGER_NAME


def ignore_wrapper(message=False, default_return=None):
    """
    忽略运行时的错误，返回默认值
    @type message: bool
    @param message: 是否输出错误日志
    @type default_return: any
    @param default_return: 错误时的默认返回值
    """

    def ignore(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:  # pylint: disable=broad-except
                if message:
                    logger = logging.getLogger(LOGGER_NAME)
                    logger.exception(err)
                return default_return

        return wrapper

    return ignore
