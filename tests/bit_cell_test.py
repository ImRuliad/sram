import cocotb
import tests.constants as constants
from cocotb.triggers import Timer

async def reset_sequence(dut):
    dut.rst.value = constants.HIGH
    dut.write_enable.value = constants.LOW
    dut.data_in.value = constants.LOW
    dut.clk.value = constants.LOW
    await Timer(2, unit=constants.NANOSECONDS)
    dut.rst.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)

async def generate_clock_cycle(dut):
    dut.clk.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)
    dut.clk.value = constants.HIGH
    await Timer(1, unit=constants.NANOSECONDS)

async def write_data(dut, data):
    dut.write_enable.value = constants.HIGH
    dut.data_in.value = data

# ============================================= BASIC FUNCTIONALITY TESTS =============================================

#ensure ff can be clocked.
@cocotb.test()
async def smoke_test(dut):
    for _ in range (constants.CLOCK_PERIOD_NS):
      await generate_clock_cycle(dut)

#ensure ff state can be reset.
@cocotb.test()
async def test_reset_state(dut):
    dut.rst.value = constants.HIGH
    dut.write_enable.value = constants.LOW
    dut.data_in.value = constants.LOW
    await Timer(2, unit=constants.NANOSECONDS)
    assert dut.data_out.value == constants.LOW, f"Reset failed: EXPECTED {constants.LOW}, GOT {dut.data_out.value}"
    cocotb.log.info("Reset state passed!")

#ensure ff can output active high.
@cocotb.test()
async def test_write_high(dut):
    await reset_sequence(dut)
    await write_data(dut, constants.HIGH)
    await generate_clock_cycle(dut)
    assert dut.data_out.value == constants.HIGH, f"Write High failed: EXPECTED {constants.HIGH}, GOT {dut.data_out.value}"

#ensure ff can output active low.
@cocotb.test()
async def test_write_low(dut):
    await reset_sequence(dut)
    await write_data(dut, constants.LOW)
    await generate_clock_cycle(dut)
    assert dut.data_out.value == constants.LOW, f"Write Low failed: EXPECTED {constants.LOW}, GOT {dut.data_out.value}"

# ============================================= ASYNC AND RESET PRIORITY TESTS =============================================

@cocotb.test()
async def test_async_rst_during_clk_high(dut):
    await reset_sequence(dut)
    await write_data(dut, constants.HIGH)
    dut.clk.value = constants.HIGH
    await Timer(1, unit=constants.NANOSECONDS)
    dut.rst.value = constants.HIGH
    await Timer(1, unit=constants.NANOSECONDS)
    assert dut.data_out.value == constants.LOW, f"Async Reset during CLK High failed: EXPECTED {constants.LOW}, GOT {dut.data_out.value}"

@cocotb.test()
async def test_async_rst_during_clk_low(dut):
    await reset_sequence(dut)
    await write_data(dut, constants.HIGH)
    dut.clk.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)
    dut.rst.value = constants.HIGH
    await Timer(1, unit=constants.NANOSECONDS)
    assert dut.data_out.value == constants.LOW, f"Async Reset during clk Low failed: EXPECTED {constants.LOW}, GOT {dut.data_out.value}"