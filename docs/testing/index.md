# Testing

| Command | Runs |
|---|---|
| `make test` | the unit tests on the computer (cmocka), and the system UI's screens compared with the images kept |
| `make sim test` | libpnut's tests, and the system program's (Board, Power, Settings and its cache, Service states, Time's clock), inside NuttX's simulator; the list is in `configs/sim/target.mk` |
| `make style` | NuttX's `nxstyle` on the C code |

CI (`.github/workflows/build.yml`) runs the three on every pull request.

## Unit tests and fakes

`tests/unit/test_*.c` build the program's own sources on the computer with
a real libpnut loop: a test runs **steps at times** on the loop (a timer
each) and checks what happened. A service under test talks to **fakes** —
small servers of the interfaces it calls, written in the test — over the
same sockets as on the device; topics are published by the test. The
system UI's tests run real LVGL on a framebuffer in memory.

!!! info "Why real loops, not mocks"
    The bugs worth catching are in the order of things: an answer after
    its screen went, a call with no room, a topic's last message. A real
    loop with fake services meets them; a mock of the library would not.

## Screens

A UI test saves what it draws (`save("name")`) as a 1-bit picture;
`make test` compares every one with `tests/screens/<name>.png`, pixel for
pixel. `make screens` writes the images again after a change meant to
show: the pull request shows the change as images.

## Proving a test can fail

A test that has never failed proves nothing. Write it first and see it
fail; when it is written after the code, break the code on purpose — the
rule the test is for — and see that test fail, then put it back.

!!! warning "Trap: a test failing for the wrong reason"
    After a failure the loop may be left half torn down: the next tests
    fail at their setup (`0xfffffffffffffff0 != 0`). Read the first
    failure, not the count.

## On the phone

Test images and the phone's shell: [Flashing](../getting-started/flashing.md),
[The shell over serial](../getting-started/shell.md). A test on the phone
never uses its owner's real data: made-up apps, made-up messages, no
sends, no deletes.
