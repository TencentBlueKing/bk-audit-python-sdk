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

from bk_audit.constants.contrib import LoggingDefaultConfig
from bk_audit.constants.utils import LOGGER_NAME


class LoggingConfigHandler(object):
    """
    处理Logging配置
    """

    def __init__(
        self,
        filename,
        log_level=logging.INFO,
        handler_cls=LoggingDefaultConfig.HANDLER_CLS,
        file_max_bytes=LoggingDefaultConfig.FILE_MAX_BYTES,
        file_backup_count=LoggingDefaultConfig.FILE_BACKUP_COUNT,
    ):
        self.filename = filename
        self.log_level = log_level
        self.handler_cls = handler_cls
        self.file_max_bytes = file_max_bytes
        self.file_backup_count = file_backup_count

    @property
    def handler_name(self):
        return LOGGER_NAME

    @property
    def handler_config(self):
        return {
            "class": self.handler_cls,
            "formatter": self.formatter_name,
            "filename": self.filename,
            "maxBytes": self.file_max_bytes,
            "backupCount": self.file_backup_count,
        }

    @property
    def formatter_name(self):
        return LOGGER_NAME

    @property
    def formatter_config(self):
        return {"format": "%(message)s"}

    @property
    def logger_name(self):
        return LOGGER_NAME

    @property
    def logger_config(self):
        return {"handlers": [self.handler_name], "level": self.log_level, "propagate": True}

    def set_logging(self, logging_config):
        logging_config["formatters"][self.formatter_name] = self.formatter_config
        logging_config["handlers"][self.handler_name] = self.handler_config
        logging_config["loggers"][self.logger_name] = self.logger_config
        return logging_config
