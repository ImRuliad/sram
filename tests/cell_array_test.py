import cocotb
import tests.constants as constants
from cocotb.triggers import Timer

# ==================== HELPER FUNCTIONS ====================

async def generate_clock_cycle(dut):
    dut.clk.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)
    dut.clk.value = constants.HIGH
    await Timer(1, unit=constants.NANOSECONDS)

async def reset_cell_array(dut):
    dut.rst.value = constants.HIGH
    dut.row_select = constants.LOW
    dut.col_write_enable.value = constants.LOW
    dut.col_data_in.value = constants.LOW
    dut.clk.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)
    dut.rst.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)
    cocotb.log.info("Array rest complete")


# ==================== BASIC FUNCTIONAL TESTS ====================

#Verify cell array can be clocked
@cocotb.test()
async def smoke_test(dut):
    for _ in range (constants.CLOCK_PERIOD_NS):
      await generate_clock_cycle(dut)