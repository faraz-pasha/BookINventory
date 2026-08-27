from PySide6.QtWidgets import QMessageBox


def show_message(
    parent,
    title,
    text,
    icon=QMessageBox.Information,
    informative_text=None,
):

    message = QMessageBox(
        parent
    )

    message.setObjectName(
        "appMessageBox"
    )

    message.setWindowTitle(
        title
    )

    message.setIcon(
        icon
    )

    message.setText(
        text
    )

    if informative_text:

        message.setInformativeText(
            informative_text
        )

    message.setStandardButtons(
        QMessageBox.Ok
    )

    message.exec()


def show_confirmation(
    parent,
    title,
    text,
    informative_text=None,
):

    message = QMessageBox(
        parent
    )

    message.setObjectName(
        "appMessageBox"
    )

    message.setWindowTitle(
        title
    )

    message.setIcon(
        QMessageBox.Warning
    )

    message.setText(
        text
    )

    if informative_text:

        message.setInformativeText(
            informative_text
        )

    message.setStandardButtons(
        QMessageBox.Yes
        | QMessageBox.No
    )

    message.setDefaultButton(
        QMessageBox.No
    )

    return (
        message.exec()
        == QMessageBox.Yes
    )