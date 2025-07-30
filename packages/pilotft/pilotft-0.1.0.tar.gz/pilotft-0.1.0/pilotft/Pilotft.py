from typing import Optional
from repath import match

import traceback
import flet as ft
# The components of Pilotft
from .core.PilotftView import PilotftView   
from .core.PilotftState import PilotftState
from .core.PilotftParams import PilotftParams
from .core.PilotftMiddleware import PilotftMiddleware
# The views
from .views.NotFoundView import NotFoundView
from .views.InternalErrorView import InternalErrorView



def route(path: str, view: type[PilotftView]) -> dict:
    return {"route": path, "view": view}

def route_str(route):
    return str(route.route) if not isinstance(route, str) else route

class Pilotft:
    def __init__(
        self,
        page: ft.Page,
        routes: list[dict],
        state: Optional[PilotftState] = None,
        middleware_cls: Optional[type[PilotftMiddleware]] = None,
        init_route: Optional[str] = None,
        not_found_view: type[PilotftView] = NotFoundView,
        internal_error_view: type[PilotftView] = InternalErrorView,
        debug: bool = True,
    ):
        self.__debug = debug
        self.__page = page
        self.__middleware_cls = middleware_cls
        self.__routes = routes
        self.__params = PilotftParams()
        self.__not_found_view = not_found_view
        self.__internal_error_view = internal_error_view
        self.__state = state or PilotftState(page)

        self.__page.on_route_change = self.route_event_handler
        if self.__page.views:
            self.__page.views.clear()

        self.__page.go(init_route or self.__page.route)

    def route_event_handler(self, route):
        try:
            route_str_value = route_str(route)
            route_match = None

            for r in self.__routes:
                route_match = match(r["route"], route_str_value)
                if route_match:
                    self.__params = PilotftParams(route_match.groupdict())

                    if self.__middleware_cls:
                        middleware = self.__middleware_cls(self.__page, self.__state, self.__params)
                        middleware.middleware()

                    if self.__page.route != route_str_value:
                        self.__page.go(self.__page.route)
                        return

                    view = r["view"](page=self.__page, state=self.__state, params=self.__params)
                    self.__page.views.clear()
                    self.__page.views.append(view.build())
                    self.__page.update()
                    view.onBuildComplete()
                    return

            view = self.__not_found_view(self.__page, self.__state, PilotftParams())
            view.debug = self.__debug
            self.__page.views.clear()
            self.__page.views.append(view.build())
            self.__page.update()
            view.onBuildComplete()

        except Exception:
            view = self.__internal_error_view(self.__page, self.__state, PilotftParams())
            view.debug = self.__debug
            if hasattr(view, "error"):
                view.error = traceback.format_exc(110)
            self.__page.views.clear()
            self.__page.views.append(view.build())
            self.__page.update()
            view.onBuildComplete()

