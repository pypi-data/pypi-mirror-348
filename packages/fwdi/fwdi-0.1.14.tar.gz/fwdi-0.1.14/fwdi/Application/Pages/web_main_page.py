import gradio as gr
from gradio.themes.base import Base
from ...Application.Abstractions.base_web_main_page import BaseWebMainPage
from ...Application.Abstractions.base_web_tabs_panel import BaseWebTabsPanel
from ...Application.Abstractions.base_web_tab_item import BaseWebTabItem
from ...Infrastructure.Web.web_tabs_panel import WebTabsPanel

class WebMainPage(BaseWebMainPage):
    def __init__(self, theme:Base=gr.themes.Glass()):
        self.__panel:BaseWebTabsPanel = WebTabsPanel(theme)
        self.__lst_page:list[BaseWebTabItem] = []

    def add_page(self, item:BaseWebTabItem):
        self.__lst_page.append(item)

    def create(self):
        main_blocks = self.__panel.create_panel(self.__lst_page)
        return main_blocks