# Service states

Service states, in the system program, knows which programs run, which
task is which program, and whether each is ready
([RFC 0006](https://github.com/pnut-labs/design/blob/master/rfcs/0006-manager.md)).

- **Who**: a service asks it who a caller is, from the caller's pid
  (`SO_PEERCRED`): the program's name, or that it was typed in a
  developer's shell (`console`, `adbd`).
- **Start**, **Stop**: the system UI starts an app's program through it.
- A program is ready once every module of its loop is; NxInit is told.
- After an update, the system program confirms the new firmware once
  every program has stayed ready for 10 s
  ([RFC 0013](https://github.com/pnut-labs/design/blob/master/rfcs/0013-firmware-updates.md)).

Interface: [Services](../interfaces/services.md). Code:
`src/system/states.c`; the update's confirm in `firmware.c`.
