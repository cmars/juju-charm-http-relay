from charms.reactive import when, when_not, set_state


@hook('config-changed')
def config_changed():
    conf = hookenv.config()
    if not conf.get('name'):
        hookenv.status_set('error', 'missing required config param "name"')
        remove_state('relay.available')
        return
    if not conf.get('etcd'):
        hookenv.status_set('error', 'missing required config param "etcd"')
        remove_state('relay.available')
        return
    hookenv.status_set('maintenance', 'configured')
    set_state('relay.available')


@when_not('http-relay.installed')
def install_http_relay():
    # Do your setup here.
    #
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #
    set_state('http-relay.installed')
