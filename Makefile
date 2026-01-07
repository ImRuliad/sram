# Makefile

# Use uv's Python by prepending venv bin to PATH
VENV_BIN := $(PWD)/.venv/bin
export PATH := $(VENV_BIN):$(PATH)
PYTHON_BIN := $(VENV_BIN)/python3

RTL_DIR := $(PWD)/rtl
SIM_DIR := $(PWD)/sim

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(RTL_DIR)/bit_cell.sv

COCOTB_TOPLEVEL = bit_cell
COCOTB_TEST_MODULES = tests.bit_cell_test

SIM_BUILD = $(SIM_DIR)/sim_build

include $(shell $(VENV_BIN)/cocotb-config --makefiles)/Makefile.sim
