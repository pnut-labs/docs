# pnut-os

pnut-os is a phone operating system on [NuttX](https://nuttx.apache.org/)
for the LilyGo T-Deck Max: an ESP32-S3, a 240 × 320 e-paper panel at one
bit, a Q20 keyboard and a touch layer, an LTE modem, Wi-Fi, LoRa, GNSS and
motion sensors. This site is for people working on it: how it is built and
tested, how its programs talk to each other, why things are the way they
are, and the traps found on the way.

## Where things are

| | |
|---|---|
| [pnut-labs/pnut-os](https://github.com/pnut-labs/pnut-os) | the system: its programs, the system UI, the apps, the tools and the tests |
| [pnut-labs/nuttx](https://github.com/pnut-labs/nuttx), [pnut-labs/nuttx-apps](https://github.com/pnut-labs/nuttx-apps) | the forks of NuttX and its apps: the board, its drivers, the kernel changes |
| [pnut-labs/design](https://github.com/pnut-labs/design) | the RFCs: what each part must do, decided before it is built |
| [pnut-labs/docs](https://github.com/pnut-labs/docs) | this site |

The RFCs say *what* and *why* at the level of the design; these pages say
*how* it was built, what each interface carries, and what surprised us.
They link to the RFCs rather than repeat them.

## Reading these pages

- **Interfaces** are written from the `.proto` files on pnut-os's master:
  every call, topic, setting, message and limit, with the comments from
  the code.
- Pages describe **master**: work on a branch brings its pages with its
  pull request.
- Two kinds of boxes stand out:

!!! info "Why"
    The reason for a rule that looks odd, and what was weighed against it.

!!! warning "Trap"
    Something that bit us: a hardware quirk, a tool that hangs, a test
    that passes for the wrong reason.
