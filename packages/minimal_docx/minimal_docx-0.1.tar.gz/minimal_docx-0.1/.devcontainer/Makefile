.SUFFIXES:
MAKEFLAGS += --no-builtin-rules

.PHONY: devcontainer devcontainer/build devcontainer/up devcontainer/down
devcontainer: tmp/devcontainer.cid

devcontainer/build:
	npx -- @devcontainers/cli build --workspace-folder .

devcontainer/up tmp/devcontainer.cid:
	mkdir -p tmp
	npx -- @devcontainers/cli up --workspace-folder . --remove-existing-container

devcontainer/down:
	podman container stop --cidfile tmp/devcontainer.cid --ignore
	rm -f tmp/devcontainer.cid
