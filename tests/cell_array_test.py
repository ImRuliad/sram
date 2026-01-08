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
    dut.row_select.value = constants.LOW
    dut.col_select.value = constants.LOW
    dut.write_enable.value = constants.LOW
    dut.data_in.value = constants.LOW
    dut.clk.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)
    dut.rst.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)
    cocotb.log.info("Array reset complete")

async def write_byte(dut, row, col, data):
    dut.row_select.value = row
    dut.col_select.value = col
    dut.write_enable.value = 0xFF
    dut.data_in.value = data
    await generate_clock_cycle(dut)
    dut.write_enable.value = constants.LOW

async def read_byte(dut, row, col):
    dut.row_select.value = row
    dut.col_select.value = col
    dut.write_enable.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)
    return int(dut.data_out.value)


# ==================== BASIC FUNCTIONAL TESTS ====================

#Verify cell array can be clocked
@cocotb.test()
async def smoke_test(dut):
    for _ in range (constants.CLOCK_PERIOD_NS):
      await generate_clock_cycle(dut)

@cocotb.test()
async def test_read_write(dut):
    await reset_cell_array(dut)
    test_data, test_row, test_col = constants.ALL_ONES, 0, 0
    await write_byte(dut, test_row, test_col, test_data)
    assert await read_byte(dut, test_row, test_col) == test_data, f"Expected {test_data}, got {await read_byte(dut, test_row, test_col)}"