ifndef JUJU_REPOSITORY
_fail:
$(error JUJU_REPOSITORY is undefined)
endif

all: $(JUJU_REPOSITORY)/xenial/http-relay

$(JUJU_REPOSITORY)/xenial/http-relay:
	LAYER_PATH=$(shell pwd)/layers INTERFACE_PATH=$(shell pwd)/interfaces charm build -s xenial

clean:
	$(RM) -r $(JUJU_REPOSITORY)/xenial/http-relay

.PHONY: all clean
