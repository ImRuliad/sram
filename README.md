# Overview
*This is a simulation of the design, development, and testing of a 16Kb SRAM (Static Random Access Memory). Will scale to a larger size later.*

<u> Architecture </u>
- Each bit cell will be comrpised of a D Flip Flop
- Each cell array will be comprised of 64 rows and 64 columns, totalling to 4096 bit cells per bank.
- Each memory bank will contain a 64 x 64 cell array
- There will be 4 banks total in this SRAM, totalling to 4 x 4096 = 16Kb memory

<u> Purpose </u>
- pass
- pass
- pass

---

# Dependencies
- Python 3.13 or below (cocotb 2.0.1 does not support 3.14 as of 02/08/2026).
- [cocotb 2.0.1](https://docs.cocotb.org/en/stable/install.html) or above.
- [uv 0.9.15](https://github.com/astral-sh/uv) or above.
- [icarus-verilog](https://formulae.brew.sh/formula/icarus-verilog).

---

# Setup
- Clone the repo to a directory of your choosing.
- Run `uv sync` to download dependencies.
- Run `uv run make` to run all tests or run `uv run make <name of test>` to run specific tests.

