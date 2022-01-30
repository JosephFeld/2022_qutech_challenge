SHELL  := /bin/bash

run : *.py
	@(                                                           \
		[ -e venv ] && source ./venv/bin/activate;           \
		./auth 'python ./sample.py'                          \
	)

