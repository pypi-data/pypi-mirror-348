import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest

from reallife.scripts.aifunc import give_a_task_time,generate_schedule,judge_type
from reallife.scripts.applescript import Notes, Reminder, Calulate, Display, ShortCut
from reallife.scripts.pypeteer import *
from reallife import Date

import time

class Test_Applescript():

    def test_shortcut(self):
        ShortCut.run_shortcut("预备")
        wode = input()

    def test_display(self):
        Display.display_dialog(1,2,buttons='"OK"',)
        Display.display_dialog(1,3,buttons='"OK","voer"',)
        Display.multiple_selection_boxes(options=['22','33','44'])

    def test_Calulate(self):
        Calulate.update(start_date= "2025年5月12日8:00",
                        end_date = "2025年5月12日9:00",
                        event_name = "会议")
        time.sleep(5)
        Calulate.delete("会议")


class Test_APPIO():

    @pytest.mark.skip(reason='#TODO')
    def test_sync_news(self):
        appio = APPIO()
        appio.sync_news(Date().date)

    @pytest.mark.skip(reason='#TODO')
    def test_sync_calulate(self):
        appio = APPIO()
        appio.sync_calulate()

    @pytest.mark.skip(reason='通过')
    def test_sync_notes(self):
        appio = APPIO()
        appio.sync_notes()


