from flet import Page
from .PilotftState import PilotftState
from .PilotftParams import PilotftParams
from repath import match

class PilotftMiddleware:
    def __init__(self, page: Page, state: PilotftState, params: PilotftParams):
        self.page = page
        self.state = state
        self._params = params
        self.init()

    def init(self):
        self.authenticated = self.page.session.get("user") is not None

    def middleware(self):
        if not self.authenticated and self.page.route not in ["/login"]:
            self.page.route = "/login"

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
