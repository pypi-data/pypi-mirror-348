# core/base_state.py
from flet import Page
from typing import Callable

class PilotState:
    def __init__(self, page: Page):
        self.page = page

    def update(self):
        self.page.update()

    async def update_async(self):
        self.page.update()

    def go(self, route):
        self.page.go(route)

    def pop_go(self, route):
        if len(self.page.views) >= 1:
            self.page.views.pop()
            self.page.go(route)

    def pop_all_go(self, route):
        self.page.views.clear()
        self.page.go(route)

    def back(self, *args, **kwargs):
        if len(self.page.views) > 1:
            pre_r = self.page.views[-2].route
            if pre_r is not None:
                self.page.views.pop()
                self.page.views.pop()
                self.page.go(pre_r)
            else:
                raise ValueError("Cannot go back because the previous route is None")

    def inject_in_state(self, func: Callable):
        setattr(self, func.__name__, func)
