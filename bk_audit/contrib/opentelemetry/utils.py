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
import sys


class BaseServiceNameHandler(object):
    """
    服务名处理
    """

    def __init__(self, service_name):
        """
        @type service_name: str
        @param service_name: 服务名
        @rtype: BaseServiceNameHandler
        """
        self._service_name = service_name

    @abc.abstractmethod
    def get_service_name(self):
        """
        获取服务名
        @rtype: str
        """
        pass


class ServiceNameHandler(BaseServiceNameHandler):
    """
    服务名处理
    """

    class SuffixEnum(object):
        CELERY_BEAT = "celery_beat"
        CELERY_WORKER = "celery_worker"
        API = "api"
        NONE = ""

    @property
    def is_celery(self):
        """
        判断是否为 Celery Worker
        @rtype: bool
        """
        return "celery" in sys.argv

    @property
    def is_celery_beat(self):
        """
        判断是否为 Celery Beat
        @rtype: bool
        """
        return self.is_celery and "beat" in sys.argv

    @property
    def suffix(self):
        """
        获取服务名后缀
        @rtype: str
        """
        if self.is_celery_beat:
            return self.SuffixEnum.CELERY_BEAT
        if self.is_celery:
            return self.SuffixEnum.CELERY_WORKER
        return self.SuffixEnum.NONE

    def get_service_name(self):
        """
        获取服务名
        @rtype: str
        """
        if self.suffix:
            return "{}_{}".format(self._service_name, self.suffix)
        return self._service_name
