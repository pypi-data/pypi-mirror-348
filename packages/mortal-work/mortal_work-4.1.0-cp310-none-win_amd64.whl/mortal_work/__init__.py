# cython: language_level=3
# #!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/17 9:28
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
__all__ = ["MortalWork"]
from .work_main import MortalWorkMain


class MortalWork(MortalWorkMain):
    """
    MortalWork 类继承自 MortalWorkMain，提供了与 Bonade SaaS 签名相关的功能。
    """

    def bonade_saas_sign(self, data, env="", update_time=True):
        """
        对给定的数据进行 Bonade SaaS 签名操作。

        :param data: 需要进行签名的数据。
        :param env: 环境标识，默认为空字符串。
        :param update_time: 是否更新时间戳，默认为 True。
        """
        return self._bonade_saas_sign(data, env, update_time)

    def bonade_saas_sign_params(self, params, env="", update_time=True):
        """
        对给定的参数进行 Bonade SaaS 签名操作。

        :param params: 需要进行签名的参数。
        :param env: 环境标识，默认为空字符串。
        :param update_time: 是否更新时间戳，默认为 True。
        """
        return self._bonade_saas_sign_params(params, env, update_time)

    def bonade_test_case_review(self, content):
        """
        执行 Bonade 测试用例的评审操作。

        :param content: 需要评审的测试用例内容，接口 /metersphere-api/track/test/review/case/list/{page}/{size} 的 curl。
        """
        return self._bonade_test_case_review(content)

    def bonade_test_case_production_demand(self, content):
        """
        执行 Bonade 生成投产需求文案操作。

        :param content: BAPD复制出来的需求标题和链接。
        """
        return self._bonade_test_production_demand(content)
