# Generated code

Each interface is a `.proto` file in `proto/pnut/`; its numbers are in
`proto/interfaces.md`, never reused. `tools/generate.sh` runs protoc once
for all of them (`make gen`, or any build when they change) with two
plugins, into `build/gen`:

- **nanopb** writes the messages as fixed-size C structs
  (`<file>.pb.h`, `.pb.c`): every string and repeated field has a
  `max_size` or `max_count` in the `.proto`.
- **protoc-gen-pnut** (`tools/protoc-gen-pnut`) writes, from pnut's own
  options (`proto/pnut/options.proto`):

| File | From | Gives |
|---|---|---|
| `<file>.pnut.h`, `.c` | `service` (`pnut.iface`, `pnut.method`) | a client (`pnut_<iface>_connect()`, a call per method with its answer handler) and a server (`pnut_<iface>_serve()` with a struct of handlers, `_reply()`, `_fail()`) |
| `<file>.topics.h`, `.c` | a message with `pnut.topic` | `_advertise()`, `_publish()`, `_subscribe()` for it |
| `<file>.settings.h`, `.c` | a message with `pnut.settings` | the owner's schema, a cache that keeps the values in that struct up to date, and their indexes |

It also writes `descriptors.pb`, the whole set, which other tools read
(the board's description and the settings' defaults are checked against
it).

## Naming

An enum's values are prefixed with the enum's name, nanopb's way:
`HAPTICS_USE_RING` in `enum HapticsUse` becomes
`PNUT_HAPTICS_USE_HAPTICS_USE_RING`. A oneof says which member it holds
in `which_<oneof>`, by the member's tag, `PNUT_<MESSAGE>_<MEMBER>_TAG`.

!!! warning "Trap: a submessage needs its `has_` flag"
    In proto3 a field that is a message is optional: nanopb sends it only
    when its `has_<field>` is true. A Settings `Set` request's `value`
    left without `has_value = true` arrives empty.

!!! warning "Trap: one number, one interface"
    The generator refuses an interface number used twice; a method's
    number and version change only as RFC 0005 says (a new version when
    its messages change meaning).

## Limits

A message is 4 KB at most on the wire ([IPC](ipc.md)); a topic's message
is a fixed-size struct. A settings message holds at most as many settings
as an owner may have ([Topics and settings](topics-settings.md)).
