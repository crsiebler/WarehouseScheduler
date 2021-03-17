build:
	docker build -t pyscheduler .

help:
	docker run -it --rm --name pyscheduler -v ${PWD}:/usr/src/app -w /usr/src/app pyscheduler python -m pyscheduler -h

run:
	docker run -it --rm --name pyscheduler -v ${PWD}:/usr/src/app -w /usr/src/app pyscheduler python -m pyscheduler --input=tests/input/spread.txt
	docker run -it --rm --name pyscheduler -v ${PWD}:/usr/src/app -w /usr/src/app pyscheduler python -m pyscheduler --input=tests/input/input1.txt
	docker run -it --rm --name pyscheduler -v ${PWD}:/usr/src/app -w /usr/src/app pyscheduler python -m pyscheduler --input=tests/input/input2.txt
	docker run -it --rm --name pyscheduler -v ${PWD}:/usr/src/app -w /usr/src/app pyscheduler python -m pyscheduler --input=tests/input/input3.txt
	docker run -it --rm --name pyscheduler -v ${PWD}:/usr/src/app -w /usr/src/app pyscheduler python -m pyscheduler --input=tests/input/input4.txt
	docker run -it --rm --name pyscheduler -v ${PWD}:/usr/src/app -w /usr/src/app pyscheduler python -m pyscheduler --input=tests/input/input5.txt

test:
	docker run -it --rm --name pyscheduler -v ${PWD}:/usr/src/app -w /usr/src/app pyscheduler python -m tests

coverage:
	docker run -it --rm --name pyscheduler -v ${PWD}:/usr/src/app -w /usr/src/app pyscheduler coverage run -m tests	

coverage-report:
	docker run -it --rm --name pyscheduler -v ${PWD}:/usr/src/app -w /usr/src/app pyscheduler coverage report

coverage-html:
	docker run -it --rm --name pyscheduler -v ${PWD}:/usr/src/app -w /usr/src/app pyscheduler coverage html
	wslview htmlcov/index.html