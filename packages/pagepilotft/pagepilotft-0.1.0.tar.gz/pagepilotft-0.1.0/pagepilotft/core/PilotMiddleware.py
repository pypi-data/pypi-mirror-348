# core/middleware.py
from flet import Page
from .PilotState import PilotState
from .PilotParams import PilotParams
from repath import match

class PilotMiddleware:
    def __init__(self, page: Page, state: PilotState, params: PilotParams):
        self.page = page
        self.state = state
        self._params = params
        self.init()

    def init(self):
        ...

    def middleware(self):
        ...

    def get_param(self, var: str):
        return self._params.get(var)

    def get_all_param(self):
        return self._params.get_all()

    def get_current_route(self):
        return self.page.route

    def redirect_route(self, route: str):
        self.page.route = route

    def is_route_match(self, route: str) -> bool:
        return match(route, self.page.route) is not None

    def is_route_not_matched(self, route: str) -> bool:
        return not self.is_route_match(route)
