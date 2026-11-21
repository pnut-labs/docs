# Programs and modules

pnut-os is a few **programs**, each a NuttX task started by NxInit, each
running several **services** as **modules** of one event loop
([RFC 0007](https://github.com/pnut-labs/design/blob/master/rfcs/0007-services.md)).
`etc/pnut/programs` says which:

| Program | Services |
|---|---|
| `pnut_system` | Service states, Settings, Power, Time, Board, the log |
| `pnut_telephony` | Telephony (the modem, SMS, mobile data) |
| `pnut_network` | Wi-Fi, Network |
| `pnut_radios` | Radio (LoRa) |
| `pnut_sensors` | Location (GNSS), Motion |
| `pnut_data` | Messages, Storage |
| `pnut_media` | Haptics |
| `pnut_ui` | the system UI, Input |

The file also names services not built yet (Bluetooth, Contacts, Audio,
…): a program that does not run yet is harmless there.

!!! info "Why few programs, many modules"
    In NuttX's flat build every program shares one address space and the
    internal RAM is small (see [Device and tooling traps](../traps.md)).
    A program costs a task, its stack and its loop's buffers; a module
    costs a struct. Services that belong together share a program, and a
    crash takes down only that program.

## Starting and readiness

NxInit (NuttX's first task) reads `etc/init.d/pnut.rc` and starts the
programs. A program creates its loop, adds its modules, and runs the loop;
each module says when it can serve (`pnut_module_ready()`), and the
program is ready once all are — NxInit is told, and Service states knows
(RFC 0006). Stopping (`SIGTERM`) lets each module finish in order, within
`CONFIG_PNUT_LIB_FINISH` (2 s).

## Who a caller is

A service knows its caller's task from `SO_PEERCRED`; Service states'
`Who` turns the task into its program's name, and says whether it was
typed in a developer's shell (`console` or `adbd`, RFC 0012). Settings,
Time, the log, Telephony, Wi-Fi, Messages and the system UI decide what a
caller may do from that.

## The settings' owners

Each service owns the settings named after it (RFC 0025): `etc/pnut/programs`
tells Settings which program runs which services, so a program reaches its
own services' settings only. Every module whose loop has levels also owns
its log level, `log.level` ([Logging](logging.md)).
