########################
# Style and Formatting #
########################

.PHONY: check
check: check-format check-lint check-types check-docs test ## Check everything

.PHONY: check-format
check-format: ## Check style formatting.
	@$(call i, Checking import formatting)
	poetry run isort --settings-path ./config/.isort.cfg --show-config --check-only -v ${src.python} $(test.python) $(template.python) $(scripts.python)
	@$(call i, Checking code formatting)
	poetry run black --check --diff -v ${src.python} $(test.python) $(template.python) $(scripts.python)

.PHONY: format
format: ## Fix formatting with isort & black. This updates files.
	@$(call i, Formatting imports)
	poetry run isort ${src.python} $(test.python) $(template.python) $(scripts.python)
	@$(call i, Formatting code)
	poetry run black ${src.python} $(test.python) $(template.python) $(scripts.python)

.PHONY: check-lint
check-lint: ## Check code for lint errors.
	@$(call i, Running the linter)
	poetry run flake8 --config=./config/flake8.ini ${src.python} $(test.python) $(template.python) $(scripts.python)

.PHONY: check-full-lint
check-full-lint: ## Check code for lint errors.
	@$(call i, Running the linter)
	poetry run flake8 --config=./config/flake8_all.ini ${src.python} $(test.python) $(template.python)
	
.PHONY: lint
lint: ## Fix linting issues with autoflake. This updates files.
	@$(call i, Running the linter fix)
	poetry run autoflake --in-place --recursive --remove-all-unused-imports --remove-unused-variables \
		${src.python} $(test.python) $(template.python) $(scripts.python)

.PHONY: check-types
check-types: ## Run mypy to check type definitions.
	@$(call i, Running mypy linter)
	poetry run mypy --config=./config/mypy.ini $(src.python) $(test.python) $(template.python) $(scripts.python)

.PHONY: safety
safety: ## Check for known vulnurabilities on dependencies.
	@$(call i, Checking for known vulnurabilities in dependencies)
	poetry run safety check --stdin --full-report


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