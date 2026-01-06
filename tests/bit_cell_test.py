import cocotb
from cocotb.triggers import Timer

LOW = 0
HIGH = 1
CLOCK_PERIODS = 10
NANOSECONDS = "ns"

async def reset_sequence(dut):
    dut.rst.value = HIGH
    dut.write_enable.value = LOW
    dut.data_in.value = LOW
    dut.clk.value = LOW
    await Timer(2, units=NANOSECONDS)
    dut.rst.value = LOW
    await Timer(1, units=NANOSECONDS)

@cocotb.test()
async def smoke_test(dut):
    for _ in range (CLOCK_PERIODS):
        dut.clk.value = LOW
        await Timer(1, unit=NANOSECONDS)
        dut.clk.value = HIGH
        await Timer(1, unit=NANOSECONDS)

@cocotb.test()
async def test_reset_state(dut):
    dut.rst.value = HIGH
    dut.write_enable.value = LOW
    dut.data_in.value = LOW
    await Timer(2, unit=NANOSECONDS)
    assert dut.data_out.value == LOW, f"Reset failed: data_out should be {LOW}, got {dut.data_out.value}"
    cocotb.log.info("Reset state passed!")

@cocotb.test()
async def test_write_high(dut):
    await reset_sequence(dut)
    dut.write_enable.value = HIGH
    dut.data_in.value = HIGH
    dut.clk.value = LOW
    await Timer(1, units=NANOSECONDS)
    dut.clk.value = HIGH
    await Timer(1, units=NANOSECONDS)
    assert dut.data_out.value == HIGH, f"Write High failed: data_out should be {HIGH}, got {dut.data_out.value}"

