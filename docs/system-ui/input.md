# Keys and input

Input, a module of the ui program, is the only reader of the keyboard,
the function keys and the touch layer the board's description names
([RFC 0027](https://github.com/pnut-labs/design/blob/master/rfcs/0027-input.md)). Keys become actions through RFC 0019's
key map (`keymap.c`):

| Key | Outside a text field |
|---|---|
| W, S, A, D | up, down, left, right |
| E, Enter | the primary action (Open, Select) |
| Q, Backspace | back |
| Alt + Enter | the screen's options |
| Space, Shift + Space | the next page, the previous |
| F1, F2, F3 (touch keys under the screen) | the left, middle and right softkeys |
| any other letter | a command letter of the options open |

In a text field the letters type; Backspace deletes; Enter confirms a
one-line field; Sym + Q leaves it, its text kept (Sym, right of Space, is
the Find key), and with Sym held W, S and E steer in a field too.

The steering keys (W, S, A, D), Space and Backspace repeat while held:
after half a second, 20 times a second. A letter being typed does not.

!!! info "Why letters steer"
    The Q20 keyboard has no arrows. W, A, S, D (and Q, E) steer, so a
    command letter is never one of them.

!!! info "Digits on the Q20"
    The digits are printed on letter keys; where a field wants a number (the
    SIM PIN), those letters type their digits (`keymap_digit()`).

A tap is a block's id sent to its screen: a row, a tile. A tap on a
softkey sends its key, as F1 to F3 would.
