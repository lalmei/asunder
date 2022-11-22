###################
# Build & Release #
###################

.PHONY: publish
publish: ## Publish package to local.
	@$(call i, Publishing package .whl to pypi)
	poetry publish

## Run checks, test, and build.
release: check build 

$(build.wheel): $(src.python)
	@$(call i, Build the package wheel)
	poetry build

build: $(build.wheel) ## Build the distribution wheel.