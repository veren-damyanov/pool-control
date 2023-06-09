
GPIO_TABLE = (
    # Board-_pin-#, GPIO-#, Special Function
    (3, 2, 'SDA'),
    (5, 3, 'SCL'),
    (7, 4, 'GPCLK0'),
    (8, 14, 'TXD'),
    (10, 15, 'RXD'),
    (11, 17, None),
    (12, 18, 'PCM_CLK'),
    (13, 27, None),
    (15, 22, None),
    (16, 23, None),
    (18, 24, None),
    (19, 10, 'MOSI'),
    (21, 9, 'MISO'),
    (22, 25, None),
    (23, 11, 'SCLK'),
    (24, 8, 'CE0'),
    (26, 7, 'CE1'),
    # (27, 0, 'ID_SD'),  # gpiozero docs do not show this as 'GPIO-0', only as 'ID SD'
    # (28, 1, 'ID_SC'),  # pigpiod setting  GPIO-1 mode raises permission error (issue #15)
    (29, 5, None),
    (31, 6, None),
    (32, 12, 'PWM0'),
    (33, 13, 'PWM1'),
    (35, 19, 'PCM_FS'),
    (36, 16, None),
    (37, 26, None),
    (38, 20, 'PCM_DIN'),
    (40, 21, 'PCM_DOUT'),
)
