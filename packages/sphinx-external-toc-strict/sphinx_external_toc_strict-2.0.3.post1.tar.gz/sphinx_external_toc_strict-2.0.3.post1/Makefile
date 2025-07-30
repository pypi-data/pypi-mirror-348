.ONESHELL:
.DEFAULT_GOAL := help
SHELL := /bin/bash

# underscore separated; aka sdist and whl names
# https://blogs.gentoo.org/mgorny/2023/02/09/the-inconsistencies-around-python-package-naming-and-the-new-policy/
APP_NAME := sphinx_external_toc_strict

define NORMALIZE_APP_NAME
try:
    from importlib import metadata
except ImportError:
    v = '$(APP_NAME)'.replace('_', "-").replace('.', "-")
    print(v)
else:
    print(metadata.metadata('$(APP_NAME)')['Name']))
endef

#virtual environment. If 0 issue warning
#Not activated:0
#activated: 1
ifeq ($(VIRTUAL_ENV),)
$(warning virtualenv not activated)
is_venv =
else
is_venv = 1
VENV_BIN := $(VIRTUAL_ENV)/bin
VENV_BIN_PYTHON := python3
endif

ifeq ($(is_venv),1)
  # Package name is hyphen delimited
  PACKAGE_NAME ?= $(shell $(VENV_BIN_PYTHON) -c "$(NORMALIZE_APP_NAME)")
  VENV_PACKAGES ?= $(shell $(VENV_BIN_PYTHON) -m pip list --disable-pip-version-check --no-python-version-warning --no-input | /bin/awk '{print $$1}')
  IS_PACKAGE ?= $(findstring $(1),$(VENV_PACKAGES))

  is_wheel ?= $(call IS_PACKAGE,wheel)
  is_piptools ?= $(call IS_PACKAGE,pip-tools)

  find_whl = $(shell [[ -z "$(3)" ]] && extension=".whl" || extension="$(3)"; [[ -z "$(2)" ]] && srcdir="dist" || srcdir="$(2)/dist"; [[ -z "$(1)" ]] && whl=$$(ls $$srcdir/$(APP_NAME)*.whl  --format="single-column") || whl=$$(ls $$srcdir/$(1)*.whl --format="single-column"); echo $${whl##*/})
endif

##@ Helpers

# https://www.thapaliya.com/en/writings/well-documented-makefiles/
.PHONY: help
help:					## (Default) Display this help -- Always up to date
	@awk -F ':.*##' '/^[^: ]+:.*##/{printf "  \033[1m%-20s\033[m %s\n",$$1,$$2} /^##@/{printf "\n%s\n",substr($$0,5)}' $(MAKEFILE_LIST)

##@ Build dependencies

.PHONY: upgrade doc_upgrade diff_upgrade _upgrade
PIP_COMPILE = $(VENV_BIN_PYTHON) -m piptools compile --allow-unsafe --resolver=backtracking

upgrade:				## Update the *.pip files with the latest packages satisfying *.in files.
	@$(MAKE) _upgrade COMPILE_OPTS="--upgrade"

upgrade-one:			## Update the *.pip files for one package. `make upgrade-one package=...`
	@test -n "$(package)" || { echo "\nUsage: make upgrade-one package=...\n"; exit 1; }
	$(MAKE) _upgrade COMPILE_OPTS="--upgrade-package $(package)"

_upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
_upgrade:
ifeq ($(is_venv),1)
  ifeq ($(is_piptools), pip-tools)
	@pip install --quiet --disable-pip-version-check -r requirements/pip-tools.pip
	$(PIP_COMPILE) -o requirements/pip.pip requirements/pip.in
	$(PIP_COMPILE) -o requirements/pip-tools.pip requirements/pip-tools.in
	$(PIP_COMPILE) -o requirements/kit.pip requirements/kit.in
	$(PIP_COMPILE) --no-strip-extras -o requirements/mypy.pip requirements/mypy.in
	$(PIP_COMPILE) --no-strip-extras -o requirements/tox.pip requirements/tox.in

	$(PIP_COMPILE) --no-strip-extras -o requirements/manage.pip requirements/manage.in
	$(PIP_COMPILE) --no-strip-extras -o requirements/dev.pip requirements/dev.in
  endif
endif

doc_upgrade: export CUSTOM_COMPILE_COMMAND=make doc_upgrade
doc_upgrade: $(VENV_BIN)	## Update the doc/requirements.pip file
ifeq ($(is_venv),1)
  ifeq ($(is_piptools), pip-tools)
	@$(VENV_BIN)/pip install --quiet --disable-pip-version-check -r requirements/pip-tools.pip
	$(VENV_BIN)/$(PIP_COMPILE) -o docs/requirements.pip docs/requirements.in
  endif
endif

diff_upgrade:			## Summarize the last `make upgrade`
	@# The sort flags sort by the package name first, then by the -/+, and
	@# sort by version numbers, so we get a summary with lines like this:
	@#      -bashlex==0.16
	@#      +bashlex==0.17
	@#      -build==0.9.0
	@#      +build==0.10.0
	@/bin/git diff -U0 | /bin/grep -v '^@' | /bin/grep == | /bin/sort -k1.2,1.99 -k1.1,1.1r -u -V

.PHONY: version-override
version-override:			## Apply fixes only
	@echo "Restriction caused by myst-parser. Force upgrade Sphinx and docutils" 1>&2
	fix_pkgs=(Sphinx docutils)
	affects=(requirements/prod.pip requirements/manage.pip requirements/dev.pip docs/requirements.pip)

	for pkg_upper in $${fix_pkgs[@]}; do
	version=$$(get_pypi_latest_version $$pkg_upper)
	pkg_lower=$$(echo "$$pkg_upper" | tr '[:upper:]' '[:lower:]')

	for f in $${affects[@]}; do
	echo "$$pkg_upper --> $$version $$f" 1>&2
	sed -e "/^$${pkg_lower}==/s/.*/$${pkg_lower}==$${version}/g" $${f} > $${f}.tmp && mv $${f}.tmp $${f}
	done

	done

# https://unix.stackexchange.com/questions/596180/awk-how-to-replace-a-line-beginning-with
.PHONY: fix-upgrade
fix-upgrade: | upgrade doc_upgrade version-override
fix-upgrade:				## Upgrade and apply fixes

##@ Testing

#run all pre-commit checks
.PHONY: pre-commit
pre-commit:				## Run checks found in .pre-commit-config.yaml
	@pre-commit run --all-files

#--strict is on
.PHONY: mypy
mypy:					## Static type checker (in strict mode)
ifeq ($(is_venv),1)
	@$(VENV_BIN_PYTHON) -m mypy -p $(APP_NAME)
endif

#make [check=1] black
.PHONY: black
black: private check_text = $(if $(check),"--check", "--quiet")
black:					## Code style --> In src and tests dirs, Code formatting. Sensible defaults -- make [check=1] black
ifeq ($(is_venv),1)
	@$(VENV_BIN)/black $(check_text) src/
	$(VENV_BIN)/black $(check_text) tests/
endif

.PHONY: isort
isort:					## Code style --> sorts imports
ifeq ($(is_venv),1)
	@$(VENV_BIN)/isort src/
	$(VENV_BIN)/isort tests/
endif

.PHONY: flake
flake:					## Code style --> flake8 extreme style nitpikker
ifeq ($(is_venv),1)
	@$(VENV_BIN_PYTHON) -m flake8 src/
	$(VENV_BIN_PYTHON) -m flake8 tests/
endif

##@ Kitting
# Initial build
# mkdir dist/ ||:; python -m build --outdir dist/ .
# pip install --disable-pip-version-check --no-color --find-links=file://///$HOME/Downloads/git_decimals/sphinx_external_toc_strict/dist sphinx-external-toc-strict

REPO_OWNER := msftcangoblowm/sphinx-external-toc-strict
REPO := $(REPO_OWNER)/sphinx_external_toc_strict

.PHONY: edit_for_release cheats relbranch kit_check kit_build kit_upload
.PHONY: test_upload kits_download github_releases

edit_for_release:               ## Edit sources to insert release facts (see howto.txt)
	python igor.py edit_for_release

cheats:                                 ## Create some useful snippets for releasing (see howto.txt)
	python igor.py cheats | tee cheats.txt

relbranch:                              ## Create the branch for releasing (see howto.txt)
	@git switch -c $(REPO_OWNER)/release-$$(date +%Y%m%d)

# Do not create a target(s) kit: or kits:
kit_check:                              ## Check that dist/* are well-formed
	python -m twine check dist/*
	@echo $$(ls -1 dist | wc -l) distribution kits

kit_upload:                             ## Upload the built distributions to PyPI
	twine upload --verbose dist/*

test_upload:                    ## Upload the distributions to PyPI's testing server
	twine upload --verbose --repository testpypi --password $$TWINE_TEST_PASSWORD dist/*

kits_build:                             ## Trigger GitHub to build kits
	python ci/trigger_build_kits.py $(REPO_OWNER)

kits_download:                  ## Download the built kits from GitHub
	python ci/download_gha_artifacts.py $(REPO_OWNER) 'dist-*' dist

github_releases: $(DOCBIN)              ## Update GitHub releases.
	$(DOCBIN)/python -m scriv github-release --all

##@ GNU Make standard targets

# kind tag current or semantic version str
.PHONY: build
build:				## Make the source distribution
	@python igor.py build_next ""

.PHONY: install
install: override usage := make [force=1]
install: override check_web := Install failed. Possible cause no web connection
install: private force_text = $(if $(force),"--force-reinstall")
install:				## Installs *as a package*, not *with the ui* -- make [force=1] [debug=1] install
ifeq ($(is_venv),1)
  ifeq ($(is_wheel), wheel)
	@if [[  "$$?" -eq 0 ]]; then

	whl=$(call find_whl,$(APP_NAME),,) #1: PYPI package name (hyphens). 2 folder/app name (APP_NAME;underscores). 3 file extension
	echo $(whl)
	$(VENV_BIN_PYTHON) -m pip install --disable-pip-version-check --no-color --log="/tmp/$(APP_NAME)_install_prod.log" $(force_text) "dist/$$whl"

	fi

  endif
endif

.PHONY: install-force
install-force: force := 1
install-force: install	## Force install even if exact same version

# --cov-report=xml
# Dependencies: pytest, pytest-cov, pytest-regressions
# make [v=1] check
# @$(VENV_BIN)/pytest --showlocals --cov=sphinx_external_toc_strict --cov-report=term-missing tests
.PHONY: check
check: private verbose_text = $(if $(v),"--verbose")
check:					## Run tests, generate coverage reports -- make [v=1] coverage
ifeq ($(is_venv),1)
	-@$(VENV_BIN_PYTHON) -m coverage erase
	$(VENV_BIN_PYTHON) -m coverage run --parallel -m pytest --showlocals $(verbose_text) tests
	$(VENV_BIN_PYTHON) -m coverage combine
	$(VENV_BIN_PYTHON) -m coverage report --fail-under=90
endif
