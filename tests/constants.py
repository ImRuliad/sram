import math
"""
This file should contain all constants used in testbenching.
"""

#Hardware parameters (MUST MATCH WITH RTL)
ROWS: int  = 64
COLS: int = 64
DATA_WIDTH: int = 8
ROW_ADDR_WIDTH: int= math.ceil(math.log2(ROWS))
COL_ADDR_WIDTH: int = math.ceil(math.log2(COLS // DATA_WIDTH))

#Test timing constants
NANOSECONDS: str = "ns"
CLOCK_PERIOD_NS: int = 1000

#Logic Levels
LOW: int = 0
HIGH: int = 1

# 8-bit data patterns
ALL_ZEROES: int = 0x00
ALL_ONES: int = 0xFF
CHECKERBOARD_A: int = 0x55  # 01010101
CHECKERBOARD_B: int = 0xAA  # 10101010