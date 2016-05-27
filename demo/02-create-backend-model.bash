#!/bin/bash -ex

HERE=$(cd $(dirname $0);pwd)

etcd_addr=$($HERE/etcd-endpoint.bash)
if [ -z "${etcd_addr}" ]; then
	echo "etcd not ready, try again when it is"
	exit 1
fi

juju add-model backend  # party
juju deploy -m backend wordpress
juju deploy -m backend mysql
juju deploy -m backend $JUJU_REPOSITORY/trusty/http-relay --series trusty
juju set-config -m backend http-relay etcd=${etcd_addr}
juju add-relation -m backend wordpress mysql
juju add-relation -m backend wordpress http-relay:frontend  # relay is a "frontend"

