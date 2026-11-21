# Screens and the stack

The system UI is the ui program, on LVGL 9.2 at one bit
([RFC 0019](https://github.com/pnut-labs/design/blob/master/rfcs/0019-system-ui.md)), drawn as the owner's design has it.
Its screens are a **stack**, Home at the foot:

| Screen | Code |
|---|---|
| Home: the date, the big clock, six shortcuts | `scr_home.c` |
| Menu: two pages of tiles, its folders | `scr_menu.c` |
| Settings | `scr_settings.c` |
| Wi-Fi, a network's join | `scr_wifi.c`, `scr_join.c` |
| Cellular | `scr_cell.c` |
| The SIM PIN, over any screen while the SIM asks | `scr_pin.c` |
| An app not built yet: "Not available yet" | `scr_unavailable.c` |
| An app's screen, in a template | `app.c`, `tpl_*.c` |

A screen is a class (`struct screen_class_s`): its build, its keys, its
taps, what it does when a status changes, its leave. `ui_push()` and
`ui_pop()` move the stack; a screen coming back on top is told every
status again.

Every screen has the **header** (the signal and battery meters, Wi-Fi's
icon, the time) and the **softkeys** at its foot (options, the primary
action, back), from `blocks.c`. Lists are `list.c`: rows of 40 px, a
heading of 20, the focused row inverted.

Other programs' settings are read and set through Settings' own calls
(`setting.c`), read again when the `settings` topic tells of a change.

!!! warning "Trap: a screen's state after it left"
    An answer can come after its screen went. Calls carry the screen's
    serial, never a pointer to it, and look it up when the answer comes
    (`ui_find()`): a screen gone finds nothing.
