ifndef JUJU_REPOSITORY
_fail:
$(error JUJU_REPOSITORY is undefined)
endif

all: $(JUJU_REPOSITORY)/trusty/http-relay

$(JUJU_REPOSITORY)/trusty/http-relay: bdist/etcdctl
	LAYER_PATH=$(shell pwd)/layers INTERFACE_PATH=$(shell pwd)/interfaces charm build -s trusty

bdist/etcdctl:
	mkdir -p $(shell dirname $@)
	CURDIR=$$(pwd); TMPDIR=$$(mktemp -d); \
		cd $$TMPDIR; \
		wget https://github.com/coreos/etcd/releases/download/v2.2.3/etcd-v2.2.3-linux-amd64.tar.gz; \
		tar xzvf etcd-v2.2.3-linux-amd64.tar.gz etcd-v2.2.3-linux-amd64/etcdctl; \
		cd $$CURDIR; \
		mv $$TMPDIR/etcd-v2.2.3-linux-amd64/etcdctl $@; \
		rm -rf $$TMPDIR

clean:
	$(RM) -r $(JUJU_REPOSITORY)/trusty/http-relay

bdist-clean:
	$(RM) bdist/etcdctl

.PHONY: all clean bdist-clean
