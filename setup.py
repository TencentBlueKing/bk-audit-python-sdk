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

from setuptools import setup

setup(
    name="bk-audit",
    version="1.0.4-rc.0",
    author="blueking",
    url="https://bk.tencent.com",
    author_email="blueking@tencent.com",
    description="Bk Audit SDK",
    packages=[
        "bk_audit",
        "bk_audit.constants",
        "bk_audit.contrib",
        "bk_audit.contrib.django",
        "bk_audit.contrib.opentelemetry",
        "bk_audit.log",
        "bk_audit.utils",
    ],
    requires=[
        "bk_iam",
        "packaging",
    ],
    extras_require={
        # OT 仅支持 Py3.6 及以上版本
        "opentelemetry": [
            "protobuf>=3.19.5",
            "opentelemetry-api>=1.7.1,<1.13.0",
            "opentelemetry-sdk>=1.7.1,<1.13.0",
            "opentelemetry-exporter-otlp>=1.7.1,<1.13.0",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4",
)
