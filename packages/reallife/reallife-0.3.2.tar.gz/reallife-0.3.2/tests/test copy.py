from abc import ABC, abstractmethod

class TaskExecutionStrategy(ABC):
    @abstractmethod
    def execute(self, task_context):
        pass

class PromptTaskExecutionStrategy(TaskExecutionStrategy):
    def execute(self, task_context):
        return task_context._state.handle(task_context)

class ScriptTaskExecutionStrategy(TaskExecutionStrategy):
    def execute(self, task_context):
        try:
            if task_context.name == '汇总到预备池':
                pass
            elif task_context.name == '同步到就绪池':
                pass
            elif task_context.name == '同步到执行池':
                pass
            elif task_context.name == '同步到日历':
                pass
            elif task_context.name == '同步到备忘录':
                pass
            elif task_context.name == '同步体重':
                pass

            if task_context.script_code:
                exec(task_context.script_code)
                return f"脚本任务 '{task_context.name}' 执行完毕。"
            else:
                return f"脚本任务 '{task_context.name}' 没有提供脚本代码。"
        except Exception as e:
            return f"脚本任务 '{task_context.name}' 执行失败：{e}"

class PersonTaskExecutionStrategy(TaskExecutionStrategy):
    def execute(self, task_context):
        try:
            task_type = judge_type(task_context.name)
            if task_type == "代码与练习":
                edit_coder(task)
            elif task_type == "实验与学习":
                test_and_study(task)
            elif task_type == "整理与优化":
                clean_and_update(task)
            elif task_type == "设计":
                design(task)
            elif task_type == "开会与对齐":
                meeting_and_talk(task)
            else:
                meeting_and_talk(task)
            task_result = Display.display_dialog("判断", f"任务是否完成: ", buttons='"complete","blockage"', button_cancel=True)
            if task_result == 'complete':
                pass
            elif task_result == 'blockage':
                pass
            elif task_result == 'no complete':
                pass
            if task_context.script_code:
                exec(task_context.script_code)
                return f"脚本任务 '{task_context.name}' 执行完毕。"
            else:
                return f"脚本任务 '{task_context.name}' 没有提供脚本代码。"
        except Exception as e:
            return f"脚本任务 '{task_context.name}' 执行失败：{e}"

class TaskState(ABC):
    @abstractmethod
    def handle(self, task_context):
        pass

    @abstractmethod
    def complete(self, task_context):
        pass

    @abstractmethod
    def get_status(self):
        pass

class TodoState(TaskState):
    def handle(self, task_context):
        return f"请开始任务：{task_context.name}"

    def complete(self, task_context):
        if isinstance(task_context.execution_strategy, ScriptTaskExecutionStrategy) or \
           isinstance(task_context.execution_strategy, PersonTaskExecutionStrategy):
            execution_result = task_context.execution_strategy.execute(task_context)
        task_context.set_state(InProgressState())
        return f"任务 '{task_context.name}' 状态更新为：进行中"

    def get_status(self):
        return "待办"

class InProgressState(TaskState):
    def handle(self, task_context):
        return f"任务 '{task_context.name}' 正在进行中。请确认是否已完成？"

    def complete(self, task_context):
        task_context.set_state(CompletedState())
        return f"任务 '{task_context.name}' 已标记为：完成"

    def get_status(self):
        return "进行中"

class CompletedState(TaskState):
    def handle(self, task_context):
        return f"任务 '{task_context.name}' 已完成。"

    def complete(self, task_context):
        return f"任务 '{task_context.name}' 已处于完成状态，无需重复操作。"

    def get_status(self):
        return "完成"

class Task:
    def __init__(self, name: str, execution_strategy: TaskExecutionStrategy, script_code: str = None):
        self.name = name
        self._state = TodoState()
        self.execution_strategy = execution_strategy
        self.script_code = script_code

    def set_state(self, state: TaskState):
        self._state = state

    def request(self):
        return self._state.handle(self)

    def complete_task(self):
        return self._state.complete(self)

    def get_status(self):
        return self._state.get_status()

class TaskManager:
    def __init__(self):
        self._tasks_order = []
        self._tasks = {}

    def clear(self):
        self._tasks_order = []
        self._tasks = {}

    def add_task(self, task_name: str, task_type='prompt', script_code: str = None):
        if task_name in self._tasks:
            return f"任务 '{task_name}' 已存在。"
        if task_type == 'prompt':
            strategy = PromptTaskExecutionStrategy()
        elif task_type == 'script':
            strategy = ScriptTaskExecutionStrategy()
        elif task_type == 'person':
            strategy = PersonTaskExecutionStrategy()
        else:
            strategy = PromptTaskExecutionStrategy()
        new_task = Task(name=task_name, execution_strategy=strategy, script_code=script_code)
        self._tasks_order.append(task_name)
        self._tasks[task_name] = new_task
        return f"任务 '{task_name}' 已添加。"

    def get_task(self, task_name: str) -> Task | None:
        return self._tasks.get(task_name)

    def get_current_sequential_task(self) -> Task | None:
        for task_name in self._tasks_order:
            task = self._tasks.get(task_name)
            if task and not isinstance(task._state, CompletedState):
                return task
        return None

    def complete_current_task(self):
        current_task = self.get_current_sequential_task()
        if current_task:
            return current_task.complete_task()
        else:
            return "没有当前需要完成的任务。"

    def get_task_status(self, task_name: str):
        task = self.get_task(task_name)
        if task:
            return f"任务 '{task_name}' 的状态是：{task.get_status()}"
        else:
            return f"任务 '{task_name}' 不存在。"

    def get_task_list(self):
        return [(name, self.get_task_status(name)) for name in self._tasks_order]

