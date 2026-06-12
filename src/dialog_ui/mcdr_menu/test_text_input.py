from mcdreforged.api.all import RHoverText, RTextTranslation

from dialog_ui.dialog_component import DialogInputsText, DialogMultiAction
from dialog_ui.dialog_component.action import DialogActionRunCommandDynamic
from dialog_ui.utils import dict_to_json_file

dialog = DialogMultiAction(
    title=RTextTranslation("mcdr_menu.test_text_input.title").fallback(
        "Test Text Input."
    ),
    inputs=[
        DialogInputsText(
            key="text_input",
            label=RTextTranslation("mcdr_menu.test_text_input.inputs_label")
            .fallback("Text Input.")
            .set_hover_event(
                RHoverText(
                    RTextTranslation("mcdr_menu.test_text_input.inputs_hover").fallback(
                        "Please input the text here you want to send."
                    )
                )
            ),
        )
    ],
    pause=False,
    actions=[DialogActionRunCommandDynamic("say $(text_input)")],
)


if __name__ == "__main__":
    print(dialog.to_dict())
    dict_to_json_file(dialog.to_dict(), "_test_text_input.json")
