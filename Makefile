# Makefile

# Use uv's Python by prepending venv bin to PATH
VENV_BIN := $(PWD)/.venv/bin
SHELL := /bin/bash
export PATH := $(VENV_BIN):$(PATH)

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/bit_cell.sv

COCOTB_TOPLEVEL = bit_cell

COCOTB_TEST_MODULES = tests.bit_cell_test

include $(shell $(VENV_BIN)/cocotb-config --makefiles)/Makefile.sim