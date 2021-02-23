cwd := invocation_directory()

alias help := list

# List available recipes
list:
	@just --list

# Install dependencies
setup:
	pip install --requirement requirements.txt

# Install package locally
install:
	pip install --editable .

# Lint package
lint:
	@flake8

# Remove distribution archives
clean:
	rm -rf build/ dist/ simple_totp.egg-info/ __pycache__/

# Generate distribution archives
build:
	python setup.py sdist bdist_wheel

# Upload distribution archives to PyPI
upload:
	twine upload dist/*

# Tag current version and push to remote repository
tag:
	#!/usr/bin/env sh
	set -euxo pipefail
	version=$(python -c 'from otp import cli; print(cli.VERSION)')
	git tag "$version"
	git push --tags

# Build and upload to PyPI
publish:
	just lint
	just clean
	just build
	just upload
	just tag
