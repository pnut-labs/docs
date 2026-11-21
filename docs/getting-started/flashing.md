# Flashing

```sh
make tdeck-max flash          # ESPTOOL_PORT, /dev/ttyACM0 by default
```

writes MCUboot, and the firmware into the first slot, confirmed. The image
is padded to the slot's 4 MB, which esptool compresses. The rest of the
flash is not written, so the system partition keeps its files: settings,
logs, messages, notifications survive a flash.

## The flash

| From | Size | What |
|---|---|---|
| `0x0` | 128 KB | MCUboot |
| `0x20000` | 4 MB | the first slot: the firmware that runs |
| `0x420000` | 4 MB | the second slot: an update, or the previous firmware |
| `0x820000` | 256 KB | free: MCUboot swaps the slots sector by sector, with no scratch area |
| `0x860000` | 64 KB | the device's data (RFC 0010), not used yet |
| `0x870000` | 2 MB | the system partition, littlefs, at `/var/lib` |
| `0xa70000` | 5.6 MB | free: for the package store (RFC 0009) |

## An update by hand

A firmware in the second slot marked for a trial is started at the next
start: MCUboot swaps the slots, so the previous firmware is kept. The
system program confirms the new one once every program has stayed ready
for 10 s; if the device starts again before that, MCUboot swaps them back.
A swap takes about 70 s for a 1.5 MB firmware, with a bar on the screen.
Until Packages installs updates, from a build's `nuttx/nuttx.hex`:

```sh
imgtool sign --pad --align 4 -v 0 -s auto -H 32 --pad-header \
  -S 0x400000 -M 1024 nuttx.hex trial.bin
esptool -p /dev/ttyACM0 write-flash 0x420000 trial.bin
```

## Test images

A branch is tried on the phone as an image of its own; the phone goes
back to master afterwards, so it never stays on a test image.

- Note `free` before and after a test: Kmem (the internal RAM) is the one
  that runs out first.

!!! warning "Trap: the port's name after a re-enumeration"
    After the USB link comes back (a reset, the charger's power cut), the
    port may return as `/dev/ttyACM1`. Set `ESPTOOL_PORT`.

!!! warning "Trap: a program that asserts at its start"
    The board resets on an assertion; a pnut-os program that asserts as it
    starts resets it in a loop. Flash a fixed image to get out.
