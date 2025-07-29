import gradio as gr
from abc import ABC, abstractmethod

class BaseWebTabItem(ABC):
    def __init__(self, name:str):
        from ...Presentation.Web.session_manager import SessionManager
        super().__init__()
        self.Name:str = name
        self._session = SessionManager()

    @abstractmethod
    def create_tab(self, parent_blocks:gr.Blocks, parent:gr.Tabs, tab_id:int):
        ...