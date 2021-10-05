"""
使用解释迁移表实现有限状态自动机, 自动机为csdn中state模式里面的第三小节用例:
 - 若状态机在initialize状态收到free请求，则迁移到free状态并执行可用执行器加一动作。
 - 若状态机在free状态收到initialize请求，则迁移到initialize状态并执行可用执行器减一动作。
"""

from abc import ABCMeta, abstractmethod
from typing import List


class HandlerController(metaclass=ABCMeta):
    @abstractmethod
    def add_avail_handler(self):
        pass

    @abstractmethod
    def remove_avail_handler(self):
        pass

    @abstractmethod
    def update_info(self):
        pass


class Action(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


class HandlerMonitor:
    INITIALIZE: int = 0
    FREE: int = 1

    INITIALIZE_REQUEST: int = 0
    FREE_REQUEST: int = 1

    state: int = INITIALIZE
    handler_controller: HandlerController
    transitions: List = []

    class Transition:
        current_state: int
        event: int
        new_state: int
        action: Action

        def __init__(self, current_state: int, event: int, new_event: int, action: Action):
            self.current_state = current_state
            self.event = event
            self.new_state = new_event
            self.action = action

    def __int__(self, controller: HandlerController):
        HandlerMonitor.handler_controller = controller
        self.add_transition(self.INITIALIZE, self.INITIALIZE_REQUEST, self.INITIALIZE, self.update_info())
        self.add_transition(self.INITIALIZE, self.FREE_REQUEST, self.FREE, self.add_handler())
        self.add_transition(self.FREE, self.INITIALIZE_REQUEST, self.INITIALIZE, self.remove_handler())
        self.add_transition(self.FREE, self.FREE, self.FREE, self.update_info())

    def add_transition(self, current_state: int, event: int, new_state: int, action: Action):
        self.transitions.append(self.Transition(current_state, event, new_state, action))

    def add_handler(self) -> Action:
        out_class = self

        class AddHandlerAction(Action):
            def execute(self):
                out_class.do_add_handler()
        return AddHandlerAction()

    def remove_handler(self) -> Action:
        out_class = self

        class RemoveHandlerAction(Action):
            def execute(self):
                out_class.do_remove_handler()
        return RemoveHandlerAction()

    def update_info(self) -> Action:
        out_class = self

        class UpdateInfoAction(Action):
            def execute(self):
                out_class.do_update_info()
        return UpdateInfoAction()

    def do_add_handler(self):
        self.handler_controller.add_avail_handler()

    def do_remove_handler(self):
        self.handler_controller.remove_avail_handler()

    def do_update_info(self):
        self.handler_controller.update_info()

    def event(self, event: int) -> None:
        for i in range(len(self.transitions)):
            transition = self.transitions[i]
            if self.state == transition.current_state and event == transition.event:
                self.state = transition.new_state
                transition.action.execute()
