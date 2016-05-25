ifndef JUJU_REPOSITORY
_fail:
$(error JUJU_REPOSITORY is undefined)
endif

all: $(JUJU_REPOSITORY)/trusty/http-relay

$(JUJU_REPOSITORY)/trusty/http-relay:
	LAYER_PATH=$(shell pwd)/layers INTERFACE_PATH=$(shell pwd)/interfaces charm build -s trusty

clean:
	$(RM) -r $(JUJU_REPOSITORY)/trusty/http-relay

.PHONY: all clean
