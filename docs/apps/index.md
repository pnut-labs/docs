# Writing an app

On master an app is a program that talks to the system UI over `pnut.Ui`
([RFC 0037](https://github.com/pnut-labs/design/blob/master/rfcs/0037-apps-and-the-system-ui.md)); its start from Menu and
its life cycle come with RFC 0037's next steps. A program typed in the
developer's shell opens under the id it gives, reverse-DNS
(`org.pnut.demo`), and may show every template unless a manifest for that
id says otherwise. Any other app is named by its service and needs its
manifest, `/etc/apps/<id>.manifest` (`pnut.AppManifest`: its icon, its
name, the templates it may show), or Open is denied.
`src/commands/uidemo.c` is the example:

1. Connect a `pnut.Ui` client to `ui` and call **Open** with credit; keep
   giving credit as events are read.
2. On **Welcome**, **Show** the first screen: a template and its content.
3. Answer **Input** (a row opened, an option chosen, back) with a new
   Show, an Update, or Leave; answer **Page needed** with **Rows**.
4. On **Stop**, save and Leave. The system UI does not send Stop yet: it
   comes with the life cycle.

!!! info "Why templates, not pixels"
    The e-paper's redraw rules, the key map, the fonts and the owner's
    design are the system UI's. An app that sends content gets all of them,
    and works on the next device unchanged.

See [Templates and app hosting](../system-ui/apps.md) and the
[UI interface](../interfaces/ui.md).
