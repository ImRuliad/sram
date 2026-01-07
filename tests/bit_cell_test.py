import cocotb
from cocotb.triggers import Timer

LOW = 0
HIGH = 1
NANOSECONDS = "ns"

async def reset_sequence(dut):
    dut.rst.value = HIGH
    dut.write_enable.value = LOW
    dut.data_in.value = LOW
    dut.clk.value = LOW
    await Timer(2, unit=NANOSECONDS)
    dut.rst.value = LOW
    await Timer(1, unit=NANOSECONDS)

async def generate_clock_cycle(dut):
    dut.clk.value = LOW
    await Timer(1, unit=NANOSECONDS)
    dut.clk.value = HIGH
    await Timer(1, unit=NANOSECONDS)

async def write_data(dut, data):
    dut.write_enable.value = HIGH
    dut.data_in.value = data


# ============================================= BASIC FUNCTIONALITY TESTS =============================================

#ensure ff can be clocked.
@cocotb.test()
async def smoke_test(dut):
    CLOCK_PERIODS = 1000
    for _ in range (CLOCK_PERIODS):
      await generate_clock_cycle(dut)

#ensure ff state can be reset.
@cocotb.test()
async def test_reset_state(dut):
    dut.rst.value = HIGH
    dut.write_enable.value = LOW
    dut.data_in.value = LOW
    await Timer(2, unit=NANOSECONDS)
    assert dut.data_out.value == LOW, f"Reset failed: EXPECTED {LOW}, GOT {dut.data_out.value}"
    cocotb.log.info("Reset state passed!")

#ensure ff can output active high.
@cocotb.test()
async def test_write_high(dut):
    await reset_sequence(dut)
    await write_data(dut, HIGH)
    await generate_clock_cycle(dut)
    assert dut.data_out.value == HIGH, f"Write High failed: EXPECTED {HIGH}, GOT {dut.data_out.value}"

#ensure ff can output active low.
@cocotb.test()
async def test_write_low(dut):
    await reset_sequence(dut)
    await write_data(dut, LOW)
    await generate_clock_cycle(dut)
    assert dut.data_out.value == LOW, f"Write Low failed: EXPECTED {LOW}, GOT {dut.data_out.value}"