task_manager = TaskManager()

class WorkdayFacade:
    def __init__(self):
        pass

    def clear(self):
        task_manager.clear()

    def _morning_tasks(self) -> str:
        task_manager.add_task("记录灵感")
        task_manager.add_task("记录体重")
        task_manager.add_task("跑步")
        task_manager.add_task("记录吃了什么")
        task_manager.add_task("洗漱护肤")
        task_manager.add_task("收拾家与锻炼")
        return "清晨任务已添加"

    def _start_work_tasks(self) -> str:
        task_manager.add_task("上班打卡", task_type="prompt")
        task_manager.add_task("同步体重", task_type="script", script_code=None)
        task_manager.add_task("汇总到预备池", task_type="script", script_code=None)
        task_manager.add_task("同步到就绪池", task_type="script", script_code=None)
        task_manager.add_task("调整优先级", task_type="prompt")
        task_manager.add_task("同步到执行池", task_type="script", script_code=None)
        task_manager.add_task("同步到日历", task_type="script", script_code=None)
        task_manager.add_task("同步到备忘录", task_type="script", script_code=None)
        task_manager.add_task("倒水", task_type="prompt")
        task_manager.add_task("写下灵感", task_type="prompt")
        task_manager.add_task("跟进阻塞池", task_type="prompt")
        return "开工任务已添加"

    def _finish_work_tasks(self) -> str:
        task_manager.add_task("同步体重 (收工)", task_type="script", script_code=None)
        task_manager.add_task("同步到备忘录", task_type="script", script_code=None)
        task_manager.add_task("检查和收集咨询", task_type="prompt")
        task_manager.add_task("检查是否仍在禅模式", task_type="prompt")
        task_manager.add_task("检测git提交", task_type="prompt")
        task_manager.add_task("下班打卡", task_type="prompt")
        task_manager.add_task("倒水", task_type="prompt")
        return "收工任务已添加"

    def _evening_tasks(self) -> str:
        task_manager.add_task("整理家里和猫猫", task_type="prompt")
        task_manager.add_task("晚上洗漱,刷牙,护肤", task_type="prompt")
        task_manager.add_task("锻炼", task_type="prompt")
        task_manager.add_task("睡觉", task_type="prompt")
        return "晚间任务已添加"
    
    def _rest(self) -> str:
        task_manager.add_task("周末", task_type="prompt")
        task_manager.add_task("查看备忘录", task_type="prompt")
        task_manager.add_task("锻炼", task_type="prompt")
        task_manager.add_task("玩游戏", task_type="prompt")
        return "晚间任务已添加"
    
    def get_current_task_info(self):
        current_task = task_manager.get_current_sequential_task()
        if current_task:
            prompt = current_task.request()
            return f"当前任务：{current_task.name} ({current_task.get_status()})\n提示: {prompt}"
        else:
            return "所有任务已完成！"

    def complete_current_task(self) -> str:
        return task_manager.complete_current_task()

    def get_all_tasks_status(self):
        return task_manager.get_task_list()

def receive():
    return workday_facade.get_current_task_info()

def complete():
    complete_message = workday_facade.complete_current_task()
    next_task_info = receive()
    return next_task_info

def list_tasks():
    tasks_list = workday_facade.get_all_tasks_status()
    if not tasks_list:
        return
    for name, status in tasks_list:
        print(f"- {name}: {status}")
    print("---------------------")

import sys

workday_facade = WorkdayFacade()

def receive_1():
    print("\n执行动作 1: receive (获取当前任务信息和提示)")
    print(receive())

def complete_1():
    print("\n执行动作 2: complete (完成当前任务)")
    print(complete())

def show_help():
    print("\n可用动作：")
    print("  1: 获取当前任务信息和提示 (不触发脚本执行)")
    print("  2: 完成当前任务 (待办脚本任务会在此处执行，然后显示下一个任务)")
    print("  3: 列出所有任务状态")
    print("  help: 显示帮助信息")
    print("  quit/exit: 退出程序")

def main():
    print("欢迎使用简单的 CLI 工具！")
    show_help()
    while True:
        print('\n-----------------------------')
        command = input("请输入动作名称 (或 'help', 'quit'): ").strip().lower()
        if command == '1':
            receive_1()
        elif command == '2':
            complete_1()
        elif command == '3':
            list_tasks()
        elif command == '3':
            list_tasks()
        elif command == '41':
            workday_facade._morning_tasks()
        elif command == '42':
            workday_facade._start_work_tasks()
        elif command == '43':
            lists = ['任务1','任务2','任务3','任务4']
            for i in lists:
                task_manager.add_task(i,task_type='person')
        elif command == '44':
            workday_facade._finish_work_tasks()
        elif command == '45':
            workday_facade._evening_tasks()
        elif command == '51':
            workday_facade._rest()
        elif command == '0':
            workday_facade.clear()
        elif command == 'help':
            show_help()
        elif command in ['quit', 'exit']:
            print("退出程序。")
            break
        else:
            print(f"未知命令: {command}")
            show_help()

if __name__ == "__main__":
    main()
