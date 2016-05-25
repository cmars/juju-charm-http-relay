from charms.reactive import when, when_not, set_state


@hook('config-changed')
def config_changed():
    conf = hookenv.config()
    for k in ('name', 'etcd'):
        if not conf.get(k):
            hookenv.status_set('error', 'missing required config param "%s"' % (k))
            remove_state('relay.available')
            return
    hookenv.status_set('maintenance', 'configured')
    set_state('relay.available')


@when_not('etcdctl.installed')
def install_etcdctl():
    apt_install(['etcd'])
    check_call(['systemctl', 'disable', 'etcd'])  # debian package is helpful*
    set_state('etcdctl.installed')
