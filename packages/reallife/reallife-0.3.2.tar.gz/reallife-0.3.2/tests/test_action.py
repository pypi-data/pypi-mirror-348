import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest



from reallife.actions.action import KanBanManager,APPIO
from reallife import Date
# from reallife.utils import 

class Test_APPIO():
    def test_sync_calulate(self):
        appio = APPIO()
        appio.sync_calulate()

    def test_sync_notes(self):
        appio = APPIO()
        appio.sync_notes()

    @pytest.mark.skip(reason='#TODO')
    def test_sync_news(self):
        appio = APPIO()
        appio.sync_news(Date().date)


class Test_KanBan():

    def test_sync_ready(self):
        """同步到预备池
        """ 
        kanb = KanBanManager(kanban_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/事件看板.md",
                             pathlib = ["/工程系统级设计/能力级别/grapher/grapher.canvas","/工程系统级设计/能力级别/kanban/kanban.canvas"])
        kanb.sync_ready()

    @pytest.mark.skip(reason='通过')
    def test_sync_order(self):
        """同步到就绪池
        """ 
        kanb = KanBanManager(kanban_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/事件看板.md",
                             pathlib = ["/工程系统级设计/能力级别/grapher/grapher.canvas","/工程系统级设计/能力级别/kanban/kanban.canvas"])
        kanb.sync_order()

    @pytest.mark.skip(reason='通过')
    def test_sync_run(self):
        """同步到执行池
        """ 
        kanb = KanBanManager(kanban_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/事件看板.md",
                             pathlib = ["/工程系统级设计/能力级别/grapher/grapher.canvas","/工程系统级设计/能力级别/kanban/kanban.canvas"])
        kanb.sync_run()

    @pytest.mark.skip(reason='通过')
    def test_sync_run2order(self):
        """从执行池未完成的迁移回就绪池
        """ 
        kanb = KanBanManager(kanban_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/事件看板.md",
                             pathlib = ["/工程系统级设计/能力级别/grapher/grapher.canvas","/工程系统级设计/能力级别/kanban/kanban.canvas"])
        kanb.sync_run2order()

    @pytest.mark.skip(reason='暂时不执行')
    def test_sync_run2over(self):
        """从执行池迁移到完成池
        """ 
        # TODO 将信息融到task中
        kanb = KanBanManager(kanban_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/事件看板.md",
                             pathlib = ["/工程系统级设计/能力级别/grapher/grapher.canvas","/工程系统级设计/能力级别/kanban/kanban.canvas"])
        kanb.sync_run2over(task='')


    @pytest.mark.skip(reason='通过')
    def test_add_tips(self):
        """增加随笔到预备池

        """ 
        kanb = KanBanManager(kanban_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/事件看板.md",
                             pathlib = ["/工程系统级设计/能力级别/grapher/grapher.canvas","/工程系统级设计/能力级别/kanban/kanban.canvas"])
        task = "你好 测试"
        kanb.add_tips(task)

    @pytest.mark.skip(reason='通过')
    def test_sync_weight(self):
        kanb = KanBanManager(kanban_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/事件看板.md",
                             pathlib = ["/工程系统级设计/能力级别/grapher/grapher.canvas","/工程系统级设计/能力级别/kanban/kanban.canvas"])
        kanb.sync_weight(Date().date)


