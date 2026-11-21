# Writing an app

On master an app is a program that talks to the system UI over `pnut.Ui`
([RFC 0037](https://github.com/pnut-labs/design/blob/master/rfcs/0037-apps-and-the-system-ui.md)); its start from Menu, a
manifest of its own and its life cycle come with RFC 0037's next steps.
`src/commands/uidemo.c` is the example:

1. Connect a `pnut.Ui` client to `ui` and call **Open** with credit; keep
   giving credit as events are read.
2. On **Welcome**, **Show** the first screen: a template and its content.
3. Answer **Input** (a row opened, an option chosen, back) with a new
   Show, an Update, or Leave; answer **Page needed** with **Rows**.
4. On **Stop**, save and Leave.

!!! info "Why templates, not pixels"
    The e-paper's redraw rules, the key map, the fonts and the owner's
    design are the system UI's. An app that sends content gets all of them,
    and works on the next device unchanged.

See [Templates and app hosting](../system-ui/apps.md) and the
[UI interface](../interfaces/ui.md).
