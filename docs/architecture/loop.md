# The event loop

Every program has one loop, made in its main thread
([RFC 0023](https://github.com/pnut-labs/design/blob/master/rfcs/0023-service-library.md),
`src/lib/include/pnut/loop.h`). Every call of libpnut takes it: the
library keeps no state of its own, since all programs share one address
space. Handlers — a descriptor ready, a timer due, an answer, a topic's
message — run on the loop's thread, one at a time.

## Sized when it is made

Everything a loop needs is taken when it is made, never later:

| Setting | Default | Is |
|---|---|---|
| `fds` | 16 (`CONFIG_PNUT_LIB_FDS`) | descriptors watched at once: each service, client, topic reader, device |
| `timers` | 16 | timers at once; each open client takes one |
| `jobs`, `workers` | 8, 1 | jobs for worker threads, and the threads |
| `budget` | 10 ms | a handler running longer is logged |
| `finish` | 2000 ms | the most the modules may take to stop |

A program that needs more says so; the system UI, which draws, has a
budget of 250 ms.

!!! warning "Trap: out of descriptors or timers"
    A loop's limits are hard: one more client or topic than its `fds`
    fails to open. Count what a program watches when adding to it.

## The budget

A handler that runs longer than the loop's budget is logged:
`A descriptor handler ran 460 ms; its budget is 250 ms`. Everything else
on that program waits meanwhile — the system UI's keys, a service's other
callers. Slow work (a file rewritten, a modem's long answer) goes to a
**job** on a worker thread (`pnut_job_submit()`): it gets a copy of its
input, calls none of the library's functions, and its result comes back to
the loop.

!!! warning "Trap: file reads per draw"
    Reading a small file from the flash is not free: the system UI once
    read an app's manifest for every line it drew and ran 700 ms. Keep
    what is read often.
