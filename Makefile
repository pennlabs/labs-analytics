SHELL := /bin/zsh

all:
	bazel run @hedron_compile_commands//:refresh_all &
	bazel run src/server:run