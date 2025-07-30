
# pysimpledraw
pysimpledraw is a simple drawing application built with Python, using `FreeSimpleGUI` for the graphical user interface and `tkinter` for canvas operations. It allows users to create and manipulate basic shapes, add text, import images, and perform common drawing operations.

## Why pysimpledraw?

pysimpledraw aims to provide a lightweight and easy-to-use drawing tool for quick sketches, annotations, or simple diagrams. It serves as a demonstration of how to integrate `FreeSimpleGUI` with `tkinter` for creating interactive graphical applications.

## Features

*   **Drawing Tools**: Rectangle, Circle, Line, Freehand, Triangle, Diamond.
*   **Text Tool**: Add and edit text on the canvas.
*   **Color Palette**: Predefined colors (Black, Red, Green) and a custom color chooser.
*   **Line Thickness**: Thin and Thick options.
*   **Eraser**: Remove objects from the canvas.
*   **Object Manipulation**:
    *   Select and move objects.
    *   Delete selected objects.
    *   Resize text (Small, Medium, Large via context menu).
    *   Resize imported images (via context menu with preset ratios).
*   **Image Import**:
    *   Import an image as a background.
    *   Import pictures as draggable and resizable objects.
*   **Canvas Operations**:
    *   Clear All: Resets the canvas.
    *   Undo/Redo: Revert and reapply actions.
    *   Save: Save the current canvas content as an image (e.g., PNG).
    *   Pan: Right-click and drag on empty canvas space.
*   **Context Menus**:
    *   Middle-click on text objects for size options.
    *   Middle-click on image objects for resize options.
*   **Keyboard Shortcuts**: Quick access to tools and actions.

## Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repository-link>
    cd pysimpledraw
    ```
2.  **Ensure Python is installed.** (Python 3.6+ recommended)
3.  **Install dependencies:**
    The application relies on `FreeSimpleGUI`, `Pillow` (PIL), and `pyperclip`. You can install them using pip:
    ```bash
    pip install FreeSimpleGUI Pillow pyperclip
    ```
    Or, if a `requirements.txt` file is provided:
    ```bash
    pip install -r requirements.txt
    ```
    (Note: A `pyproject.toml` is present, which might be used with tools like Poetry or Hatch for dependency management. If so, follow their respective installation procedures.)

## Usage

### As a Standalone Script

Navigate to the directory containing `main.py` (e.g., `pysimpledraw`) and run:

```bash
python main.py
```

### As a Package (using -m)

If `pysimpledraw` is structured as a runnable package (e.g., with an `__main__.py` or if `main.py` is intended to be run this way), you might be able to run it from the parent directory (`pysimpledraw`):

```bash
python -m pysimpledraw.main
```
(This assumes `pysimpledraw` is in your Python path or you are in the `pysimpledraw` directory which contains `pysimpledraw`.)

## GUI Features and Operations

The application window is divided into sections: Instructions, Tools, and the Canvas.

### Instructions Panel

*   **Mouse**:
    *   **Left Button**: Draw shapes or add text (double-click).
    *   **Middle Button**: Access context menus for text (size) or images (resize).
    *   **Right Button**: Select objects, move selected objects, or pan the canvas (if clicking on empty space).
*   **Double Click**:
    *   On an existing text object: Edit the text.
    *   On an empty area: Place new text.
*   **Shortcuts**: See the "Keyboard Shortcuts" section below.

### Tools Panel

#### Shape Tools:
*   **`r ectangle`**: Selects the rectangle drawing tool.
*   **`c ircle`**: Selects the circle drawing tool.
*   **`t line`**: Selects the line drawing tool.
*   **`f ree`**: Selects the freehand drawing tool.
*   **`T riangle`**: Selects the triangle drawing tool.
*   **`d iamond`**: Selects the diamond drawing tool.
*   **`e rase`**: Selects the eraser tool (click on an object to delete it).

#### Color Tools:
*   **`Black`**, **`Red`**, **`Green`**: Set the current drawing color.
*   **`...` (Custom Color)**: Opens a color chooser dialog.

#### Thickness Tools:
*   **`1 Thin`**: Sets line thickness to thin.
*   **`2 Thick`**: Sets line thickness to thick.

#### Action Buttons:
*   **`Clear All`**: Clears all drawings from the canvas.
*   **`Undo`**: Reverts the last action.
*   **`Redo`**: Reapplies the last undone action.
*   **`Save`**: Opens a dialog to save the canvas content as an image file.
*   **`Import Background`**: Imports an image to set as the canvas background.
*   **`Import Picture`**: Imports an image as a movable and resizable object on the canvas.

### Canvas

*   The main drawing area.
*   Supports panning by right-clicking and dragging on an empty area.
*   Objects can be selected by right-clicking on them. Multiple objects can be selected by right-clicking and dragging a selection box (though this feature might depend on the exact implementation details for multi-select).

## Keyboard Shortcuts

The application supports the following keyboard shortcuts:

*   **Shape Selection:**
    *   `r`: Rectangle
    *   `c`: Circle
    *   `t`: Line
    *   `f`: Freehand
    *   `T` (Shift + t): Triangle
    *   `d`: Diamond
    *   `e`: Eraser
*   **Color Selection:**
    *   `B` (Shift + b): Black
    *   `R` (Shift + r): Red
    *   `G` (Shift + g): Green
*   **Thickness Selection:**
    *   `1`: Thin
    *   `2`: Thick
*   **Object Deletion:**
    *   `Delete`: Deletes the currently selected object(s).

## Contributing

Found a bug or have a feature request? Please open an issue on the GitHub repository.

**GitHub Repository:** [https://github.com/fxyzbtc/pysimpledraw]


