#!/usr/bin/env python3

import json
import os
import sys
from subprocess import check_call

sys.path.append('lib')

from charmhelpers.core import hookenv


if __name__ == '__main__':
    local_data = hookenv.relation_get()
    env = {}
    env.update(os.environ)
    env['ETCDCTL_ENDPOINT'] = hookenv.config().get('etcd')
    check_call(['etcdctl', 'set', '/{{ relay_name }}/{{ side }}', json.dumps(local_data)], env=env)
