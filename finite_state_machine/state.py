"""
使用state模式实现有限自动状态机
"""
from abc import ABCMeta, abstractmethod


class HandlerController:
    def add_avail_handler(self):
        print("增加可用handler")
        pass

    def remove_avail_handler(self):
        print("移除可用handler")
        pass

    def update_info(self):
        print("更新信息")
        pass


class HandlerState(metaclass=ABCMeta):
    @abstractmethod
    def initialize_request(self, h):
        pass

    @abstractmethod
    def free_request(self, h):
        pass


class HandlerInitializeState(HandlerState):
    def initialize_request(self, h):
        h.update_info()

    def free_request(self, h):
        h.set_free_state()
        h.add_handler()


class HandlerFreeState(HandlerState):
    def initialize_request(self, h):
        h.set_initialize_state()
        h.remove_handler()

    def free_request(self, h):
        h.update_info()


class Handler:
    initialize_state = HandlerInitializeState()
    free_state = HandlerFreeState()

    state = initialize_state
    controller: HandlerController

    def __init__(self, controller: HandlerController):
        self.controller = controller

    def free_request(self):
        self.state.free_request(self)

    def initialize_request(self):
        self.state.initialize_request(self)

    def set_initialize_state(self):
        self.state = self.initialize_state

    def set_free_state(self):
        self.state = self.free_state

    def add_handler(self):
        self.controller.add_avail_handler()

    def remove_handler(self):
        self.controller.remove_avail_handler()

    def update_info(self):
        self.controller.update_info()

    def is_initialize_state(self):
        return self.state == self.initialize_state

    def is_free_state(self):
        return self.state == self.free_state


a = Handler(HandlerController())
a.initialize_request()
re = a.is_initialize_state()
assert re is True
a.free_request()
re = a.is_free_state()
assert re is True
a.free_request()
re = a.is_free_state()
assert re is True
a.initialize_request()
re = a.is_initialize_state()
assert re is True
