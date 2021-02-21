cwd := invocation_directory()

alias help := list

# List available recipes
list:
	@just --list

# Remove distribution archives
clean:
	rm -rf build/ dist/ simple_totp.egg-info/ __pycache__/

# Generate distribution archives
build:
	python setup.py sdist

# Upload distribution archives to Test PyPI
upload-test:
	twine upload --repository testpypi dist/*

# Build and upload to Test PyPI
publish-test:
	just clean
	just build
	just upload-test

# Upload distribution archives to PyPI
upload:
	twine upload dist/*

# Build and upload to PyPI
publish:
	just clean
	just build
	just upload

# Install package locally
install:
	pip install --editable .

# Install package from Test PyPI
install-test:
	pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ simple-totp
