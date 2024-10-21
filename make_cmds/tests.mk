##############
# Unit Tests #
##############

.PHONY: test
test: clean ## Run tests in the poetry environment.
	@$(call i, Running tests)
	poetry run pytest  -c=config/pytest.ini ${test.python}

