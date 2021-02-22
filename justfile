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

# Remove distribution archives
clean:
	rm -rf build/ dist/ simple_totp.egg-info/ __pycache__/

# Generate distribution archives
build:
	python setup.py sdist bdist_wheel

# Upload distribution archives to PyPI
upload:
	twine upload dist/*

# Build and upload to PyPI
publish:
	just clean
	just build
	just upload
