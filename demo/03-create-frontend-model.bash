#!/bin/bash -ex

HERE=$(cd $(dirname $0);pwd)

etcd_addr=$($HERE/etcd-endpoint.bash)
if [ -z "${etcd_addr}" ]; then
	echo "etcd not ready, try again when it is"
	exit 1
fi

juju add-model frontend  # business
juju deploy -m frontend haproxy
juju deploy -m frontend $JUJU_REPOSITORY/xenial/http-relay --series xenial
juju set-config -m frontend http-relay etcd=${etcd_addr}
juju add-relation -m frontend haproxy http-relay:backend  # relay is a "backend"
