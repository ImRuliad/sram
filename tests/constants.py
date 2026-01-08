import math
"""
This file should contain all constants used in testbenching.
"""

#Hardware parameters (MUST MATCH WITH RTL)
ROWS = 64
COLS = 64
DATA_WIDTH = 8
ROW_ADDR_WIDTH = math.ceil(math.log2(ROWS))
COL_ADDR_WIDTH = math.ceil(math.log2(COLS // DATA_WIDTH))

#Test timing constants
NANOSECONDS = "ns"
CLOCK_PERIOD_NS = 1000

#Logic Levels
LOW = 0
HIGH = 1

# 8-bit data patterns
ALL_ZEROES = 0x00
ALL_ONES = 0xFF
CHECKERBOARD_A = 0x55  # 01010101
CHECKERBOARD_B = 0xAA  # 10101010