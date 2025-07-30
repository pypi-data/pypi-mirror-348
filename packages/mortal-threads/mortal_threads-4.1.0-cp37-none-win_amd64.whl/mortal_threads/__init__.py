#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 17:23
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .threads_main import MortalThreadsMain


class MortalThreads(MortalThreadsMain):
    """
    MortalThreads 类继承自 MortalThreadsMain，用于管理多线程任务的执行。
    该类提供了多种方法来控制线程的启动、停止、状态查询等操作。
    """

    def __init__(self, func, max_workers=None, maximum=False, logfile=False, logger=False, reserve=True, duration=None):
        """
        初始化 MortalThreads 实例。

        :param func: 线程执行的目标函数。
        :param max_workers: 最大线程数，默认为 None。
        :param maximum: 是否启用最大线程数限制，默认为 False。
        :param logfile: 是否将日志输出到文件，默认为 False。
        :param logger: 是否启用日志记录，默认为 False。
        :param reserve: 是否保留线程执行结果，默认为 True。
        :param duration: 线程执行的最大持续时间，默认为 None。
        """
        super().__init__(func, max_workers, maximum, logfile, logger, reserve, duration)

    def send(self, thread_name: str = None, **kwargs):
        """
        发送一个任务到线程池中执行。

        :param thread_name: 线程名称，默认为 None。
        :param kwargs: 传递给目标函数的参数。
        :return: 任务发送结果。
        """
        return self._send(thread_name, **kwargs)

    def send_list(self, thread_list):
        """
        发送多个任务到线程池中执行。

        :param thread_list: 任务列表，每个任务为一个字典，包含线程名称和参数。
        :return: 任务发送结果。
        """
        return self._send_list(thread_list)

    def join(self, break_result="mortal_break"):
        """
        等待所有线程执行完成。

        :param break_result: 线程中断时的返回值，默认为 "mortal_break"。
        :return: 所有线程的执行结果。
        """
        return self._join(break_result)

    def join_property(self, break_result="mortal_break", interval=5):
        """
        等待所有线程执行完成，并定期检查线程状态。

        :param break_result: 线程中断时的返回值，默认为 "mortal_break"。
        :param interval: 检查线程状态的间隔时间，默认为 5 秒。
        :return: 所有线程的执行结果。
        """
        return self._join_property(break_result, interval)

    def stop(self, thread_name):
        """
        停止指定线程的执行。

        :param thread_name: 要停止的线程名称。
        :return: 停止操作的结果。
        """
        return self._stop(thread_name)

    def stop_all(self):
        """
        停止所有线程的执行。

        :return: 停止操作的结果。
        """
        return self._stop_all()

    def clear_queue(self):
        """
        清空任务队列。

        :return: 清空操作的结果。
        """
        return self._clear_queue()

    def clear_record(self):
        """
        清空线程执行记录。

        :return: 清空操作的结果。
        """
        return self._clear_record()

    def close(self):
        """
        关闭线程池，停止所有线程并释放资源。

        :return: 关闭操作的结果。
        """
        return self._close()

    def done(self):
        """
        检查所有线程是否已完成执行。

        :return: 如果所有线程已完成，返回 True；否则返回 False。
        """
        return self._done()

    def get_qsize(self):
        """
        获取任务队列中的任务数量。

        :return: 任务队列中的任务数量。
        """
        return self._get_qsize()

    def get_status(self, thread_name):
        """
        获取指定线程的状态。

        :param thread_name: 线程名称。
        :return: 线程的状态。
        """
        return self._get_status(thread_name)

    def get_all_status(self):
        """
        获取所有线程的状态。

        :return: 所有线程的状态。
        """
        return self._get_all_status()

    def get_run_status(self):
        """
        获取线程池的运行状态。

        :return: 线程池的运行状态。
        """
        return self._get_run_status()

    def get_result(self, thread_name):
        """
        获取指定线程的执行结果。

        :param thread_name: 线程名称。
        :return: 线程的执行结果。
        """
        return self._get_result(thread_name)

    def get_all_result(self):
        """
        获取所有线程的执行结果。

        :return: 所有线程的执行结果。
        """
        return self._get_all_result()

    def get_failed_result(self):
        """
        获取所有失败线程的执行结果。

        :return: 所有失败线程的执行结果。
        """
        return self._get_failed_result()

    def get_failed(self):
        """
        获取所有失败的线程。

        :return: 所有失败的线程。
        """
        return self._get_failed()

    def rerun_failed(self):
        """
        重新执行所有失败的线程。

        :return: 重新执行操作的结果。
        """
        return self._rerun_failed()

    def set_max_workers(self, workers_number=None):
        """
        设置线程池的最大线程数。

        :param workers_number: 最大线程数，默认为 None。
        :return: 设置操作的结果。
        """
        return self._set_max_workers(workers_number)

    def is_close(self):
        """
        检查线程池是否已关闭。

        :return: 如果线程池已关闭，返回 True；否则返回 False。
        """
        return self._is_close()

    def is_run(self):
        """
        检查线程池是否正在运行。

        :return: 如果线程池正在运行，返回 True；否则返回 False。
        """
        return self._is_run()
