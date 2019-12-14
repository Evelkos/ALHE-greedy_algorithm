test:
	python -mpytest -q greedy

fmt:
	isort -rc --atomic greedy
	black greedy
