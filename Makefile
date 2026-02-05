SHELL = /bin/sh

IMAGE_NAME=arena-mcp-server

.PHONY: dbuild drun dshell dclean release

dbuild:
	docker compose -f docker-compose.yml build

drun:
	docker compose -f docker-compose.yml up -d

dshell:
	docker compose exec -it $(IMAGE_NAME) /bin/sh

dclean:
	docker compose -f docker-compose.yml down --rmi

# Release a new version
# Usage: make release VERSION=0.0.1
release:
ifndef VERSION
	$(error VERSION is required. Usage: make release VERSION=0.0.1)
endif
	@echo "Creating release v$(VERSION)..."
	@if git rev-parse v$(VERSION) >/dev/null 2>&1; then \
		echo "Error: Tag v$(VERSION) already exists"; \
		exit 1; \
	fi
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	git push origin v$(VERSION)
	@echo ""
	@echo "✓ Release v$(VERSION) created and pushed!"
	@echo "✓ GitHub workflow will build and push: ghcr.io/carbonrobotics/arena-mcp-server:v$(VERSION)"
	@echo ""
	@echo "Monitor the build at: https://github.com/carbonrobotics/arena-mcp-server/actions"