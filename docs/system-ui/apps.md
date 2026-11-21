# Templates and app hosting

Apps draw nothing themselves: they tell the system UI what to show, in
**templates** of its own, and it draws them as the owner's design has them
([RFC 0037](https://github.com/pnut-labs/design/blob/master/rfcs/0037-apps-and-the-system-ui.md)).

- `pnut.Ui` is served on `ui`. An app calls **Open**: the answer is a
  stream of events (Welcome first), as its credit allows.
- The app is known by Service states' Who; a program typed in the
  developer's shell gives its own id.
- One app at a time, so far.
- **Show** sends a whole screen: an id the app chooses, a template, its
  content, the focused item; or a **sheet** over it. **Update** changes
  parts of the screen on top; **Rows** answers a list's page needed;
  **Leave** ends.
- Templates: **List**, **Detail**, **Empty**, **Busy**; sheets
  **Confirm** and **Busy**. Options may carry command letters.

The events: **Welcome** (the display, rows per page, the languages, the
clock), **Input** (a row opened, an option chosen, the primary action,
back), **Page needed**, **Stop**.

`uidemo list|detail|empty|confirm|busy` from the shell shows each template
with made-up content and prints what the owner does.

Interface: [UI](../interfaces/ui.md). Code: `host.c` (the apps'
connections), `app.c`, `tpl_*.c`.
