import os
from typing import Protocol
from drivers.web.framework import settings

class ClassResolver(Protocol):
    def __getitem__(self, item):
        pass


def get_application(di: ClassResolver):
    module_path = os.getenv('FRAMEWORK_SETTINGS_MODULE')
    settings_app = __import__(module_path)
    settings.app_settings = settings_app