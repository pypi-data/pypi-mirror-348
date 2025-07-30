import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import re
import pytest

from reallife.main import morning,push_task

from reallife.main import rest,evening

from reallife.main import start_work, finish_work

class Test_Morning():
    # @pytest.mark.skip(reason='通过')
    def test_morning(self):
        result = morning("2025-05-11")
        print(result)
        push_task(task=result,date = "2025-05-11")

    @pytest.mark.skip(reason='通过')
    def start_work(self):
        result = start_work("2025-05-11")
        print(result)
        push_task(task=result,date = "2025-05-11")

    @pytest.mark.skip(reason='通过')
    def finish_work(self):
        result = finish_work("2025-05-11")
        print(result)
        push_task(task=result,date = "2025-05-11")

    def test_evening(self):
        result = evening("2025-05-11")
        print(result)
        push_task(task=result,date = "2025-05-11")

    def test_rest(self):
        result = rest("2025-05-11")
        print(result)
        push_task(task=result,date = "2025-05-11")



