from microbit import display, Image, sleep

# Length of one Morse timing unit in milliseconds.
# Increase this value to make the signal easier to read.
UNIT = 250

LIGHT = Image(
    "99999:"
    "99999:"
    "99999:"
    "99999:"
    "99999"
)

# Positive numbers: LEDs on
# Negative numbers: LEDs off
# Values represent Morse timing units.
SIGNAL = (
     3, -1,  1, -1,  3, -1,  1, -3,
     1, -1,  1, -1,  1, -1,  1, -3,
     1, -3,
     3, -1,  1, -1,  3, -1,  1, -3,
     3, -1,  1, -1,  3, -7,

     1, -1,  3, -1,  3, -3,
     1, -1,  1, -3,
     3, -3,
     1, -1,  1, -1,  1, -1,  1, -7,

     1, -1,  1, -1,  1, -3,
     1, -3,
     3, -1,  1, -1,  3, -1,  1, -3,
     1, -1,  1, -1,  3, -3,
     1, -1,  3, -1,  1, -3,
     1, -1,  1, -3,
     3, -3,
     3, -1,  1, -1,  3, -1,  3
)


def transmit():
    for duration in SIGNAL:
        if duration > 0:
            display.show(LIGHT)
            sleep(duration * UNIT)
        else:
            display.clear()
            sleep(abs(duration) * UNIT)

    display.clear()


while True:
    transmit()

    # Pause before transmitting the signal again.
    sleep(3000)
