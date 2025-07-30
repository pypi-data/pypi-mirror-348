# core/base_view.py
from flet import Page, View
from .PilotState import PilotState
from .PilotParams import PilotParams

class PilotView:
    def __init__(self, page: Page, state: PilotState, params: PilotParams):
        self.page = page
        self.state = state
        self.params = params
        self.debug = False
        self.error = ""

    def build(self) -> View:
        raise NotImplementedError("You must implement the build () method.")

    def onBuildComplete(self):
        ...
