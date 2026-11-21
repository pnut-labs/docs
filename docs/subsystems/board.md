# Board

Board, in the system program, describes the device to the other programs
([RFC 0024](https://github.com/pnut-labs/design/blob/master/rfcs/0024-board.md)): its parts, which bus and lines each is
on, its battery, its radios' bands. The description is the target's
`configs/<target>/board.toml`, checked at build time against
`pnut.BoardDescription` and compiled into `/etc/pnut/board.pb`; Board
reads it at start and serves it whole.

- Programs open a part from what Board says — the modem's UART and its
  power key, the screen, the vibration motor, the GNSS receiver — never
  from a path of their own.
- Every unit is unprovisioned for now: there is no per-device data yet.
- **Airplane mode** is Board's setting, announced on the
  `airplane_mode` topic: Telephony and Radio switch their radios off.

Interface: [Board](../interfaces/board.md). Code: `src/system/board.c`.

!!! info "Why a description"
    The same programs run on the simulator, in QEMU and on the phone; the
    next device will differ. What differs lives in one file per target.
