![logo.png](https://github.com/TencentBlueKing/bk-audit-python-sdk/blob/master/assests/logo.png)

[![license](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/TencentBlueKing/bk-audit-python-sdk/blob/master/LICENSE.txt)
[![Release Version](https://img.shields.io/badge/release-1.2.0-brightgreen.svg)](https://github.com/TencentBlueKing/bk-audit-python-sdk/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/TencentBlueKing/bk-audit-python-sdk/pulls)
[![codecov](https://codecov.io/github/TencentBlueKing/bk-audit-python-sdk/branch/master/graph/badge.svg?token=CUG20ZMOVQ)](https://codecov.io/github/TencentBlueKing/bk-audit-python-sdk)
[![Test](https://github.com/TencentBlueKing/bk-audit-python-sdk/actions/workflows/unittest_py3.yml/badge.svg)](https://github.com/TencentBlueKing/bk-audit-python-sdk/actions/workflows/unittest_py3.yml)

[(English Documents Available)](https://github.com/TencentBlueKing/bk-audit-python-sdk/blob/master/readme_en.md)

## Overview

bk-audit-python-sdk 是蓝鲸审计中心 (BK-AUDIT) 提供的用于快速接入审计体系的 Python SDK

## Features

- [Basic] 兼容 Python2/Python3
- [Audit] 支持自定义审计事件处理，将非标准字段格式化为审计事件
- [Audit] 支持自定义审计事件输出，内置审计事件输出到日志文件或通过 OT 上报
- [Contrib] Django Support, 集成了 Django 专用事件处理，通过注入 Request 对象简化审计事件上报
- [Contrib] OpenTelemetry Support, 集成 OT Log 上报模块，直接上报到 OT Collector

## Getting started

### Installation

```bash
$ pip install bk-audit
```

### Usage

- [使用文档](https://github.com/TencentBlueKing/bk-audit-python-sdk/blob/master/docs/usage.md)

## Roadmap

- [版本日志](https://github.com/TencentBlueKing/bk-audit-python-sdk/blob/master/release.md)

## Support

- [蓝鲸论坛](https://bk.tencent.com/s-mart/community)
- [蓝鲸 DevOps 在线视频教程](https://bk.tencent.com/s-mart/video/)
- [蓝鲸社区版交流群](https://jq.qq.com/?_wv=1027&k=5zk8F7G)

## BlueKing Community

- [BK-CMDB](https://github.com/Tencent/bk-cmdb)：蓝鲸配置平台（蓝鲸 CMDB）是一个面向资产及应用的企业级配置管理平台。
- [BK-CI](https://github.com/Tencent/bk-ci)：蓝鲸持续集成平台是一个开源的持续集成和持续交付系统，可以轻松将你的研发流程呈现到你面前。
- [BK-BCS](https://github.com/Tencent/bk-bcs)：蓝鲸容器管理平台是以容器技术为基础，为微服务业务提供编排管理的基础服务平台。
- [BK-PaaS](https://github.com/Tencent/bk-paas)：蓝鲸 PaaS 平台是一个开放式的开发平台，让开发者可以方便快捷地创建、开发、部署和管理 SaaS 应用。
- [BK-SOPS](https://github.com/Tencent/bk-sops)：标准运维（SOPS）是通过可视化的图形界面进行任务流程编排和执行的系统，是蓝鲸体系中一款轻量级的调度编排类 SaaS 产品。
- [BK-JOB](https://github.com/Tencent/bk-job) 蓝鲸作业平台(Job)是一套运维脚本管理系统，具备海量任务并发处理能力。

## Contributing

如果你有好的意见或建议，欢迎给我们提 Issues 或 Pull Requests，为蓝鲸开源社区贡献力量。   
[腾讯开源激励计划](https://opensource.tencent.com/contribution) 鼓励开发者的参与和贡献，期待你的加入。

## License

基于 MIT 协议， 详细请参考 [LICENSE](https://github.com/TencentBlueKing/bk-audit-python-sdk/blob/master/License.txt)
