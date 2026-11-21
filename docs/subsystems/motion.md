# Motion

Motion, in the sensors program, reads the BHI260AP sensor hub's virtual
sensors through NuttX's uORB topics ([RFC 0036](https://github.com/pnut-labs/design/blob/master/rfcs/0036-motion.md)),
each open only while wanted.

- Still or moving; the facing (up, down, upright, on its side) from three
  accelerometer readings, on the `motion` topic.
- Today's steps, kept in `/var/lib/motion/steps` (saved every 10 minutes
  while they change), started again at local midnight; the activity.
- Gestures (picked up, lifted to look) on the `gestures` topic, for the
  system UI.
- Settings `motion.steps`, `motion.wake`, `motion.face_down`.

Interface: [Motion](../interfaces/motion.md). Code: `src/sensors/`.

!!! warning "Trap: the first open uploads the hub's firmware"
    The hub has no firmware of its own: the first sensor opened uploads
    Bosch's image, which takes long enough that it runs on a worker. The
    image is fetched at build time at a pinned commit.
