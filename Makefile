SHELL := /bin/zsh

all:
	bazel run src/server:run