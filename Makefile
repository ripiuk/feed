PYTHON = python3.7


PSQL_USER = oleksandr
PSQL_PASSWORD = oleksandr
PSQL_DB = feed
# ========== Linux (Debian) ==========


# ----- Install -----

install:
	$(if $(shell apt-cache search $(PYTHON)), , \
		sudo apt-get -q update \
		&& apt-get install --no-install-recommends -y apt-utils software-properties-common \
		&& add-apt-repository -y ppa:jonathonf/python-3.7 \
		&& apt-get -q update)
	sudo apt-get install --no-install-recommends -y \
		build-essential \
		$(PYTHON) $(PYTHON)-dev $(PYTHON)-venv cython \
		libssl-dev libffi-dev openssl \
		redis-server

install-psql:
	sudo apt-get -q update \
	&& apt-get install -y postgresql postgresql-contrib postgresql-server-dev-10
	sudo -u postgres psql -c "CREATE USER $(PSQL_USER) with password '$(PSQL_PASSWORD)'"
	sudo -u postgres psql -c "ALTER ROLE $(PSQL_USER) SET client_encoding TO 'utf8'"
	sudo -u postgres psql -c "ALTER ROLE $(PSQL_USER) SET default_transaction_isolation TO 'read committed'"
	sudo -u postgres psql -c "ALTER ROLE $(PSQL_USER) SET timezone TO 'UTC'"
	sudo -u postgres psql -c "CREATE DATABASE $(PSQL_DB) OWNER $(PSQL_USER)"
	sudo -u postgres psql -c "ALTER USER $(PSQL_USER) CREATEDB"

# ----- Virtualenv -----

venv_init:
	if [ ! -e "venv/bin/activate" ]; then $(PYTHON) -m venv venv ; fi;
	bash -c "source venv/bin/activate && \
		pip install --upgrade wheel pip setuptools && \
		pip install --upgrade --requirement requirements.txt"


# ----- Update -----

update: venv_init

update-dev: venv_init
	bash -c "source venv/bin/activate && \
		pip install --upgrade --requirement requirements-dev.txt"

# ----- Setup -----

setup: install venv_init

setup_test: install update-dev


# ----- Run -----

run:
	xdg-open "http://127.0.0.1:8000/usage_info"
	python manage.py runserver


# ----- Tests -----

test: update-dev
	python manage.py test
	flake8

test-cov: update-dev
	coverage run --source='.' manage.py test
	coverage report