REPO_NAME := RecommenderXBlock
DOCKER_NAME := recommenderxblock

COMMON_CONSTRAINTS_TXT=requirements/common_constraints.txt
.PHONY: $(COMMON_CONSTRAINTS_TXT)
$(COMMON_CONSTRAINTS_TXT):
	wget -O "$(@)" https://raw.githubusercontent.com/edx/edx-lint/master/edx_lint/files/common_constraints.txt || touch "$(@)"

install-test:
	pip install -q -r requirements/test.txt

install: install-test

test:  ## Run the tests
	mkdir -p var
	rm -rf .coverage
	python ./test.py $(TEST)

quality:  ## Run the quality checks
	pycodestyle --config=.pep8 recommender
	pylint --rcfile=pylintrc recommender
	python setup.py -q sdist
	twine check dist/*

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: $(COMMON_CONSTRAINTS_TXT)  ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -r requirements/pip.txt
	pip install -q -r requirements/pip_tools.txt
	pip-compile --upgrade --allow-unsafe --rebuild -o requirements/pip.txt requirements/pip.in
	pip-compile --upgrade -o requirements/pip_tools.txt requirements/pip_tools.in
	pip install -qr requirements/pip.txt
	pip install -qr requirements/pip_tools.txt
	pip-compile --upgrade -o requirements/base.txt requirements/base.in
	pip-compile --upgrade -o requirements/test.txt requirements/test.in
	pip-compile --upgrade -o requirements/quality.txt requirements/quality.in
	pip-compile --upgrade -o requirements/tox.txt requirements/tox.in
	pip-compile --upgrade -o requirements/ci.txt requirements/ci.in

requirements: ## install development environment requirements
	pip install -r requirements/pip.txt
	pip install -qr requirements/pip-tools.txt


dev.build:
	docker build -t $(DOCKER_NAME)-dev $(CURDIR)

dev.run: dev.build ## Clean, build and run test image
	docker run -p 8000:8000 -v $(CURDIR):/usr/local/src/$(REPO_NAME) --name $(DOCKER_NAME)-dev $(DOCKER_NAME)-dev
