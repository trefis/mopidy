from __future__ import unicode_literals

import os

import mopidy
from mopidy import exceptions, ext
from mopidy.utils import config


class Extension(ext.Extension):

    dist_name = 'Mopidy-MPRIS'
    ext_name = 'mpris'
    version = mopidy.__version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return open(conf_file).read()

    def get_config_schema(self):
        schema = config.ExtensionConfigSchema()
        schema['desktop_file'] = config.Path()
        return schema

    def validate_environment(self):
        if 'DISPLAY' not in os.environ:
            raise exceptions.ExtensionError(
                'An X11 $DISPLAY is needed to use D-Bus')

        try:
            import dbus  # noqa
        except ImportError as e:
            raise exceptions.ExtensionError('dbus library not found', e)

    def get_frontend_classes(self):
        from .actor import MprisFrontend
        return [MprisFrontend]
