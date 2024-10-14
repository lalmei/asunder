########################
# Style and Formatting #
########################

.PHONY: check
check: check-format check-lint check-types check-docs test ## Check everything

.PHONY: check-format
check-format: ## Check style formatting.
	@$(call i, Checking code formatting)
	poetry run ruff format --check --config=./config/ruff.toml ${src.python} $(test.python) $(template.python) $(scripts.python)

.PHONY: format
format: ## Fix formatting with isort & black. This updates files.
	@$(call i, Formatting code)
	poetry run ruff format --fix --config=./config/ruff.toml ${src.python} $(test.python) $(template.python) $(scripts.python)

.PHONY: check-lint
check-lint: ## Check code for lint errors.
	@$(call i, Running the linter)
	poetry run ruff check --config=./config/ruff.toml ${src.python} $(test.python) $(template.python) $(scripts.python)

.PHONY: lint
lint: ## Check code for lint errors.
	@$(call i, Running the linter)
	poetry run ruff check --fix --config=./config/ruff.toml ${src.python} $(test.python) $(template.python) $(scripts.python)


.PHONY: check-types
check-types: ## Run mypy to check type definitions.
	@$(call i, Running mypy linter)
	poetry run mypy --config=./config/mypy.ini $(src.python) $(test.python) $(template.python) $(scripts.python)

# .PHONY: safety
# safety: ## Check for known vulnurabilities on dependencies.
# 	@$(call i, Checking for known vulnurabilities in dependencies)
# 	poetry run safety check --stdin --full-report


#################
#     Badges    #
#################

.PHONY:docstring-coverage
docstring-coverage: ## Compute docstring coverage
	@$(call i, Compute docstring coverage)
	poetry run interrogate -c config/interrogate.toml .

.PHONY: maintain
maintain: ## Compute maintainability metric
	poetry run radon cc -s --total-average  src/* | \
	 tail -n 1  | sed  -E 's/^Average complexity: ([ABCDEF]) .*$\/\1/' | \
	 xargs -I {} poetry run anybadge --label Maintainability --value={} \
	  --file=maintain.svg A=green B=orange C=yellow D=red F=red
