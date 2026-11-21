# E-paper redraw rules

The panel is a 240 x 320 e-paper (UC8253): a partial refresh takes about
0.8 s, a full one 1.0 s, and partial refreshes leave ghosting. The system
UI draws by one rule (`redraw.c`, RFC 0019):

- Keys pressed within **500 ms** of the first are drawn once, at the end:
  one redraw per decision.
- A change no key caused (a topic, the clock) is drawn at once, or with
  the keys when they are being gathered.
- A **full refresh** is due after **5** partial ones, and taken at the
  next change of screen — **never while typing**.
- Only what differs from the panel is sent.

!!! info "Why gather keys"
    Every action costs a redraw of most of a second. Drawn after each key,
    W W W S would take four seconds and flicker; gathered, it is one.

!!! warning "Trap: a full refresh inverts the screen"
    A full refresh flashes the whole panel black and white. That is why it
    waits for a change of screen, and never comes while the owner types.

!!! warning "Trap: a refresh that never happened"
    NuttX's framebuffer layer discards the e-paper driver's answer to a
    refresh: a failed one shows no error. Time it instead (about 1 s is a
    real refresh).
