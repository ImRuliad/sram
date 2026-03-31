import cocotb
from cocotb.handle import SimHandleBase
from cocotb.triggers import Timer

import tests.constants as constants


@cocotb.test()
async def generate_clock_cycle(dut: SimHandleBase) -> None:
    dut.clk.value = constants.LOW
    await Timer(1, unit=constants.NANOSECONDS)
    dut.clk.value = constants.HIGH
    await Timer(1, unit=constants.NANOSECONDS)


@cocotb.test()
async def smoke_test(dut: SimHandleBase) -> None:
    for _ in range(constants.CLOCK_PERIOD_NS):
        await generate_clock_cycle(dut)
