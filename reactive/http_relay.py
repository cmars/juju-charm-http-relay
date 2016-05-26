from subprocess import check_call

from charms.reactive import hook, when, when_not, remove_state, set_state
from charmhelpers.core import hookenv
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_install


@when_not('etcdctl.installed')
def install_etcdctl():
    apt_install(['etcd'])
    check_call(['systemctl', 'disable', 'etcd'])  # debian package is helpful*
    set_state('etcdctl.installed')


@when_not('relay.init')
def init_relays():
    md = hookenv.metadata()
    for side in ('provides', 'requires'):
        for endpoint_name, endpoint in md.get(side, {}).items():
            if endpoint and endpoint.get('relay'):
                create_relay_hooks(endpoint, endpoint.get('relay'), side=side)
    set_state('relay.init')


def create_relay_hooks(endpoint, relay_name, side=None):
    if not side:
        raise Exception('missing required kwarg 'side')
    context = {
        'endpoint': endpoint,
        'relay_name': relay_name,
        'side': 'side',
    })
    render(source='changed.py',
        target=os.path.join(hookenv.charm_dir(), 'hooks', '%s-relation-changed'),
        perms=0o755,
        context=context)
    render(source='departed.py',
        target=os.path.join(hookenv.charm_dir(), 'hooks', '%s-relation-departed'),
        perms=0o755,
        context=context)


@hook('config-changed')
def config_changed():
    conf = hookenv.config()
    if not conf.get('etcd'):
       hookenv.status_set('error', 'missing required config param "etcd"')
       remove_state('relay.available')
       return
    hookenv.status_set('maintenance', 'configured')
    set_state('relay.available')
