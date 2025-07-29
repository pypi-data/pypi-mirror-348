import gradio as gr
from gradio.themes.base import Base
from ...Application.Abstractions.base_web_tab_item import BaseWebTabItem
from ...Application.Abstractions.base_web_tabs_panel import BaseWebTabsPanel

class WebTabsPanel(BaseWebTabsPanel):
    def __init__(self, theme:Base=gr.themes.Glass()):
        self.__theme:Base = theme
        self.__main_blocks:gr.Blocks = gr.Blocks(theme=self.__theme)
        self.__tabs:gr.Tabs = None
        self.__actual_tabs:dict[str, int] = {}
    
    def create_panel(self, lst_comp:list[BaseWebTabItem])->gr.Blocks:
        with self.__main_blocks:
            if not self.__tabs:
                self.__tabs = gr.Tabs()

            with self.__tabs:
                for index, item in enumerate(lst_comp):
                    item.create_tab(self.__main_blocks, self.__tabs, index)
                    self.__actual_tabs[item.Name] = index

        return self.__main_blocks