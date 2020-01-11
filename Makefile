test:
	python -mpytest -q src

fmt:
	isort -rc --atomic src
	black src
	isort -rc --atomic main.py
	black main.py