import json
import os
import shutil
from subprocess import check_call, check_output

from charms.reactive import hook, when, when_not, remove_state, set_state
from charms.reactive.helpers import data_changed
from charmhelpers.core import hookenv
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_install


@when_not('etcdctl.installed')
def install_etcdctl():
    shutil.copyfile(os.path.join(hookenv.charm_dir(), 'bdist/etcdctl'), '/usr/bin/etcdctl')
    os.chmod('/usr/bin/etcdctl', 0o755)
    set_state('etcdctl.installed')


@when_not('relay.init')
def init_relays():
    md = hookenv.metadata()
    for role in ('provides', 'requires'):
        for endpoint_name, endpoint_info in md.get(role, {}).items():
            if endpoint_info and endpoint_info.get('relay'):
                create_relay_hooks(endpoint_name, endpoint_info, endpoint_info.get('relay'), role=role)
    set_state('relay.init')


def counterpart_role(role):
    if role == 'provides':
        return 'requires'
    elif role == 'requires':
        return 'provides'
    raise Exception('cannot determine counterpart role for %s' % (role))


def create_relay_hooks(endpoint_name, endpoint_info, relay_name, role=None):
    if not role:
        raise Exception('missing required kwarg "role"')
    context = {
        'endpoint_name': endpoint_name,
        'endpoint_info': endpoint_info,
        'relay_name': relay_name,
        'counterpart': counterpart_role(role),
    }
    render(source='changed.py',
        target=os.path.join(hookenv.charm_dir(), 'hooks', '%s-relation-changed' % (endpoint_name)),
        perms=0o755,
        context=context)
    render(source='departed.py',
        target=os.path.join(hookenv.charm_dir(), 'hooks', '%s-relation-departed' % (endpoint_name)),
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


@when('relay.available')
def poll_remote():
    env = {}
    env.update(os.environ)
    env['ETCDCTL_ENDPOINT'] = hookenv.config().get('etcd')

    md = hookenv.metadata()
    for declared_role in ('provides', 'requires'):
        for endpoint_name, endpoint_info in md.get(declared_role, {}).items():
            if not endpoint_info or not endpoint_info.get('relay'):
                continue
            relay_name = endpoint_info.get('relay')
            relations = hookenv.role_and_interface_to_relations(declared_role, endpoint_info['interface'])
            for relation_name in relations:
                etcd_path = '/%s/%s' % (relay_name, declared_role)
                try:
                    remote_data_json = check_output(['etcdctl', 'get', etcd_path], env=env, universal_newlines=True)
                    remote_data = json.loads(remote_data_json)
                    if data_changed(etcd_path, remote_data):
                        for rid in hookenv.relation_ids(relation_name):
                            hookenv.relation_set(relation_id=rid, **remote_data)
                            hookenv.log('relayed %s to relation %s' % (etcd_path, rid))
                except Exception as e:
                    hookenv.log('failed to relay %s: %s' % (etcd_path, e))
