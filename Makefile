test:
	python -mpytest -q src

fmt:
	isort -rc --atomic src
	black src
