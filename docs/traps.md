# Device and tooling traps

Things that bit us, gathered in one place; each subsystem's page has its
own. The hardware itself — its parts, pins and their quirks — is
described on the board's page in the NuttX fork:
[lilygo-tdeck-max](https://github.com/pnut-labs/nuttx/tree/master/Documentation/platforms/xtensa/esp32s3/boards/lilygo-tdeck-max).

## USB and the serial port

!!! warning "Never open the port while the chip sleeps"
    On battery the ESP32-S3 light-sleeps, and its USB goes with it.
    Opening the serial port then once made the computer give up on the
    device until it was unplugged. Tests that run on battery wait a fixed
    time before talking to the device again.

!!! warning "The port stays while the device is gone"
    The computer does not drop `/dev/ttyACM0` when the chip disconnects its
    USB: a script cannot wait for the port to vanish. Wait fixed times.

!!! warning "A new name after re-enumeration"
    After the USB link comes back, the port may be `/dev/ttyACM1`.

## Power

!!! warning "Never cut USB power from the console"
    Setting the charger's EN_HIZ (USB power cut, to measure the battery)
    takes the console with it. If the line restoring it is never written,
    the device stays on battery with its USB dead until a key or a reset.
    Start a separate restore on the device first, and check the script
    before running it.

## The modem

!!! warning "Never send `AT+ICF`"
    The modem reports `2,2`, which matches the chip's 8N1. `AT+ICF=3,0`
    cut the link until the modem was powered off and on.

!!! warning "Band and mode experiments"
    `AT+CNMP` and `AT+CNBP` can leave the modem searching for a network it
    never finds, drawing ~80 mA and not answering. Telephony's setup
    restores them at its start, but don't experiment with them on a phone
    in use.

## Memory

!!! info "Two heaps"
    With Wi-Fi on, the heap is split: **Kmem**, the internal RAM (about
    196 KB, of which some 36 KB is free on master), and **Umem**, the 8 MB
    PSRAM. Kmem runs out first: note `free` before and after a test.

!!! warning "A stack too small resets silently"
    A task's stack overflow can show as a reset loop with nothing printed:
    USB enumerates, writes time out, no prompt. A board init thread's stack
    of 2 KB did this once.

## Debugging with JTAG

!!! warning "Never leave hardware breakpoints armed"
    Killing gdb and OpenOCD can leave IBREAKENABLE and DBREAKC set. Without
    a debugger the next thread to hit one traps forever, `Ready` in `ps`
    and never running. End every session with `delete`,
    `monitor reg ibreakenable 0`, `monitor reg dbreakc0 0`,
    `monitor reg dbreakc1 0`, `monitor resume`, `detach` — or reset the
    board.

## The radios

!!! info "2.4 GHz only"
    The ESP32-S3's Wi-Fi is 2.4 GHz only: a phone's hotspot must offer it
    (on an iPhone, *Maximize Compatibility*).
