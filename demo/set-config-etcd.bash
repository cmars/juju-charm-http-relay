#!/bin/bash -ex

HERE=$(cd $(dirname $0);pwd)

etcd_addr=$($HERE/etcd-endpoint.bash)
if [ -z "${etcd_addr}" ]; then
	echo "etcd not ready, try again when it is"
	exit 1
fi

juju set-config -m backend http-relay etcd=${etcd_addr}
juju set-config -m frontend http-relay etcd=${etcd_addr}
