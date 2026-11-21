# Messages

Messages, in the data program, is the device's store of text messages
([RFC 0029](https://github.com/pnut-labs/design/blob/master/rfcs/0029-messages.md)): conversations by transport and peer,
in files appended to. Transports (Telephony's SMS) register, deliver what
they receive, and take what is to be sent.

- `messages`, `messages show <conversation>`, `send <transport> <peer>
  <text>`, `read`, `delete` from the shell.
- A delivery is answered once it is kept; the `messages` topic says which
  conversation changed.

Interface: [Messages](../interfaces/messages.md). Code: `src/data/`.

!!! warning "Trap: SQLite"
    Tried, measured, dropped: on littlefs a commit rewrote nearly the whole
    database (12 s at 232 KB). See [Storage layout](../architecture/storage.md).
