SHELL := bash
version := 0.1.0

src.python := $(shell find ./src -type f -name "*.py" || :)
test.python := $(shell find ./tests -type f -name "*.py" || :)
scripts.python := $(shell find ./scripts -type f -name "*.py" || :)
src.python.pyc := $(shell find . -type f -name "*.pyc")
cache.dir := $(shell find . -type d -name __pycache__)
checkpoint.dir := $(shell find . -type d -name .ipynb_checkpoints)
mypy.cache.dir := $(shell find . -type d -name ".mypy_cache")
pytest.cache.dir := $(shell find . -type d -name ".pytest_cache")

dist.dir := dist
egg.dir := .eggs
build.dir := build
site.dir := site
output.dir := output

build.wheel := $(dist.dir)/asunder-$(version).tar.gz

include make_cmds/clean.mk
include make_cmds/poetry.mk
include make_cmds/quality.mk
include make_cmds/tests.mk
include make_cmds/documentation.mk
include make_cmds/build.mk

##############
# Versioning #
##############

.PHONY: bump-patch
bump-patch: ## Bump the patch version (_._.X) everywhere.
	@$(call i, Bumping the patch number)
	poetry run bump2version patch --allow-dirty --verbose --config-file config/.bumpversion.cfg

.PHONY: bump-minor
bump-minor: ## Bump the minor version (_.X._) everywhere.
	@$(call i, Bumping the minor number)
	poetry run bump2version minor --allow-dirty --verbose --config-file config/.bumpversion.cfg

.PHONY: bump-major
bump-major: ## Bump the major version (X._._) everywhere.
	@$(call i, Bumping the major number)
	poetry run bump2version major --allow-dirty --verbose --config-file config/.bumpversion.cfg

.PHONY: bump-release
bump-release: ## Convert the version into a release variant (_._._).
	@$(call i, Converting to release)
	poetry run bump2version release --allow-dirty --verbose --config-file config/.bumpversion.cfg

.PHONY: bump-dev
bump-dev: ## Convert the version into a dev variant (_._._-dev__).
	@$(call i, Converting to dev)
	poetry run bump2version dev --allow-dirty --verbose --config-file config/.bumpversion.cfg

.PHONY: bump-build
bump-build: ## Bump the build number (_._._-____XX) everywhere.
	@$(call i, Bumbing the build number)
	poetry run bump2version build --allow-dirty --verbose --config-file config/.bumpversion.cfg




#####################
# Docker Unit Tests #
#####################

.PHONY: docker-build
docker-build: clean ## Build docker image to test template.
	docker build -t ${docker.image}:${version} \
		--label org.label-schema.vcs-ref=${CI_COMMIT_SHA} \
		--label org.label-schema.vcs-url=${CI_PROJECT_URL} \
		--label com.climate.ci.job-url=${CI_JOB_URL} -f Dockerfile.dev .

.PHONY: docker-test
docker-test: clean ## Test in a clean container in your local machine.
	$(call i, Running tests in container)
	docker run --rm  \
		--mount type=bind,source=${PWD}/,target=/root/project,bind-propagation=private \
		--mount type=bind,source=${HOME}/.ssh,target=/root/.ssh,bind-propagation=private \
		--mount type=bind,source=${HOME}/.aws,target=/root/.aws,bind-propagation=private \
		${docker.image}:${version} make release


.PHONY: docker-env
docker-env: clean ## Run an interactive container in your local machine.
	$(call i, Jumping in base docker env)
	docker run --rm  -it  \
		--mount type=bind,source=${PWD}/,target=/root/project,bind-propagation=private \
		--mount type=bind,source=${HOME}/.ssh,target=/root/.ssh,bind-propagation=private \
		--mount type=bind,source=${HOME}/.aws,target=/root/.aws,bind-propagation=private \
		${docker.image}:${version} bash

.PHONY: help
help: ## Print the help screen.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":|:[[:space:]].*?##"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

##################
# User Functions #
##################

define BROWSER_PYSCRIPT
import os, webbrowser, sys
from urllib.request import pathname2url

webbrowser.open(sys.argv[1])
endef
export BROWSER_PYSCRIPT
BROWSER := poetry run python -c "$$BROWSER_PYSCRIPT"

define i
echo
python3 scripts/colors.py INFO "$1"
echo
endef

define w
echo
python3 scripts/colors.py WARN "$1"
echo
endef

define e
echo
python3 scripts/colors.py ERROR "$1"
echo
endef
