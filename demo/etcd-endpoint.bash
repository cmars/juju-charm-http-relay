#!/bin/bash -e

juju status -m etcd --format json | \
	jq -r '.services.etcd.units|to_entries|.[].value|.["public-address"]+":"+.["open-ports"][0]' | \
	sed 's/\/tcp$//' | xargs | sed 's/ /,/g'
