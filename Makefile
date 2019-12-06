PYTHON = python3.7


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


# ----- Virtualenv -----

venv:
	@if [ ! -d "venv" ]; then $(PYTHON) -m venv venv ; fi;


# ----- Update -----

update:
	@echo "----- Updating requirements -----"
	@export XXHASH_FORCE_CFFI=1
	@pip install --upgrade wheel pip
	@pip install --upgrade --requirement requirements.txt


# ----- Setup -----

setup: install venv
	@bash -c "source venv/bin/activate && $(MAKE) update"


# ----- Run -----

run:
	xdg-open "http://127.0.0.1:8000/"
	python manage.py runserver
