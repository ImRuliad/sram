import math
"""
This file should contain all constants used in testbenching.
"""

#Hardware parameters (MUST MATCH WITH RTL)
ROWS = 64
COLS = 64
ADDR_WIDTH = math.log2(ROWS)

#Test timing constants
NANOSECONDS = "ns"
CLOCK_PERIOD_NS = 2

#Logic Levels
LOW = 0
HIGH = 1

#Common Data Patterns
ALL_ZEROES = 0x0000000000000000
ALL_ONES = 0xFFFFFFFFFFFFFFFF
CHECKERBOARD_A = 0x5555555555555555  
CHECKERBOARD_B = 0xAAAAAAAAAAAAAAAA