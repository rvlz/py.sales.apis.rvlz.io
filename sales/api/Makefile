.PHONY: test
test:
	@python manage.py test

.PHONY: lint
lint:
	@python -m flake8

.PHONY: format
format:
	@python -m black . --line-length 79 --verbose
