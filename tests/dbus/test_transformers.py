import pytest

# TODO: fixture
from pyxsession.config import (
    BaseConfig, AutostartConfig, MenuConfig, MimeConfig, ApplicationsConfig
)
from pyxsession.dbus.transformers import Transformer, MultiTransformer
from pyxsession.dbus.marshmallow.fields import Str


config_loaded = BaseConfig(
    autostart=AutostartConfig(
        directories=['/home/josh/.config/autostart', '/etc/xdg/autostart'],
        environment_name='pyxsession',
        skip_unparsed=False,
        skip_invalid=False
    ),
    menu=MenuConfig(
        filename='/etc/xdg/menus/arch-applications.menu'
    ),
    mime=MimeConfig(
        cache='/usr/share/applications/mimeinfo.cache',
        environment='pyxsession'
    ),
    applications=ApplicationsConfig(
        directories=['/usr/share/applications'],
        skip_unparsed=False,
        skip_invalid=False
    ),
    urls={'https': 'firefox.desktop'}
)

config_dumped = [
    [
        ['/home/josh/.config/autostart', '/etc/xdg/autostart'],
        'pyxsession',
        False,
        False
    ],
    [
        '/etc/xdg/menus/arch-applications.menu'
    ],
    [
        '/usr/share/applications/mimeinfo.cache',
        'pyxsession'
    ],
    [
        ['/usr/share/applications'],
        False,
        False
    ],
    {'https': 'firefox.desktop'}
]

config_signature = '((asvvv)(v)(vv)(asvv)a{ss})'


@pytest.mark.parametrize('type_,dumped,loaded,sig', [
    (Str(), 'hello', 'hello', 's'),
    (BaseConfig, config_dumped, config_loaded, config_signature)
])
def test_transformer(type_, dumped, loaded, sig):
    xform = Transformer(type_)
    assert xform.signature() == sig
    assert xform.dump(loaded) == dumped
    assert xform.load(dumped) == loaded
