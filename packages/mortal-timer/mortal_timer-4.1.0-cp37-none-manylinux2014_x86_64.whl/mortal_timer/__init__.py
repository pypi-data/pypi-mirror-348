# cython: language_level=3
# #!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 17:44
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .timer_main import MortalTimerMain


class MortalTimer(MortalTimerMain):
    """
    MortalTimer 类继承自 MortalTimerMain，用于管理定时任务的启动、停止和等待。

    该类提供了对定时任务的基本控制功能，包括启动定时器、停止定时器以及等待定时器完成。
    """

    def __init__(self, func, *args, **kwargs):
        """
        初始化 MortalTimer 实例。

        :param func: 定时任务要执行的函数。
        :param args: 传递给 func 的位置参数。
        :param kwargs: 传递给 func 的关键字参数。
        """
        super().__init__(func, *args, **kwargs)

    def start(self, interval, mark=None, once=False, timer_ranges=0, ranges_stop=0):
        """
        启动定时器。

        :param interval: 定时器的执行间隔时间（单位：秒）。
        :param mark: 定时器的标识符，用于区分不同的定时器（可选）。
        :param once: 如果为 True，定时器只执行一次；否则会重复执行（默认：False）。
        :param timer_ranges: 定时器的执行次数范围（默认：0，表示无限次）。
        :param ranges_stop: 定时器在达到执行次数范围后是否停止（默认：0，表示不停止）。
        """
        self._start(interval, mark, once, timer_ranges, ranges_stop)

    def join(self):
        """
        等待定时器任务完成。

        :return: 返回定时器任务的执行结果。
        """
        return self._join()

    def stop(self):
        """
        停止定时器。

        :return: 返回定时器的停止状态。
        """
        return self._stop()
