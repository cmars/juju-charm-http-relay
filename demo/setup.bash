#!/bin/bash -ex

HERE=$(cd $(dirname $0);pwd)

make -C ${HERE}/.. clean all

${HERE}/00-bootstrap.bash
${HERE}/01-create-etcd-model.bash
${HERE}/02-create-backend-model.bash
${HERE}/03-create-frontend-model.bash

