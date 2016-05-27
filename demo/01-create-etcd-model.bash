#!/bin/bash -ex

juju add-model etcd
juju deploy -n 3 etcd
