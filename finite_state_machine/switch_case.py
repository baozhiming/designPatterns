"""
使用switch/case语句实现有限状态自动机, 自动机为csdn中state模式里面的第三小节用例:
 - 若状态机在initialize状态收到free请求，则迁移到free状态并执行可用执行器加一动作。
 - 若状态机在free状态收到initialize请求，则迁移到initialize状态并执行可用执行器减一动作。
因为python中没有实现switch/case语句，所以使用if else语句代替
"""
from abc import ABCMeta, abstractmethod


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


class HandlerMonitor:
    INITIALIZE: int = 0
    FREE: int = 1

    INITIALIZE_REQUEST: int = 0
    FREE_REQUEST: int = 1

    state: int = INITIALIZE
    handler_controller: HandlerController

    def __int__(self, controller: HandlerController):
        HandlerMonitor.handler_controller = controller

    def event(self, event: int) -> None:
        if self.state == self.INITIALIZE:
            if event == self.INITIALIZE_REQUEST:
                self.handler_controller.update_info()
            elif event == self.FREE_REQUEST:
                self.state = self.FREE
                self.handler_controller.add_avail_handler()
        elif self.state == self.FREE:
            if event == self.INITIALIZE_REQUEST:
                self.state = self.INITIALIZE
                self.handler_controller.remove_avail_handler()
            elif event == self.FREE_REQUEST:
                self.handler_controller.update_info()
