import os
from drivers.web.framework.entrypoint import get_application


os.environ.setdefault(
    'FRAMEWORK_SETTINGS_MODULE',
    'drivers.web.application.settings'
)
get_application = get_application
