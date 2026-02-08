import cocotb
import tests.constants as constants
from cocotb.triggers import Timer
from cocotb.handle import SimHandleBase

# ==================== HELPER FUNCTIONS ====================


async def generate_clock_cycle(dut: SimHandleBase) -> None:
    dut.clk.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)
    dut.clk.value = constants.HIGH
    await Timer(1, unit=constants.NANOSECONDS)


async def reset_cell_array(dut: SimHandleBase) -> None:
    dut.rst.value = constants.HIGH
    dut.row_select.value = constants.LOW
    dut.col_select.value = constants.LOW
    dut.write_enable.value = 0x00  # 8-bit byte-enable: all bits disabled
    dut.data_in.value = constants.LOW
    dut.clk.value = constants.LOW

    await Timer(1, unit=constants.NANOSECONDS)
    dut.rst.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)
    cocotb.log.info("Array reset complete")


async def write_byte(dut: SimHandleBase, row: int, col: int, data: int) -> None:
    dut.row_select.value = row
    dut.col_select.value = col
    dut.write_enable.value = 0xFF  # 8-bit byte-enable: all bits enabled
    dut.data_in.value = data

    await generate_clock_cycle(dut)
    dut.write_enable.value = 0x00  # Disable all byte-enable bits


async def read_byte(dut: SimHandleBase, row: int, col: int) -> int:
    dut.row_select.value = row
    dut.col_select.value = col
    dut.write_enable.value = 0x00  # 8-bit byte-enable: all bits disabled (read mode)

    await Timer(1, unit=constants.NANOSECONDS)
    return int(dut.data_out.value)


# ==================== BASIC FUNCTIONAL TESTS ====================


# Verify cell array can be clocked
@cocotb.test()
async def smoke_test(dut: SimHandleBase) -> None:
    for _ in range(constants.CLOCK_PERIOD_NS):
        await generate_clock_cycle(dut)


@cocotb.test()
async def test_read_write(dut: SimHandleBase) -> None:
    await reset_cell_array(dut)
    test_data: int = constants.ALL_ONES
    test_row: int = 0
    test_col: int = 0

    await write_byte(dut, test_row, test_col, test_data)
    read_data: int = await read_byte(dut, test_row, test_col)
    assert read_data == test_data, f"Expected {test_data}, got {read_data}"
