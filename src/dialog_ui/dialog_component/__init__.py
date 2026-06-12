"""Dialog component module - provides easy access to all dialog-related classes."""

from dialog_ui.dialog_component.action import (
    DialogAction,
    DialogActionBase,
    DialogActionChangePage,
    DialogActionCopyToClipboard,
    DialogActionCustom,
    DialogActionCustomDynamic,
    DialogActionOpenUrl,
    DialogActionRunCommand,
    DialogActionRunCommandDynamic,
    DialogActionShowDialog,
    DialogActionSuggestCommand,
)
from dialog_ui.dialog_component.base import (
    DialogBase,
    DialogNoticeAction,
)
from dialog_ui.dialog_component.body import (
    DialogBodyBase,
    DialogBodyItem,
    DialogBodyItemDescription,
    DialogBodyItemObject,
    DialogBodyPlainMessage,
)
from dialog_ui.dialog_component.dialogs import (
    DialogConfirmation,
    DialogList,
    DialogMultiAction,
    DialogNotice,
    DialogServerLinks,
)
from dialog_ui.dialog_component.inputs import (
    DialogInputsBase,
    DialogInputsBoolean,
    DialogInputsNumberRange,
    DialogInputsSingleOption,
    DialogInputsSingleOptionCompound,
    DialogInputsText,
    DialogInputsTextMultiline,
)
from dialog_ui.dialog_component.types import (
    DialogActionType,
    DialogActionTypeDynamic,
    DialogAfterActionOperation,
    DialogBodyType,
    DialogInputsType,
    DialogType,
    check_if_type_matched,
)

__all__ = [
    "DialogAction",
    # Action classes
    "DialogActionBase",
    "DialogActionChangePage",
    "DialogActionCopyToClipboard",
    "DialogActionCustom",
    "DialogActionCustomDynamic",
    "DialogActionOpenUrl",
    "DialogActionRunCommand",
    "DialogActionRunCommandDynamic",
    "DialogActionShowDialog",
    "DialogActionSuggestCommand",
    "DialogActionType",
    "DialogActionTypeDynamic",
    "DialogAfterActionOperation",
    "DialogBase",
    # Body classes
    "DialogBodyBase",
    "DialogBodyItem",
    "DialogBodyItemDescription",
    "DialogBodyItemObject",
    "DialogBodyPlainMessage",
    "DialogBodyType",
    # Dialog classes
    "DialogConfirmation",
    # Input classes
    "DialogInputsBase",
    "DialogInputsBoolean",
    "DialogInputsNumberRange",
    "DialogInputsSingleOption",
    "DialogInputsSingleOptionCompound",
    "DialogInputsText",
    "DialogInputsTextMultiline",
    "DialogInputsType",
    "DialogList",
    "DialogMultiAction",
    "DialogNotice",
    "DialogNoticeAction",
    "DialogServerLinks",
    # Types
    "DialogType",
    "check_if_type_matched",
]
