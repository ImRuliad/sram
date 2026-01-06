import cocotb
from cocotb.triggers import Timer

LOW = 0
HIGH = 1
CLOCK_PERIODS = 10
NANOSECONDS = "ns"







@cocotb.test()
async def smoke_test(dut):
    for _ in range (CLOCK_PERIODS):
        dut.clk.value = LOW
        await Timer(1, unit=NANOSECONDS)
        dut.clk.value = HIGH
        await Timer(1, unit=NANOSECONDS)
