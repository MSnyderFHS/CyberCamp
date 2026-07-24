"""Receive the Potomac Panther's final clue on a BBC micro:bit.

Flash this file to each student's micro:bit as ``main.py``. It listens for
the numbered packets sent by ``panther_final_clue_transmitter.py``, stores
each packet once, and prints the complete letter to the USB serial screen in
the micro:bit Python editor.

Controls:
    Button A: print the completed letter to serial again.
    Button B: show how many of the 36 packets have arrived.
"""

from microbit import Image, button_a, button_b, display, sleep
import radio


RADIO_CHANNEL = 7
RADIO_GROUP = 42
PACKET_LENGTH = 64
TOTAL_PACKETS = 36

packets = [None] * TOTAL_PACKETS
received_count = 0
letter_ready = False
letter_shown = False


def accept_packet(message):
    """Store a valid numbered packet and return True when all have arrived."""
    global received_count

    slash = message.find("/")
    space = message.find(" ")

    if slash < 1 or space < slash + 2:
        return False

    try:
        number = int(message[:slash])
        total = int(message[slash + 1:space])
    except ValueError:
        return False

    if total != TOTAL_PACKETS or number < 1 or number > TOTAL_PACKETS:
        return False

    index = number - 1
    if packets[index] is None:
        packets[index] = message[space + 1:]
        received_count += 1

        # Show packet-reception progress without blocking the radio loop.
        display.show(
            str(received_count),
            delay=100,
            wait=False,
            loop=False,
            clear=True,
        )

    return received_count == TOTAL_PACKETS


def print_letter():
    """Print the reassembled letter to the Python editor's serial screen."""
    display.show(Image.YES)

    print("")
    print("=" * 46)
    print("A FINAL LETTER FROM THE POTOMAC PANTHER")
    print("=" * 46)
    print("")

    paragraph = ""

    for text in packets:
        if text == "---":
            if paragraph:
                print(paragraph)
                paragraph = ""
            print("")
        else:
            if paragraph:
                paragraph += " "
            paragraph += text

    if paragraph:
        print(paragraph)

    print("")
    print("=" * 46)
    print("Press button A to print this letter again.")
    print("=" * 46)
    print("")
    display.show(Image.YES)


radio.config(
    channel=RADIO_CHANNEL,
    group=RADIO_GROUP,
    length=PACKET_LENGTH,
    queue=10,
)
radio.on()

# A target means the micro:bit is listening for the Panther's transmission.
display.show(Image.TARGET)

while True:
    if not letter_ready:
        incoming = radio.receive()

        if incoming == "PANTHER LETTER START":
            display.show(Image.TARGET)
        elif incoming == "PANTHER LETTER END":
            # Keep partial packets. The transmitter repeats, so missing
            # packets can be filled in during the next broadcast.
            if received_count < TOTAL_PACKETS:
                display.show(
                    str(received_count),
                    delay=150,
                    wait=False,
                    loop=False,
                    clear=True,
                )
        elif incoming:
            letter_ready = accept_packet(incoming)

        if button_b.was_pressed():
            display.show(
                str(received_count),
                delay=150,
                wait=False,
                loop=False,
                clear=True,
            )
    else:
        if not letter_shown:
            # Nothing else is needed from the radio once the letter is whole.
            radio.off()
            print_letter()
            letter_shown = True
            button_a.was_pressed()  # Clear any earlier button A press.
        elif button_a.was_pressed():
            print_letter()
        elif button_b.was_pressed():
            display.scroll(
                str(received_count) + "/" + str(TOTAL_PACKETS),
                delay=80,
            )
            display.show(Image.YES)

    sleep(20)
