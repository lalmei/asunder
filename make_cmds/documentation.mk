#################
# Documentation #
#################

.PHONY: check-docs
check-docs: ## Check documentation.
	@$(call i, Checking Documentation)
	poetry run mkdocs build -f config/mkdocs.yml -s

.PHONY: docs
docs: ## Build documentation.
	@$(call i, Build Documentation)
	poetry run mkdocs build -f config/mkdocs.yml

.PHONY: docs-preview
docs-preview: ## Build documentation preview.
	@$(call i, Build Documentation Preview)
	mkdir -p site_preview
	poetry run mkdocs build -f config/mkdocs.yml -d ../site_preview


.PHONY: docs-serve
docs-serve: ## Serve documentation.
	@$(call i, Serve Documentation)
	poetry run mkdocs serve -f config/mkdocs.yml --dev-addr 127.0.0.1:8008

.PHONY: docs-live 
docs-live: docs-serve ## Serve documentation and open browser.
	@$(call i, Opening webpage)
	$(BROWSER) http://127.0.0.1:8008/asunder

