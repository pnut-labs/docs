# Theme

The theme is the owner's design at one bit: IBM Plex Sans and Plex Mono
in the sizes the design uses, and the owner's icons (`src/ui/theme/`).
They are made at build time into `build/ui` by `tools/mkfont.py` and
`tools/mkicons.py` (`make ... UI_PYTHON=`), with the pinned packages of
`tools/requirements.txt`.

| Fonts | Sizes |
|---|---|
| Sans | 11, 12, 13, 14; bold 12, 13, 14, 16 |
| Mono bold | 10, 11, 12; 26 and 36 (digits only: the clock, the PIN) |
| Icons | 11, 12, 14, 16, 18, 20 |

!!! info "Why pinned wheels"
    freetype-py and PyMuPDF bring their own FreeType and MuPDF, so the
    glyphs come out the same on every computer — and so do the screens'
    images the tests compare.

!!! warning "Trap: an icon added shifts the others"
    Icons are numbered in the order of their files. Adding one moves the
    code points of those after it; a test that pins a code point changes
    with it.
