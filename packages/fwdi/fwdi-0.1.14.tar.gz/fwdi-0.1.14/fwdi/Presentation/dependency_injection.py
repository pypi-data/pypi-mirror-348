#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from .Pages.web_service_setting_panel import WebServiceSettingPanel
from .Pages.rights_management_panel import RightsManagementPanel
from ..Application.Pages.web_main_page import WebMainPage
from ..Presentation.Web.session_manager import SessionManager
from ..Application.Abstractions.base_http_auth import BaseHttpAuth
from ..Presentation.DefaultControllers.http_auth import HttpAuthFWDI
from ..Presentation.Web.default_page import DefaultPage
from ..WebApp.web_application import WebApplication
from .DefaultControllers.home_controller import Controller
from .DefaultControllers.token_controller import TokenController
from .DefaultControllers.health_checks_controller import HealthChecksController


class DependencyInjection():
    from ..Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI

    def AddEndpoints(app:WebApplication)->None:
        #------------- HOME ENDPOINTS -----------------------------
        app.map_get(path="/home", endpoint=Controller().index)
        
        #-------------/HOME ENDPOINTS -----------------------------
        app.map_post(path='/token', endpoint=TokenController.post)

        #-------------/WEB PAGES ENDPOINTS-------------------------
        DependencyInjection.AddWebPages(app)
    
    def AddWebPages(app:WebApplication):
        default_config_services = WebMainPage()
        default_config_services.add_page(WebServiceSettingPanel("Конфигурация сервиса"))
        default_config_services.add_page(RightsManagementPanel("Управление правами"))
        
        app.add_web_page(default_config_services.create(), '/config', is_auth=True)

        default_page = DefaultPage().create_panel()
        app.add_web_page(default_page, path="/default")

    def AddHealthChecks(app:WebApplication)->None:
        app.map_get(path="/health_checks", endpoint=HealthChecksController().index)

    def AddPresentation(services:BaseServiceCollectionFWDI)->None:
        services.AddTransient(BaseHttpAuth, HttpAuthFWDI)
        services.AddSingleton(SessionManager)
        services.AddSingleton(DefaultPage)
        services.AddTransient(WebServiceSettingPanel)
        services.AddTransient(RightsManagementPanel)