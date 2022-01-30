SHELL  := /bin/bash

run : *.py
	@(                                                           \
		source ./venv/bin/activate;                          \
		./auth 'python ./sample.py'                          \
	)

