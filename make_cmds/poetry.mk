#########
# Setup #
#########

ifeq ($(shell which poetry), )
	$(error "Can't find poetry on the PATH. Please run 'make install-poetry' or update PATH")
endif

poetry.lock: pyproject.toml
	@$(call i, Updating poetry.lock file)
	poetry lock --no-update

.PHONY: install-poetry
install-poetry: ## Install poetry.
	@$(call i, Installing Poetry)
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: install
install: poetry.lock  ## Install all dependencies with poetry.
	@$(call i, Installing all python dependencies)
	poetry install --no-ansi --sync

.PHONY: install-no-dev
install-no-dev: poetry.lock ## Install only dependencies necessary to run code.
	@$(call i, Installing python dependencies, excluding dev)
	poetry install --sync --no-ansi --no-dev

.PHONY: update-poetry
update-poetry: ### Update all dependencies with poetry.
	@$(call i, Updating all python dependencies)
	poetry update

.PHONY: jupyter-kernel
jupyter-kernel: ## Install a Jupyter kernel for this project.
	@$(call i, Installing a Jupyter kernel for this project)
	poetry run python -m ipykernel install --user --name=asunder
