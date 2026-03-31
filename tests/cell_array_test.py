import cocotb
from cocotb.handle import SimHandleBase
from cocotb.triggers import Timer

import tests.constants as constants
from tests.utils import generate_clock_cycle, smoke_test

# ==================== HELPER FUNCTIONS ====================


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


# Ensure cell can be clocked
# Figure out how to call this method from utils.py
@cocotb.test()
async def smoke_test(dut: SimHandleBase) -> None:
    await smoke_test(dut)


@cocotb.test()
async def test_read_write(dut: SimHandleBase) -> None:
    await reset_cell_array(dut)
    test_data: int = constants.ALL_ONES
    test_row: int = 0
    test_col: int = 0
    await write_byte(dut, test_row, test_col, test_data)
    read_data: int = await read_byte(dut, test_row, test_col)
    assert read_data == test_data, f"Expected {test_data}, got {read_data}"

@cocotb.test()
async def test_march_c(dut: SimHandleBase) -> None:
    await reset_cell_array(dut)

    all_addresses = [
        (row,col)
        for row in range (constants.ROWS)
        for col in range (constants.COLS // constants.DATA_WIDTH)
    ]

    #Pass 1
    for row, col in all_addresses:
        await write_byte(dut, row, col, constants.ALL_ZEROES)
    
    #Pass 2
    for row, col in all_addresses:
        val = await read_byte(dut, row, col)
        assert val == constants.ALL_ZEROES
        await write_byte(dut, row, col, constants.ALL_ONES)
    
    #Pass 3
    for row, col in all_addrs:
        val = await read_byte(dut, row, col)
        assert val == constants.ALL_ONES, f"Pass 3 ↑ r1 failed at ({row},{col}): got {val:#04x}"
        await write_byte(dut, row, col, constants.ALL_ZEROES)

    # Pass 4: ↓ read 0x00, then write 0xFF
    for row, col in reversed(all_addrs):
        val = await read_byte(dut, row, col)
        assert val == constants.ALL_ZEROES, f"Pass 4 ↓ r0 failed at ({row},{col}): got {val:#04x}"
        await write_byte(dut, row, col, constants.ALL_ONES)

    # Pass 5: ↓ read 0xFF, then write 0x00
    for row, col in reversed(all_addrs):
        val = await read_byte(dut, row, col)
        assert val == constants.ALL_ONES, f"Pass 5 ↓ r1 failed at ({row},{col}): got {val:#04x}"
        await write_byte(dut, row, col, constants.ALL_ZEROES)

    # Pass 6: ↑ read 0x00 (final verification)
    for row, col in all_addrs:
        val = await read_byte(dut, row, col)
        assert val == constants.ALL_ZEROES, f"Pass 6 ↑ r0 failed at ({row},{col}): got {val:#04x}"

