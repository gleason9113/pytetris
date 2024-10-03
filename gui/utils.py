# pytetris/gui/utils.py
# Helper functions related to the MainWindow class
from PyQt6.QtWidgets import QLayoutItem


def recursive_traverse(layout):
    """
    Recursively traverse the layout to print widget information.
    :param layout: QLayout to traverse.
    """
    for i in range(layout.count()):
        item = layout.itemAt(i)

        if isinstance(item, QLayoutItem):
            widget = item.widget()

            if widget:
                # Get widget information
                widget_type = widget.__class__.__name__
                geometry = widget.geometry()
                visibility = widget.isVisible()

                # Print out widget information
                print(f"Widget Type: {widget_type}")
                print(f"Geometry: {geometry}")
                print(f"Visible: {visibility}")

                # Check if widget is in the layout (if layout contains the widget)
                if layout.indexOf(widget) != -1:
                    print(f"In Layout: Yes")
                else:
                    print(f"In Layout: No")
                print('-' * 40)

            # Handle nested layouts (in case there are any sub-layouts)
            if isinstance(item, QLayoutItem) and item.layout():
                recursive_traverse(item.layout())


def print_layout_info(central_widget):
    """
    Prints layout information including geometry and visibility for every widget in the central widget layout.
    :param central_widget: The central widget of the MainWindow.
    """
    layout = central_widget.layout()
    if layout is not None:
        recursive_traverse(layout)
    else:
        print("No layout set for central widget.")
