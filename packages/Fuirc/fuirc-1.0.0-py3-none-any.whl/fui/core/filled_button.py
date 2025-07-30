from fui.core.elevated_button import ElevatedButton


class FilledButton(ElevatedButton):
    """
    Filled buttons have the most visual impact after the FloatingActionButton (https://fui.dev/docs/controls/floatingactionbutton), and should be used for important, final actions that complete a flow, like Save, Join now, or Confirm.

    Example:
    ```
    import fui as ft


    def main(page: ft.Page):
        page.title = "Basic filled buttons"
        page.add(
            ft.FilledButton(text="Filled button"),
            ft.FilledButton("Disabled button", disabled=True),
            ft.FilledButton("Button with icon", icon="add"),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://fui.dev/docs/controls/filledbutton
    """

    def _get_control_name(self):
        return "filledbutton"
