# Building

pnut-os builds NuttX with pnut-os's own programs in it, for three targets:

| Target | Is |
|---|---|
| `sim` | NuttX's simulator on the computer, `sim:nsh` |
| `qemu` | the ESP32-S3 in Espressif's QEMU, `esp32s3-devkit:qemu_debug` |
| `tdeck-max` | the LilyGo T-Deck Max, `lilygo-tdeck-max:full` |

## The tree

```sh
git clone --recursive https://github.com/pnut-labs/pnut-os.git
```

NuttX and nuttx-apps are submodules pinned to the commits pnut-os is
tested with ([pnut-labs/nuttx](https://github.com/pnut-labs/nuttx),
[pnut-labs/nuttx-apps](https://github.com/pnut-labs/nuttx-apps)). After a
pull that moves them: `git submodule update`; `make <target>` warns when
they differ.

## What you need

| For | Tools |
|---|---|
| every target | GNU make, kconfig-frontends, Python 3.11+ with kconfiglib, genromfs, xxd, protoc with Python's protobuf, curl (nanopb is fetched and checked against its checksum) |
| `sim` | gcc, zlib's headers |
| `qemu`, `tdeck-max` | Espressif's `xtensa-esp-elf` **14.2**, esptool, Espressif's QEMU |
| `tdeck-max` | the network while it builds (the IMU's firmware, MCUboot's sources, at pinned commits), CMake, MCUboot's `imgtool` |
| `make test` | cmocka and libsodium |

On Debian: `apt install kconfig-frontends python3-kconfiglib
protobuf-compiler python3-protobuf libcmocka-dev libsodium-dev`.

!!! warning "Trap: GCC 15"
    GCC 15 defaults to C23, which the Espressif HAL does not build with.
    Put the 14.2 toolchain first on the `PATH`.

!!! warning "Trap: ESP-IDF's Python"
    ESP-IDF's Python environment has a kconfiglib of its own that cannot
    read NuttX's Kconfig. When it comes first on the `PATH`, name another:
    `make tdeck-max PYTHON=/usr/bin/python3`.

## Commands

| Command | Does |
|---|---|
| `make <target>` | configures NuttX for the target, and builds it |
| `make <target> run` | `sim` on the computer (`poweroff` leaves), `qemu` in QEMU (Ctrl-A X leaves) |
| `make <target> flash` | builds it and writes it to the device ([Flashing](flashing.md)) |
| `make test` | the unit tests on the computer, and the system UI's screens compared with the images kept |
| `make <target> test` | the tests inside it: `sim` runs libpnut's in the simulator |
| `make gen` | the interfaces' code from their `.proto` files, into `build/gen` |
| `make style` | NuttX's `nxstyle` on pnut-os's C code |
| `make clean` | removes the build |

One target is configured at a time: building another configures afresh.

## How a build goes

1. `apps/external` becomes a link to `src/`, so nuttx-apps builds
   pnut-os's code with its own.
2. NuttX is configured with the board's configuration
   (`configs/<target>/target.mk` names it), then pnut-os's options,
   `configs/<target>/fragment.config`, are merged over it. Every option
   there must reach the final configuration: a misspelt one, or one whose
   dependencies are not met, stops the build.
3. pnut-os's `/etc` is staged in `build/etc`: the device's description
   (`board.toml`, compiled to `pnut/board.pb`) and the settings' defaults
   (`defaults.toml`, checked against the settings' schemas).
4. NuttX builds the image, with `build/etc` laid over the board's `/etc`.
   NxInit, NuttX's first task, reads `etc/init.d/pnut.rc` and starts
   pnut-os's programs.
5. For the T-Deck Max, MCUboot is built too.

!!! warning "Trap: running NuttX's make by hand"
    Built by NuttX's own make, the image lacks `pnut.rc` (the overlay is
    passed by pnut-os's Makefile), and NxInit starts nothing. Always build
    through `make <target>`.

!!! warning "Trap: the device build removes nxstyle"
    A `tdeck-max` build cleans NuttX's host tools, `nxstyle` with them.
    Build it again before `make style`:
    `make -C nuttx/tools -f Makefile.host nxstyle`.
