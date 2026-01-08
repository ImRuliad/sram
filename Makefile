# Makefile

VENV_BIN := $(PWD)/.venv/bin
export PATH := $(VENV_BIN):$(PATH)
PYTHON_BIN := $(VENV_BIN)/python3

RTL_DIR := $(PWD)/rtl
SIM_DIR := $(PWD)/sim

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

# ==================== BIT CELL TEST ==================== 
test_bit_cell: VERILOG_SOURCES += $(RTL_DIR)/bit_cell.sv
test_bit_cell: COCOTB_TOPLEVEL = bit_cell
test_bit_cell: COCOTB_TEST_MODULES = tests.bit_cell_test
test_bit_cell: SIM_BUILD = $(SIM_DIR)/sim_build
test_bit_cell: 
	@echo "Running bit_cell tests..."
	$(MAKE) -f $(firstword $(MAKEFILE_LIST)) sim MODULE=$(COCOTB_TEST_MODULES) TOPLEVEL=$(COCOTB_TOPLEVEL) VERILOG_SOURCES="$(VERILOG_SOURCES)" SIM_BUILD=$(SIM_BUILD)

# ==================== CELL ARRAY TEST ==================== 
test_cell_array: VERILOG_SOURCES += $(RTL_DIR)/bit_cell.sv $(RTL_DIR)/cell_array.sv
test_cell_array: COCOTB_TOPLEVEL = cell_array
test_cell_array: COCOTB_TEST_MODULES = tests.cell_array_test
test_cell_array: SIM_BUILD = $(SIM_DIR)/sim_build
test_cell_array:
	@echo "Running cell_array tests..."
	$(MAKE) -f $(firstword $(MAKEFILE_LIST)) sim MODULE=$(COCOTB_TEST_MODULES) TOPLEVEL=$(COCOTB_TOPLEVEL) VERILOG_SOURCES="$(VERILOG_SOURCES)" SIM_BUILD=$(SIM_BUILD)

include $(shell $(VENV_BIN)/cocotb-config --makefiles)/Makefile.sim
