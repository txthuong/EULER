# LTE Frequency Bands Module

UL = {
    1: (1920, 1980),
    2: (1850, 1910),
    3: (1710, 1785),
    4: (1710, 1755),
    5: (824, 849),
    7: (2500, 2570),
    8: (880, 915),
    9: (1749.9, 1794.9),
    10: (1710, 1770),
    11: (1427.9, 1447.9),
    12: (699, 716),
    13: (777, 787),
    14: (788, 798),
    17: (704, 716),
    18: (815, 830),
    19: (830, 845),
    20: (832, 862),
    21: (1447.9, 1462.9),
    22: (3410, 3490),
    23: (2000, 2020),
    24: (1626.5, 1660.5),
    25: (1850, 1915),
    26: (814, 849),
    27: (807, 824),
    28: (703, 748),
    30: (2305, 2313),
    31: (452.5, 457.5)
}

DL = {
    1: (2110, 2170),
    2: (1930, 1990),
    3: (1805, 1880),
    4: (2110, 2155),
    5: (869, 894),
    7: (2620, 2690),
    8: (925, 960),
    9: (1844.9, 1879.9),
    10: (2110, 2170),
    11: (1475.9, 1495.9),
    12: (729, 746),
    13: (746, 756),
    14: (758, 768),
    17: (734, 746),
    18: (860, 875),
    19: (875, 890),
    20: (791, 821),
    21: (1495.9, 1510.9),
    22: (3510, 3590),
    23: (2180, 2200),
    24: (1525, 1559),
    25: (1930, 1995),
    26: (859, 894),
    27: (852, 869),
    28: (758, 803),
    30: (2350, 2360),
    31: (462.5, 467.5)
}

DLEarfcn = {
    1: (0, 599),
    2: (600, 1199),
    3: (1200, 1949),
    4: (1950, 2399),
    5: (2400, 2649),
    7: (2750, 3449),
    8: (3450, 3799),
    9: (3800, 4149),
    10: (4150, 4749),
    11: (4750, 4949),
    12: (5010, 5179),
    13: (5180, 5279),
    14: (5280, 5379),
    17: (5730, 5849),
    18: (5850, 5999),
    19: (6000, 6149),
    20: (6150, 6449),
    21: (6450, 6599),
    22: (6600, 7399),
    23: (7500, 7699),
    24: (7700, 8039),
    25: (8040, 8689),
    26: (8690, 9039),
    27: (9040, 9209),
    28: (9210, 9659),
    30: (9770, 9869),
    31: (9870, 9919)
}

ULEarfcn = {
    1: (18000, 18599),
    2: (18600, 19199),
    3: (19200, 19949),
    4: (19950, 20399),
    5: (20400, 20649),
    7: (20750, 21449),
    8: (21450, 21799),
    9: (21800, 22149),
    10: (22150, 22749),
    11: (22750, 22949),
    12: (23010, 23179),
    13: (23180, 23279),
    14: (23280, 23379),
    17: (23730, 23849),
    18: (23850, 23999),
    19: (24000, 24149),
    20: (24150, 24449),
    21: (24450, 24599),
    22: (24600, 25399),
    23: (25500, 25699),
    24: (25700, 26039),
    25: (26040, 26689),
    26: (26690, 27039),
    27: (27040, 27209),
    28: (27210, 27659),
    30: (27660, 27759),
    31: (27760, 27809)
}

BW = {
    1: (5, 10, 15, 20),
    2: (1.4, 3, 5, 10, 15, 20),
    3: (1.4, 3, 5, 10, 15, 20),
    4: (1.4, 3, 5, 10, 15, 20),
    5: (1.4, 3, 5, 10),
    7: (5, 10, 15, 20),
    8: (1.4, 3, 5, 10),
    9: (5, 10, 15, 20),
    10: (5, 10, 15, 20),
    11: (5, 10),
    12: (1.4, 3, 5, 10),
    13: (5, 10),
    14: (5, 10),
    17: (5, 10),
    18: (5, 10, 15),
    19: (5, 10, 15),
    20: (5, 10, 15, 20),
    21: (5, 10, 15),
    22: (5, 10, 15, 20),
    23: (1.4, 3, 5, 10, 15, 20),
    24: (5, 10),
    25: (1.4, 3, 5, 10, 15, 20),
    26: (1.4, 3, 5, 10, 15),
    27: (1.4, 3, 5, 10),
    28: (3, 5, 10, 15, 20),
    30: (5, 10),
    31: (1.4, 3, 5)
}

        
def getUL(band):
    return UL[band]
    
def getDL(band):
    return DL[band]

def getBW(band):
    return BW[band]
    
def getULEarfcn(band):
    return ULEarfcn[band]
    
def getDLEarfcn(band):
    return DLEarfcn[band]
    
def getMaxBand():
    return max(BW)
    
def getMinBand():
    return min(BW)
    
def getBands():
    return BW.keys()
    
    