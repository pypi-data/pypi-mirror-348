from fui.core.elevated_button import ElevatedButton


class Button(ElevatedButton):
    """
    Elevated buttons or Buttons are essentially filled tonal buttons with a shadow. To prevent shadow creep, only use them when absolutely necessary, such as when the button requires visual separation from a patterned background.

    Example:
    ```
    import fui as ft

    def main(page: ft.Page):
        page.title = "Basic buttons"
        page.add(
            ft.Button(text="Button"),
            ft.Button("Disabled button", disabled=True),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://fui.dev/docs/controls/elevatedbutton
    """
