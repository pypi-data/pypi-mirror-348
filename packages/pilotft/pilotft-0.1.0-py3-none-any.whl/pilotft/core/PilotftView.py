from flet import Page, View
from .PilotftState import PilotftState
from .PilotftParams import PilotftParams
from typing import Optional

class PilotftView:
    def __init__(
            self, 
            page: Page, 
            state: Optional[PilotftState] = None, 
            params: Optional[PilotftParams] = None
        ):
        self.page = page
        self.state = state
        self.params = params
        self.debug = False
        self.error = ""

    def build(self) -> View:
        raise NotImplementedError("You must implement the build () method.")

    def onBuildComplete(self):
        ...
