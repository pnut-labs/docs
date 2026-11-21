# IPC: services, clients, streams

A service is a module's interface, served on a local stream socket at
`<rundir>/<name>` (`/var/run/<name>`); a client connects to it by name
([RFC 0005](https://github.com/pnut-labs/design/blob/master/rfcs/0005-communication.md),
[RFC 0023](https://github.com/pnut-labs/design/blob/master/rfcs/0023-service-library.md)).
Their code is generated from the interface's `.proto`
([Generated code](generated.md)); the [Interfaces](../interfaces/index.md)
pages list every call.

## Messages

A message is a 16-byte header (little-endian: the protocol's version, the
kind, the interface's number, the method's number and version, the
status, a sequence number an answer repeats, the body's length, the app
on the runtime's connections, a stream's credit) and a nanopb body;
**4 KB at most**, header included. An answer carries a status:

| Status | Means |
|---|---|
| `OK` | done |
| `BUSY` | a queue is full: try later |
| `DENIED` | the caller may not |
| `NOTFOUND` | no such interface, method or thing |
| `INVALID` | does not parse, or asks the impossible |
| `UNAVAILABLE` | not ready, or the hardware is absent; also a lost connection |
| `TIMEOUT` | no answer in time (5 s by default) |
| `INTERNAL` | the service failed |
| `ENDED` | a stream is over |

A failed answer may carry a detail, `pnut.Error`: the interface's own error
code and a text.

## Calls in flight

A client has **8 calls in flight** at most (`CONFIG_PNUT_LIB_INFLIGHT`):
one more fails at once (`-EBUSY`). A service takes a connection's request
only when its send buffer has room for the answer beside the room kept
for the answers it owes; one more than 8 waiting is answered busy.

!!! warning "Trap: many calls at once"
    A loop that sends a call per item of a list runs out after 8. Send as
    there is room and go on as answers come back.

!!! warning "Trap: every call needs its answer handler"
    A call made with no handler is refused (`-EINVAL`), even when its
    answer does not matter.

## Connections

A client reconnects by itself when the connection is lost, waiting
100 ms at first and up to 5 s, and tells its state handler each time.
A service accepts 2 connections from one program at most (known by its
pid), so one program cannot take every connection.

## Streams and credit

A call may answer with a **stream** of items (Wi-Fi's scan, an app's
events, Radio's packets). The client gives **credit**, items it can take;
the service sends no more than that, and the stream ends with `ENDED` or
another status.

## Events

A service may send an event on a connection without a call; it needs room
beside every answer owed.
