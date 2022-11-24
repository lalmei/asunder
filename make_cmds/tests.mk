##############
# Unit Tests #
##############

.PHONY: test
test: clean ## Run tests in the poetry environment.
	@$(call i, Running tests)
	poetry run pytest  -c=config/pytest.ini ${test.python}

###########
# Cleanup #
###########

.PHONY: clean
clean: clean-test ## Remove all build artifacts.
	rm -f docs/modules.rst
	rm -rf $(build.dir)
	rm -rf $(dist.dir)
	rm -f $(src.python.pyc)
	rm -rf $(egg.dir)
	rm -rf $(site.dir)
	rm -rf $(output.dir)
	

.PHONY: clean-test
clean-test: ## Remove test and coverage artifacts.
	rm -fr .tox/
	rm -fr .coverage*
	rm -fr htmlcov/
	rm -rf junit.xml
	rm -rf $(pytest.cache.dir)
	rm -rf $(cache.dir)
	rm -rf $(checkpoint.dir)
	rm -rf $(mypy.cache.dir)
	rm -rf interrogate_badge.svg
	rm -rf maintain.svg

.PHONY: clean-poetry-cache
clean-poetry-cache: ## Clear the local poetry cache.
	poetry cache clear -n --all $(shell poetry cache list | head -n 1 )

.PHONY: clean-full ## Clean artifacts and cache
clean-full: clean clean-poetry-cache
