from os import path
from DService.web.data_service_urls import urls_pattern as url_handlers

settings = {
    'debug': True,
    'template_path': path.join(path.dirname(__file__), 'template'),
    'static_path': path.join(path.dirname(__file__), 'static')
}

