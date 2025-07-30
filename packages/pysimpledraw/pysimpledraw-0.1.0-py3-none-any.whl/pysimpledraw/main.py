import FreeSimpleGUI as sg
import tkinter as tk
from tkinter import simpledialog, colorchooser, filedialog
import math
import copy
import os
from PIL import Image, ImageGrab, ImageTk
from io import BytesIO
import pyperclip

class DrawingApp:
    def __init__(self):
        # Initialize select_mode early to avoid reference errors
        self.select_mode = False

        # Create the FreeSimpleGUI window and the canvas
        self.setup_window()
        
        # State variables
        self.current_shape = "rectangle"  # Default shape
        self.current_color = "black"      # Default color
        self.current_thickness = "thin"   # Default line thickness
        self.start_x = None
        self.start_y = None
        self.current_obj = None
        self.selected_obj = None
        self.line_start = None
        self.objects = {}  # Store objects with their coordinates and properties
        self.move_start_x = None
        self.move_start_y = None
        self.canvas_x = 0  # For canvas.scan_dragto if needed
        self.canvas_y = 0  # For canvas.scan_dragto
        self.scale = 1.0
        self.preview_line = None
        self.is_panning = False  # New flag for canvas panning

        self.undo_stack = []  # For undo functionality
        self.redo_stack = []  # For redo functionality

        # Background Image
        self.bg_image_pil = None
        self.bg_image_tk = None # Keep a reference to avoid garbage collection

        # For imported image objects
        self.active_pil_images = {} # {tag: PIL.Image object (original)}
        self.tk_image_references = {} # {tag: ImageTk.PhotoImage object (current for display)}
        
        # State for image resizing
        self.is_resizing_image = False
        self.resize_corner = None  # e.g., "tl", "tr", "bl", "br"
        self.resize_obj_tag = None
        self.original_resize_coords = None # Coords of image at start of resize op

        # State for object dragging (general)
        self.selected_obj_for_drag = False # Flag if a drag operation on selected items is active
        self.pan_start_x = 0 # For canvas panning
        self.pan_start_y = 0 # For canvas panning
        
        # Initial UI update for buttons
        self.update_button_visuals()
        
        # Context menu for text objects
        self.text_context_menu = tk.Menu(self.window.TKroot, tearoff=0)
        self.text_context_menu.add_command(label="Small", command=lambda: self.change_text_size_preset("small"))
        self.text_context_menu.add_command(label="Medium", command=lambda: self.change_text_size_preset("medium"))
        self.text_context_menu.add_command(label="Large", command=lambda: self.change_text_size_preset("large"))
        
        # Context menu for image objects
        self.image_context_menu = tk.Menu(self.window.TKroot, tearoff=0)
        self.image_context_menu.add_command(label="1/4 Size", command=lambda: self.resize_selected_image(0.25))
        self.image_context_menu.add_command(label="1/2 Size", command=lambda: self.resize_selected_image(0.5))
        self.image_context_menu.add_command(label="3/4 Size", command=lambda: self.resize_selected_image(0.75))
        self.image_context_menu.add_command(label="*2 Size", command=lambda: self.resize_selected_image(2.0))
        self.image_context_menu.add_command(label="*3 Size", command=lambda: self.resize_selected_image(3.0))
        self.image_context_menu.add_command(label="*4 Size", command=lambda: self.resize_selected_image(4.0))

        # Selection mode state
        self.selected_objs = set()  # For multi-selection
        self.middle_clicked_obj_tag = None # For context menus
        
    def setup_window(self):
        # Define the menu layout
        menu_def = [
            ['Edit', ['Undo', 'Redo', 'Clear All']],
            ['Help', ['About']]
        ]
        
        # Define the layout
        layout = [
            [sg.Menu(menu_def, key='-MENU-')],
            [
            sg.Frame('Instructions', [
                [sg.Text('Mouse: left button to draw, middle button to menu, right button to select, move, pan')],
                [sg.Text('Double click to place text or edit text')],
                [sg.Text('Use shortcuts: 1: thin, 2:thick, r: rectangle, c: circle, t: line, f: free, T: triangle, d: diamond, e: erase')],
            ], expand_x=True, element_justification='center'),
            ],
            [
            sg.Frame('Tools', [                    [
                sg.Button('r ectangle', key='-RECTANGLE-', button_color=('white', 'lightgray')),
                sg.Button('c ircle', key='-CIRCLE-', button_color=('white', 'lightgray')),
                sg.Button('t line', key='-LINE-', button_color=('white', 'lightgray')),
                sg.Button('f ree', key='-FREE-', button_color=('white', 'lightgray')),
                sg.Button('T riangle', key='-TRIANGLE-', button_color=('white', 'lightgray')),
                sg.Button('d iamond', key='-DIAMOND-', button_color=('white', 'lightgray')),
                sg.Button('e rase', key='-ERASE-', button_color=('white', 'lightgray'))
                ],
                [
                sg.Button('Black', key='-BLACK-', size=(6, 1), button_color=('white', 'black')),
                sg.Button('Red', key='-RED-', size=(6, 1), button_color=('white', 'red')),
                sg.Button('Green', key='-GREEN-', size=(6, 1), button_color=('white', 'green')),
                sg.Button('...', key='-CUSTOM-COLOR-', size=(3, 1), button_color=('white', 'gray')),
                ],
                [
                sg.Button('1 Thin', key='-THIN-', button_color=('white', 'lightgray')),
                sg.Button('2 Thick', key='-THICK-', button_color=('white', 'lightgray')),
                ],                [
                sg.Button('Clear All', key='-CLEAR-', button_color=('white', 'gray')),
                sg.Button('Undo', key='-UNDO-', button_color=('white', 'gray')),
                sg.Button('Redo', key='-REDO-', button_color=('white', 'gray')),
                sg.Button('Save', key='-SAVE-', button_color=('white', 'gray'))
                ],
                [ # New row for import buttons
                sg.Button('Import Background', key='-IMPORT-BACKGROUND-', button_color=('white', 'gray')),
                sg.Button('Import Picture', key='-IMPORT-PICTURE-', button_color=('white', 'gray')),
                ]
            ], expand_x=True, element_justification='center')
            ],
            [sg.Canvas(size=(800, 600), key='-CANVAS-', background_color='white', expand_x=True, expand_y=True)],
        ]
        
        # Create the window
        self.window = sg.Window('Drawing App', layout, finalize=True, resizable=True)
        
        # Get the tkinter canvas from PySimpleGUI
        self.canvas_widget = self.window['-CANVAS-'].TKCanvas
        self.canvas = self.canvas_widget
        
        # Set up canvas bindings
        self.canvas_widget.bind("<Button-1>", self.start_draw)
        self.canvas_widget.bind("<B1-Motion>", self.draw)
        self.canvas_widget.bind("<ButtonRelease-1>", self.end_draw)
        # self.canvas_widget.bind("<Double-Button-1>", self.add_text) # Changed to edit_text_or_add
        self.canvas_widget.bind("<Double-Button-1>", self.handle_double_click)


        # Right mouse button (Button-3) for selecting and moving
        self.canvas_widget.bind("<ButtonPress-3>", self.start_right_drag_select) 
        self.canvas_widget.bind("<B3-Motion>", self.right_drag_select) 
        self.canvas_widget.bind("<ButtonRelease-3>", self.end_right_drag_select) 

        # Middle mouse button (Button-2) for context menus and potentially other actions
        self.canvas_widget.bind("<ButtonPress-2>", self.handle_middle_mouse_press)
        self.canvas_widget.bind("<ButtonRelease-2>", self.handle_middle_mouse_release)


        # Bind Configure event for canvas resize (for background image)
        self.canvas_widget.bind("<Configure>", self.on_canvas_resize)

          # Keyboard shortcuts
        self.window.TKroot.bind("<KeyPress-r>", lambda e: self.set_shape("rectangle"))
        self.window.TKroot.bind("<KeyPress-c>", lambda e: self.set_shape("circle"))
        self.window.TKroot.bind("<KeyPress-t>", lambda e: self.set_shape("line"))
        self.window.TKroot.bind("<KeyPress-f>", lambda e: self.set_shape("free"))
        self.window.TKroot.bind("<KeyPress-T>", lambda e: self.set_shape("triangle"))
        self.window.TKroot.bind("<KeyPress-d>", lambda e: self.set_shape("diamond"))
        self.window.TKroot.bind("<KeyPress-e>", lambda e: self.set_shape("erase"))
        
        self.window.TKroot.bind("<KeyPress-B>", lambda e: self.set_color("black"))
        self.window.TKroot.bind("<KeyPress-R>", lambda e: self.set_color("red"))
        self.window.TKroot.bind("<KeyPress-G>", lambda e: self.set_color("green"))
        
        self.window.TKroot.bind("<KeyPress-1>", lambda e: self.set_thickness("thin"))
        self.window.TKroot.bind("<KeyPress-2>", lambda e: self.set_thickness("thick"))
        self.window.TKroot.bind("<KeyPress-Delete>", lambda e: self.delete_selected_object())
        
    def delete_selected_object(self):
        deleted_something = False
        if self.selected_objs:
            self.save_state_for_undo() # Save state before deleting multiple objects
            for tag in list(self.selected_objs): # Iterate over a copy for safe deletion
                obj_ids = self.canvas.find_withtag(tag)
                if obj_ids:
                    self.canvas.delete(obj_ids[0])
                if tag in self.objects:
                    del self.objects[tag]
                if tag in self.active_pil_images:
                    del self.active_pil_images[tag]
                if tag in self.tk_image_references:
                    del self.tk_image_references[tag]
                deleted_something = True
            self.selected_objs.clear()
            self.clear_selection_visuals() # Clear visual feedback for all selections
            self.selected_obj = None # Ensure single selection is also cleared

        elif self.selected_obj:
            self.save_state_for_undo() # Save state before deleting a single object
            tag = None
            # selected_obj might be an ID or a tag, try to get tag
            try:
                tags = self.canvas.gettags(self.selected_obj)
                if tags:
                    tag = tags[0]
            except tk.TclError: # If selected_obj is not a valid canvas item ID
                pass

            if tag:
                obj_ids = self.canvas.find_withtag(tag)
                if obj_ids:
                    self.canvas.delete(obj_ids[0]) # Delete from canvas
                if tag in self.objects:
                    del self.objects[tag] # Delete from internal tracking
                if tag in self.active_pil_images:
                    del self.active_pil_images[tag]
                if tag in self.tk_image_references:
                    del self.tk_image_references[tag]
                deleted_something = True
            elif isinstance(self.selected_obj, int): # If it's a canvas ID directly
                # This case might be less common if we consistently use tags
                self.canvas.delete(self.selected_obj)
                # Need to find the tag associated with this ID to remove from self.objects
                # This part might need refinement if we only store by tag
                # For now, assume selection primarily works with tags
                deleted_something = True


            self.clear_selection_visuals() # Clear visual feedback
            self.selected_obj = None # Clear the selection

        if deleted_something:
            # self.save_state_for_undo() # Already called above
            pass # Future: update UI or other elements if needed

    def update_button_visuals(self):
        # Update shape buttons
        shape_buttons = {
            'rectangle': '-RECTANGLE-',
            'circle': '-CIRCLE-',
            'line': '-LINE-',
            'free': '-FREE-',
            'triangle': '-TRIANGLE-',
            'diamond': '-DIAMOND-',
            'erase': '-ERASE-'
        }
        
        for shape, key in shape_buttons.items():
            if shape == self.current_shape and key in self.window.key_dict:
                self.window[key].update(button_color=('white', 'blue'))
            elif key in self.window.key_dict:
                self.window[key].update(button_color=('black', 'lightgray'))
          # Update color buttons with a border to show current selection
        color_buttons = {
            'black': '-BLACK-',
            'red': '-RED-',
            'green': '-GREEN-'
        }
        
        for color_name, key in color_buttons.items():
            if color_name == self.current_color and key in self.window.key_dict:
                # Active color - full opacity
                self.window[key].update(button_color=('white', color_name))
            elif key in self.window.key_dict:
                # Inactive color - semi-transparent (not really transparent but lighter shade)
                if color_name == 'black':
                    inactive_color = '#808080'  # Gray for black
                elif color_name == 'red':
                    inactive_color = '#FFC0C0'  # Light red
                elif color_name == 'green':
                    inactive_color = '#90EE90'  # Light green (darker shade)
                else:
                    inactive_color = color_name
                self.window[key].update(button_color=('white', inactive_color))
        
        # Update thickness buttons
        thickness_buttons = {
            'thin': '-THIN-',
            'thick': '-THICK-'
        }
        
        for thickness, key in thickness_buttons.items():
            if thickness == self.current_thickness and key in self.window.key_dict:
                self.window[key].update(button_color=('white', 'blue'))
            elif key in self.window.key_dict:
                self.window[key].update(button_color=('black', 'lightgray'))

    def set_shape(self, shape):
        self.current_shape = shape
        self.select_mode = False
        self.selected_objs.clear()
        self.clear_selection_visuals()
        self.selected_obj = None  # Clear single selection
        
        # Set cursor for erase mode
        if shape == "erase":
            # Create an eraser cursor
            self.canvas.config(cursor="dotbox")  # Using a built-in cursor that looks similar to an eraser
        else:
            # Reset to default cursor
            self.canvas.config(cursor="")
            
        # self.active_pil_images.clear() # Potentially clear these if not in select mode
        # self.tk_image_references.clear()
        self.update_button_visuals() # Update button visuals
        
    def set_color(self, color):
        changed = False
        if self.selected_objs:
            for tag in self.selected_objs:
                if tag in self.objects:
                    self.objects[tag]["color"] = color
                    obj_type = self.objects[tag]["type"]
                    # Ensure obj_id is valid before using it
                    obj_ids = self.canvas.find_withtag(tag)
                    if not obj_ids:
                        continue # Skip if object not found on canvas
                    obj_id = obj_ids[0]
                    
                    if obj_type == "text":
                        self.canvas.itemconfig(obj_id, fill=color)
                    elif obj_type in ("line", "free"):
                        self.canvas.itemconfig(obj_id, fill=color)
                    else: # rectangle, circle, triangle, diamond
                        self.canvas.itemconfig(obj_id, outline=color)
                    changed = True
            if changed:
                self.save_state_for_undo()

        # Update current color for new objects
        self.current_color = color
        self.update_button_visuals()
    
    def set_thickness(self, thickness):
        self.current_thickness = thickness
        
        # Apply thickness to selected objects if any
        if self.select_mode and self.selected_objs:
            for tag in self.selected_objs:
                if tag in self.objects:
                    self.objects[tag]["thickness"] = thickness
                    self._apply_thickness_to_object(tag)
        elif self.selected_obj:
            tag = self.canvas.gettags(self.selected_obj)[0]
            if tag in self.objects:
                self.objects[tag]["thickness"] = thickness
                self._apply_thickness_to_object(tag)
                
        self.update_button_visuals()
    
    def _apply_thickness_to_object(self, tag):
        if tag not in self.objects:
            return
            
        obj = self.objects[tag]
        obj_id = self.canvas.find_withtag(tag)[0]
        
        # Determine width based on thickness
        width = 1 if obj.get("thickness", "thin") == "thin" else 3
        
        if obj["type"] in ["line", "free", "triangle", "diamond"]:
            self.canvas.itemconfig(obj_id, width=width)
        elif obj["type"] in ["rectangle", "circle"]:
            self.canvas.itemconfig(obj_id, width=width)
    
    def choose_color(self):
        color = colorchooser.askcolor()[1]  # Returns RGB tuple and hex value
        if color:
            self.set_color(color)

    def start_draw(self, event):
        self.start_x = self.canvas.canvasx(event.x) / self.scale
        self.start_y = self.canvas.canvasy(event.y) / self.scale
        self._draw_started = False
        self._draw_first_event = (self.start_x, self.start_y)
        
        # Handle eraser tool
        if self.current_shape == "erase":
            # Find object under cursor
            x = self.start_x
            y = self.start_y
            obj_tag = self.find_overlapping(x, y)
            if obj_tag:
                # Save state for undo before erasing
                self.save_state_for_undo()
                # Delete the object
                obj_id = self.canvas.find_withtag(obj_tag)[0]
                self.canvas.delete(obj_id)
                if obj_tag in self.objects:
                    del self.objects[obj_tag]
            return
        
        # Left mouse button is only for drawing, not selecting
        if self.select_mode:
            return  
        
        # With left mouse button, always clear any existing selection
        self.selected_obj = None
        self.selected_objs.clear()
        self.clear_selection_visuals()
    
    def draw(self, event):
        x = self.canvas.canvasx(event.x) / self.scale
        y = self.canvas.canvasy(event.y) / self.scale
        if not hasattr(self, '_draw_first_event'):
            return
        dx = abs(x - self._draw_first_event[0])
        dy = abs(y - self._draw_first_event[1])
        if not self._draw_started and (dx > 3 or dy > 3):
            # Start the actual drawing now
            self._draw_started = True
            
            # Get the line width based on thickness
            width = 1 if self.current_thickness == "thin" else 3
            
            if self.current_shape == "line":
                self.line_start = (self._draw_first_event[0], self._draw_first_event[1])
            elif self.current_shape == "free":
                tag = f"obj_{len(self.objects)}"
                self.current_obj = self.canvas.create_line(
                    self._draw_first_event[0], self._draw_first_event[1], x, y,
                    fill=self.current_color, width=width, tags=tag, smooth=True
                )
                self.objects[tag] = {
                    "type": "free",
                    "color": self.current_color,
                    "thickness": self.current_thickness,
                    "coords": [self._draw_first_event[0], self._draw_first_event[1], x, y]
                }
            elif self.current_shape == "rectangle":
                tag = f"obj_{len(self.objects)}"
                self.current_obj = self.canvas.create_rectangle(
                    self._draw_first_event[0], self._draw_first_event[1], x, y,
                    outline=self.current_color, width=width, tags=tag
                )
                self.objects[tag] = {
                    "type": "rectangle",
                    "color": self.current_color,
                    "thickness": self.current_thickness,
                    "coords": [self._draw_first_event[0], self._draw_first_event[1], x, y]
                }
            elif self.current_shape == "circle":
                tag = f"obj_{len(self.objects)}"
                self.current_obj = self.canvas.create_oval(
                    self._draw_first_event[0], self._draw_first_event[1], x, y,
                    outline=self.current_color, width=width, tags=tag
                )
                self.objects[tag] = {
                    "type": "circle",
                    "color": self.current_color,
                    "thickness": self.current_thickness,
                    "coords": [self._draw_first_event[0], self._draw_first_event[1], x, y]
                }
            elif self.current_shape == "triangle":
                tag = f"obj_{len(self.objects)}"
                # Calculate triangle points
                x0, y0 = self._draw_first_event[0], self._draw_first_event[1]
                # Make triangle point upward by default
                points = [
                    x0, y,  # Bottom left
                    (x0 + x) / 2, y0,  # Top middle
                    x, y  # Bottom right
                ]
                self.current_obj = self.canvas.create_polygon(
                    points, outline=self.current_color, fill="", width=width, tags=tag
                )
                self.objects[tag] = {
                    "type": "triangle",
                    "color": self.current_color,
                    "thickness": self.current_thickness,
                    "coords": points
                }
            elif self.current_shape == "diamond":
                tag = f"obj_{len(self.objects)}"
                # Calculate diamond points
                x0, y0 = self._draw_first_event[0], self._draw_first_event[1]
                mid_x, mid_y = (x0 + x) / 2, (y0 + y) / 2
                points = [
                    mid_x, y0,  # Top
                    x, mid_y,  # Right
                    mid_x, y,  # Bottom
                    x0, mid_y  # Left
                ]
                self.current_obj = self.canvas.create_polygon(
                    points, outline=self.current_color, fill="", width=width, tags=tag
                )
                self.objects[tag] = {
                    "type": "diamond",
                    "color": self.current_color,
                    "thickness": self.current_thickness,
                    "coords": points
                }
        if not self._draw_started:
            return
            
        # Update object appearance as the mouse moves
        width = 1 if self.current_thickness == "thin" else 3
        
        if self.current_shape == "line" and self.line_start:
            if hasattr(self, 'preview_line') and self.preview_line:
                self.canvas.delete(self.preview_line)
            self.preview_line = self.canvas.create_line(
                self.line_start[0], self.line_start[1], x, y,
                fill=self.current_color, width=width, tags="preview_line"
            )
        elif self.current_shape == "free" and self.current_obj:
            tag = self.canvas.gettags(self.current_obj)[0]
            coords = self.objects[tag]["coords"]
            coords.extend([x, y])
            self.canvas.coords(self.current_obj, *coords)
        elif self.current_shape == "triangle" and self.current_obj:
            x0, y0 = self._draw_first_event[0], self._draw_first_event[1]
            # Update triangle points
            points = [
                x0, y,  # Bottom left
                (x0 + x) / 2, y0,  # Top middle
                x, y  # Bottom right
            ]
            self.canvas.coords(self.current_obj, *points)
            self.objects[self.canvas.gettags(self.current_obj)[0]]["coords"] = points
        elif self.current_shape == "diamond" and self.current_obj:
            x0, y0 = self._draw_first_event[0], self._draw_first_event[1]
            mid_x, mid_y = (x0 + x) / 2, (y0 + y) / 2
            points = [
                mid_x, y0,  # Top
                x, mid_y,  # Right
                mid_x, y,  # Bottom
                x0, mid_y  # Left
            ]
            self.canvas.coords(self.current_obj, *points)
            self.objects[self.canvas.gettags(self.current_obj)[0]]["coords"] = points
        elif self.current_shape in ["rectangle", "circle"] and self.current_obj:
            self.canvas.coords(
                self.current_obj,
                self._draw_first_event[0], self._draw_first_event[1], x, y
            )
            self.objects[self.canvas.gettags(self.current_obj)[0]]["coords"] = [self._draw_first_event[0], self._draw_first_event[1], x, y]
    
    def end_draw(self, event):
        if hasattr(self, '_draw_started') and not self._draw_started:
            # No actual drawing happened
            return
            
        if self.current_shape == "line" and self.line_start:
            x = self.canvas.canvasx(event.x) / self.scale
            y = self.canvas.canvasy(event.y) / self.scale
            tag = f"obj_{len(self.objects)}"
            width = 1 if self.current_thickness == "thin" else 3
            
            # Remove the preview line
            if hasattr(self, 'preview_line') and self.preview_line:
                self.canvas.delete(self.preview_line)
                self.preview_line = None
            
            self.current_obj = self.canvas.create_line(
                self.line_start[0], self.line_start[1], x, y,
                fill=self.current_color, width=width, tags=tag
            )
            
            self.objects[tag] = {
                "type": "line",
                "color": self.current_color,
                "thickness": self.current_thickness,
                "coords": [self.line_start[0], self.line_start[1], x, y]
            }
            self.line_start = None
            self.save_state_for_undo()
        
        elif self.current_shape == "free" and self.current_obj:
            self.save_state_for_undo()
            self.current_obj = None
            
        elif self.current_obj and self.current_shape in ["rectangle", "circle", "triangle", "diamond"]:
            self.save_state_for_undo()
            self.current_obj = None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.objects = {}
        self.selected_obj = None
        self.middle_clicked_obj_tag = None # Reset on clear
        self.current_obj = None
        self.line_start = None
        
        # Clear background image references
        self.bg_image_pil = None
        self.bg_image_tk = None
        
        # Clear imported picture object references
        self.active_pil_images.clear()
        self.tk_image_references.clear()

        # Reset scale and view to default
        self.scale = 1.0
        self.canvas_x = 0
        self.canvas_y = 0
        
    def find_overlapping(self, x, y):
        # x, y are logical (unscaled) coordinates
        radius = 5 / self.scale  # Radius in logical units for point proximity
        
        # Canvas coordinates for find_overlapping (which expects screen coordinates)
        # However, canvas.find_overlapping is not the primary method here.
        # We iterate self.objects and check logical coordinates.

        text_hits = []
        other_hits = []
        
        # Iterate through objects. Consider visual stacking order if possible (e.g. reverse of creation or use canvas item IDs)
        # For now, iterate and then prioritize text.
        sorted_tags = list(self.objects.keys()) # Potentially sort by creation order or z-index later

        for tag in sorted_tags:
            obj_data = self.objects[tag]
            obj_type = obj_data["type"]
            coords = obj_data["coords"]

            if obj_type == "text":
                # For text, check bounding box. Tkinter's bbox is in screen coords.
                # We need to get the logical bbox or check against logical coords.
                # Text coords are [logical_x, logical_y]. Font size also matters.
                # A simple check: if click is near the text's anchor point.
                # A more robust check would involve self.canvas.bbox(tag) and converting to logical.
                # For now, let's assume a small clickable area around the text anchor.
                # Estimate a bounding box based on font size (this is a rough approximation)
                font_size = obj_data.get("font_size", 12) # Logical font size
                # Approximate width/height based on text length and font_size (very rough)
                # This part is tricky without rendering the text to get its actual logical bbox.
                # Let's use canvas.bbox(tag) and convert back to logical.
                try:
                    # Get screen bbox from canvas, then convert to logical for checking
                    screen_bbox = self.canvas.bbox(tag)
                    if screen_bbox:
                        logical_bbox_x1 = screen_bbox[0] / self.scale # Assuming canvas_x/y are 0 for this conversion
                        logical_bbox_y1 = screen_bbox[1] / self.scale
                        logical_bbox_x2 = screen_bbox[2] / self.scale
                        logical_bbox_y2 = screen_bbox[3] / self.scale
                        if logical_bbox_x1 <= x <= logical_bbox_x2 and \
                           logical_bbox_y1 <= y <= logical_bbox_y2:
                            text_hits.append(tag)
                except tk.TclError: # Item might not be on canvas yet or deleted
                    pass

            elif obj_type == "rectangle" or obj_type == "image": # Image is also rectangular
                x1, y1, x2, y2 = coords # These are logical coordinates
                left, right = min(x1, x2), max(x1, x2)
                top, bottom = min(y1, y2), max(y1, y2)
                if left <= x <= right and top <= y <= bottom:
                    other_hits.append(tag)
            elif obj_type == "circle":
                x1, y1, x2, y2 = coords
                center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
                rx, ry = abs(x2 - x1) / 2, abs(y2 - y1) / 2
                if rx == 0 or ry == 0: continue
                norm_dx, norm_dy = (x - center_x) / rx, (y - center_y) / ry
                if norm_dx * norm_dx + norm_dy * norm_dy <= 1:
                    other_hits.append(tag)
            elif obj_type in ["triangle", "diamond"]:
                # Point-in-polygon test is needed here.
                # For simplicity, if canvas.find_overlapping with a small area around (x,y) hits this object's tag.
                # This requires converting logical x,y to screen x,y for canvas.find_overlapping.
                screen_check_x = x * self.scale
                screen_check_y = y * self.scale
                overlapping_canvas_ids = self.canvas.find_overlapping(
                    screen_check_x - 2, screen_check_y - 2, 
                    screen_check_x + 2, screen_check_y + 2
                )
                obj_canvas_ids = self.canvas.find_withtag(tag)
                if obj_canvas_ids and obj_canvas_ids[0] in overlapping_canvas_ids:
                    other_hits.append(tag)

            elif obj_type in ["line", "free"]:
                # Check proximity to line segments. This is complex.
                # A simpler check: if the object's bounding box (expanded slightly) contains the point.
                # Or, if canvas.find_overlapping hits it.
                screen_check_x = x * self.scale
                screen_check_y = y * self.scale
                overlapping_canvas_ids = self.canvas.find_overlapping(
                    screen_check_x - radius * self.scale, screen_check_y - radius * self.scale, 
                    screen_check_x + radius * self.scale, screen_check_y + radius * self.scale
                )
                obj_canvas_ids = self.canvas.find_withtag(tag)
                if obj_canvas_ids and obj_canvas_ids[0] in overlapping_canvas_ids:
                     # More precise check for lines/free: iterate segments
                    obj_coords = obj_data["coords"]
                    for i in range(0, len(obj_coords) - 2, 2):
                        p1x, p1y = obj_coords[i], obj_coords[i+1]
                        p2x, p2y = obj_coords[i+2], obj_coords[i+3]
                        # Distance from point (x,y) to line segment (p1,p2)
                        # This is a simplified check (distance to infinite line)
                        # A true segment distance is more complex.
                        # For now, if bounding box of segment (with radius) contains point.
                        min_seg_x, max_seg_x = min(p1x, p2x) - radius, max(p1x, p2x) + radius
                        min_seg_y, max_seg_y = min(p1y, p2y) - radius, max(p1y, p2y) + radius
                        if min_seg_x <= x <= max_seg_x and min_seg_y <= y <= max_seg_y:
                            # This is still a bbox check of segment.
                            # A proper line proximity check is needed for accuracy.
                            other_hits.append(tag)
                            break # Found hit for this line/free object


        # Prioritize text hits. If multiple hits, the one "on top" (last in draw order or raised)
        # The current canvas.find_withtag(tag) or canvas.bbox(tag) refers to the single canvas item.
        # If text_hits is not empty, return the "topmost" one.
        # How to determine topmost from tags? If they were raised, canvas handles it.
        # We can query canvas items at point:
        if text_hits:
            # Query canvas items at the logical point (converted to screen)
            screen_x, screen_y = x * self.scale, y * self.scale
            ids_at_point = self.canvas.find_closest(screen_x, screen_y, halo=max(1,int(radius*self.scale/2)))
            if ids_at_point:
                top_id_at_point = ids_at_point[0] # Closest is usually topmost
                tags_of_top_id = self.canvas.gettags(top_id_at_point)
                for t in tags_of_top_id:
                    if t in text_hits:
                        return t # Return the specific text tag that is topmost
            if text_hits: return text_hits[-1] # Fallback: last text object checked that matched

        if other_hits:
            screen_x, screen_y = x * self.scale, y * self.scale
            ids_at_point = self.canvas.find_closest(screen_x, screen_y, halo=max(1,int(radius*self.scale/2)))
            if ids_at_point:
                top_id_at_point = ids_at_point[0]
                tags_of_top_id = self.canvas.gettags(top_id_at_point)
                for t in tags_of_top_id:
                    if t in other_hits:
                        return t # Return the specific non-text tag that is topmost
            if other_hits: return other_hits[-1] # Fallback

        return None
    
    def quadratic_bezier(self, x1, y1, cx, cy, x2, y2, steps=20):
        points = []
        for i in range(steps + 1):
            t = i / steps
            mt = 1 - t
            x = mt * mt * x1 + 2 * mt * t * cx + t * t * x2
            y = mt * mt * y1 + 2 * mt * t * cy + t * t * y2
            points.extend([x, y])
        return points
    
    def add_text(self, event):
        x = self.canvas.canvasx(event.x) / self.scale
        y = self.canvas.canvasy(event.y) / self.scale
        text = simpledialog.askstring("Input Text", "Enter text below:")
        if text:
            tag = f"obj_{len(self.objects)}"
            text_id = self.canvas.create_text(
                x, y, text=text, fill=self.current_color, font=("Arial", 12), tags=tag
            )
            self.objects[tag] = {
                "type": "text",
                "color": self.current_color,
                "coords": [x, y],
                "font_size": 12, # Store logical font size
                "text": text,
                "thickness": self.current_thickness # Though not directly used for text fill
            }
            self.canvas.tag_raise(tag) # Ensure text is on top
            self.save_state_for_undo()
        self.canvas.focus_set()

    def edit_text_object_content(self, tag_to_edit):
        if tag_to_edit not in self.objects or self.objects[tag_to_edit]["type"] != "text":
            return

        obj_data = self.objects[tag_to_edit]
        current_text = obj_data.get("text", "")
        
        # Use simpledialog to get new text
        new_text = simpledialog.askstring("Edit Text", 
                                          "Enter new text (multiple lines allowed):",
                                          initialvalue=current_text,
                                          parent=self.window.TKroot)
        
        if new_text is not None and new_text != current_text:
            # Delete the old canvas text item
            canvas_ids = self.canvas.find_withtag(tag_to_edit)
            if canvas_ids:
                self.canvas.delete(canvas_ids[0])
            
            # Update the object in self.objects
            obj_data["text"] = new_text
            
            # Recreate the text object on the canvas (will be done by redraw_all_objects)
            # No need to create it here directly if redraw_all_objects handles it
            
            self.save_state_for_undo()
            self.redraw_all_objects() # This will redraw the updated text
            self.update_selection_visuals() # Re-apply selection visuals

    def handle_double_click(self, event):
        x = self.canvas.canvasx(event.x) / self.scale
        y = self.canvas.canvasy(event.y) / self.scale
        
        clicked_obj_tag = self.find_overlapping(x, y)
        
        if clicked_obj_tag and self.objects[clicked_obj_tag]["type"] == "text":
            self.edit_text_object_content(clicked_obj_tag)
        else:
            # If not clicking on text, or clicking on empty space, add new text
            self.add_text(event)

    def handle_middle_mouse_press(self, event):
        self.middle_clicked_obj_tag = None  # Reset before attempting to set

        # Use canvas.find_closest to find items near the click. event.x, event.y are screen coordinates.
        items = self.canvas.find_closest(event.x, event.y, halo=3) # halo is a small tolerance in pixels

        clicked_tag_candidate = None
        clicked_item_id_candidate = None

        if items:
            for item_id in items: # find_closest might return multiple if equidistant or overlapping
                tags = self.canvas.gettags(item_id)
                if tags:
                    # Our convention is that the first tag (e.g., "obj_123") is the main identifier
                    # that maps to our self.objects dictionary.
                    potential_tag = tags[0]
                    if potential_tag in self.objects:
                        # Check if the click is actually within the bounding box of this specific item
                        # self.canvas.bbox(item_id) returns screen coordinates (x1, y1, x2, y2)
                        x1, y1, x2, y2 = self.canvas.bbox(item_id)
                        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                            clicked_tag_candidate = potential_tag
                            clicked_item_id_candidate = item_id
                            break # Found a valid object, prioritize this one
        
        if clicked_tag_candidate:
            obj_type = self.objects[clicked_tag_candidate]["type"]
            if obj_type == "text":
                self.middle_clicked_obj_tag = clicked_tag_candidate
                # self.selected_obj = clicked_item_id_candidate # Optional: if text actions also use selected_obj
            elif obj_type == "image":
                self.middle_clicked_obj_tag = clicked_tag_candidate
                # resize_selected_image uses self.selected_obj (canvas ID)
                self.selected_obj = clicked_item_id_candidate 
            # else: it's another object type, no specific middle-click context menu for it

    def handle_middle_mouse_release(self, event):
        if self.middle_clicked_obj_tag and self.middle_clicked_obj_tag in self.objects:
            obj_type = self.objects[self.middle_clicked_obj_tag]["type"]
            
            # Optional: Check if mouse is still over the same object to prevent menu if mouse dragged off.
            # For simplicity, we'll show menu if a relevant object was clicked on ButtonPress.

            if obj_type == "text":
                self.text_context_menu.post(event.x_root, event.y_root)
            elif obj_type == "image":
                # Ensure self.selected_obj is correctly set to the image's canvas ID
                # This should have been done in handle_middle_mouse_press
                if self.selected_obj == self.canvas.find_withtag(self.middle_clicked_obj_tag)[0]:
                     self.image_context_menu.post(event.x_root, event.y_root)
                else:
                    # Fallback or error: selected_obj might not match middle_clicked_obj_tag's image
                    # This case should ideally not happen if press handler is correct.
                    # For robustness, could try to re-select here, but better to ensure press handler is solid.
                    pass # Or log an issue
            
        self.middle_clicked_obj_tag = None # Always reset after use or if no menu shown

    def change_text_size_preset(self, size):
        if not self.selected_obj and not self.selected_objs:
            return
        
        size_map = {"small": 8, "medium": 12, "large": 18}
        new_size = size_map.get(size, 12)
            
        # Apply to all selected objects
        if self.selected_objs:
            for tag in self.selected_objs:
                if tag in self.objects and self.objects[tag]["type"] == "text":
                    obj = self.objects[tag]
                    obj["font_size"] = new_size
                    obj_id = self.canvas.find_withtag(tag)[0]
                    self.canvas.itemconfig(obj_id, font=("Arial", new_size))
            self.save_state_for_undo()
        # Apply to single selected object
        elif self.selected_obj:
            tag = self.canvas.gettags(self.selected_obj)[0]
            if tag in self.objects and self.objects[tag]["type"] == "text":
                obj = self.objects[tag]
                obj["font_size"] = new_size
                self.canvas.itemconfig(self.selected_obj, font=("Arial", new_size))
                self.save_state_for_undo()

    def save_state_for_undo(self):
        """Saves the current state of all objects for undo."""
        # Deep copy current objects state
        state_copy = copy.deepcopy(self.objects)
        self.undo_stack.append(state_copy)
        self.redo_stack.clear()  # Clear redo stack when a new action is performed
    
    def undo_last_action(self):
        if not self.undo_stack:
            return
        
        # Save current state to redo stack
        current_state = copy.deepcopy(self.objects)
        self.redo_stack.append(current_state)
        
        # Restore previous state
        prev_state = self.undo_stack.pop()
        self.canvas.delete("all")  # Clear canvas
        self.objects = prev_state
        self.redraw_all_objects()
        
        # Clear selections
        self.selected_obj = None
        self.selected_objs.clear()
        
    def redo_last_action(self):
        if not self.redo_stack:
            return
        
        # Save current state to undo stack
        current_state = copy.deepcopy(self.objects)
        self.undo_stack.append(current_state)
        
        # Restore next state
        next_state = self.redo_stack.pop()
        self.canvas.delete("all")  # Clear canvas
        self.objects = next_state
        self.redraw_all_objects()
        
        # Clear selections
        self.selected_obj = None
        self.selected_objs.clear()
    
    def redraw_all_objects(self):
        self.canvas.delete("all")  # Clear canvas first
        
        # Redraw background if it exists
        if self.bg_image_pil:
            self.draw_background_image() # This handles its own scaling and positioning

        text_tags_to_raise = []
        # Clear runtime references, they will be repopulated
        self.tk_image_references.clear() 

        # Sort objects? For now, draw in order, then raise text.
        # If selection highlighting is done by redrawing on top, that needs to be handled last.
        
        for tag, obj_data in self.objects.items():
            obj_type = obj_data["type"]
            coords = obj_data["coords"]  # Logical, unscaled
            color = obj_data.get("color", self.current_color)
            thickness_str = obj_data.get("thickness", self.current_thickness)
            
            # Scale width, ensuring it's at least 1px on screen after scaling
            # For logical width, it's 1 or 3. For screen width, it's scale * logical_width.
            screen_line_width = max(1, int((1 if thickness_str == "thin" else 3) * self.scale))

            # Helper to scale logical coordinates to screen coordinates for drawing
            # This assumes self.canvas_x and self.canvas_y are for scan_dragto and not a world view offset.
            # If canvasx/y in events already account for pan, then drawing at scaled logical coords is fine.
            def T(p_coords_logical):
                return [c * self.scale for c in p_coords_logical]

            if obj_type == "rectangle":
                s_coords = T(coords)
                self.canvas.create_rectangle(*s_coords, outline=color, width=screen_line_width, tags=tag)
            elif obj_type == "circle":
                s_coords = T(coords)
                self.canvas.create_oval(*s_coords, outline=color, width=screen_line_width, tags=tag)
            elif obj_type == "line":
                s_coords = T(coords)
                self.canvas.create_line(*s_coords, fill=color, width=screen_line_width, tags=tag)
            elif obj_type == "free":  # Series of points
                s_coords = T(coords)
                self.canvas.create_line(*s_coords, fill=color, width=screen_line_width, tags=tag, smooth=True)
            elif obj_type == "triangle" or obj_type == "diamond":
                s_coords = T(coords)
                self.canvas.create_polygon(*s_coords, outline=color, fill="", width=screen_line_width, tags=tag) # No fill for these polygons
            elif obj_type == "text":
                s_coords_xy = T([coords[0], coords[1]])  # Scaled x, y for anchor
                font_size_logical = obj_data.get("font_size", 12)
                # Scale font size for display, ensuring minimum practical size
                scaled_font_size = max(6, int(font_size_logical * self.scale)) 
                text_content = obj_data.get("text", "")
                self.canvas.create_text(s_coords_xy[0], s_coords_xy[1], text=text_content, fill=color,
                                        font=("Arial", scaled_font_size), tags=tag)
                text_tags_to_raise.append(tag)
            elif obj_type == "image":
                # Coords are [x0_logical, y0_logical, x1_logical, y1_logical]
                pil_img = self.active_pil_images.get(tag)
                if not pil_img:
                    try:
                        pil_img = Image.open(obj_data["filepath"])
                        self.active_pil_images[tag] = pil_img  # Cache it
                    except Exception as e:
                        print(f"Error loading image {obj_data['filepath']} for redraw: {e}")
                        continue
                
                # Scaled top-left corner for drawing
                draw_x_screen = coords[0] * self.scale
                draw_y_screen = coords[1] * self.scale
                
                # Scaled width and height for the image on canvas
                img_display_width_screen = int((coords[2] - coords[0]) * self.scale)
                img_display_height_screen = int((coords[3] - coords[1]) * self.scale)

                if img_display_width_screen <= 0 or img_display_height_screen <= 0:
                    continue # Skip drawing if dimensions are invalid

                try:
                    # Resize the original PIL image to the target display size
                    resized_pil_img = pil_img.resize((img_display_width_screen, img_display_height_screen), Image.LANCZOS)
                    tk_image = ImageTk.PhotoImage(resized_pil_img)
                    self.tk_image_references[tag] = tk_image  # IMPORTANT: keep reference for this redraw cycle

                    self.canvas.create_image(draw_x_screen, draw_y_screen, image=tk_image, anchor="nw", tags=tag)
                except Exception as e:
                    print(f"Error resizing/displaying image {tag}: {e}")


        # Raise all text objects to ensure they are on top
        for tag in text_tags_to_raise:
            try:
                self.canvas.tag_raise(tag)
            except tk.TclError: # Object might have been deleted during other operations
                pass
        
        # Re-apply selection visuals if needed (complex, depends on how selection is stored and visualized)
        # For now, this basic redraw is the focus.
        # If selection involves drawing extra items (like bounding boxes), that should happen here too.
        self.update_selection_visuals() # A new or existing method to show selection

    def update_selection_visuals(self):
        self.clear_selection_visuals()
        # The blue dashed highlight is the visual indicator for selected objects (multi-selection or single selection)
        for tag in self.selected_objs:
            if tag in self.objects:
                obj = self.objects[tag]
                # Ensure canvas item exists before trying to get its ID, though find_withtag should handle non-existent tags gracefully.
                obj_ids = self.canvas.find_withtag(tag)
                if not obj_ids: continue # Skip if object not on canvas
                obj_id = obj_ids[0] # Use obj_id if needed, though not directly used in highlight creation below

                coords = obj["coords"]
                if obj["type"] == "rectangle" or obj["type"] == "image": # Added "image"
                    hl = self.canvas.create_rectangle(*coords, outline="#00f", width=2, dash=(4,2), tags="_selhl")
                elif obj["type"] == "circle":
                    hl = self.canvas.create_oval(*coords, outline="#00f", width=2, dash=(4,2), tags="_selhl")
                elif obj["type"] in ["line", "free"]:
                    hl = self.canvas.create_line(*coords, fill="#00f", width=2, dash=(4,2), tags="_selhl")
                elif obj["type"] == "text":
                    x, y = coords
                    hl = self.canvas.create_rectangle(x-40, y-20, x+40, y+20, outline="#00f", width=2, dash=(4,2), tags="_selhl")
                elif obj["type"] in ["triangle", "diamond"]:
                    hl = self.canvas.create_polygon(*coords, outline="#00f", fill="", width=2, dash=(4,2), tags="_selhl")
    
    def clear_selection_visuals(self):
        self.canvas.delete("_selhl")
        
    def start_right_drag_select(self, event):
        # Right mouse button is used for selecting and moving objects
        x = self.canvas.canvasx(event.x) / self.scale
        y = self.canvas.canvasy(event.y) / self.scale
        
        # Check if we clicked on an object
        clicked_obj = self.find_overlapping(x, y)
        
        if clicked_obj:
            # Select the object for moving
            self.selected_obj = self.canvas.find_withtag(clicked_obj)[0]
            self.selected_objs = set([clicked_obj])
            self.update_selection_visuals()
            self.move_start_x = x
            self.move_start_y = y
            self._moving_object = True
            self.is_panning = False
        else:
            # Start panning the canvas with right mouse button on empty area
            self._moving_object = False
            self.is_panning = True
            self.canvas.scan_mark(event.x, event.y)
            self.pan_start_x = event.x
            self.pan_start_y = event.y
            
            # If in selection mode, start a selection rectangle instead of panning
            if self.select_mode:
                self.is_panning = False
                self.rdrag_start_x = x
                self.rdrag_start_y = y
                self.rdrag_rect = self.canvas.create_rectangle(
                    x, y, x, y,
                    outline="#00f", dash=(4,2), width=2, tags="_rdragrect"
                )

    def right_drag_select(self, event):
        if hasattr(self, '_moving_object') and self._moving_object:
            # Move the selected object
            if not self.selected_obj:
                return
                
            x = self.canvas.canvasx(event.x) / self.scale
            y = self.canvas.canvasy(event.y) / self.scale
            dx = x - self.move_start_x
            dy = y - self.move_start_y
            tag = self.canvas.gettags(self.selected_obj)[0]
            
            if tag in self.objects:
                obj = self.objects[tag]
                if obj["type"] in ["rectangle", "circle"]:
                    x1, y1, x2, y2 = obj["coords"]
                    self.canvas.coords(
                        self.selected_obj,
                        x1 + dx, y1 + dy, x2 + dx, y2 + dy
                    )
                    obj["coords"] = [x1 + dx, y1 + dy, x2 + dx, y2 + dy]
                elif obj["type"] in ["line", "free"]:
                    coords = obj["coords"]
                    new_coords = [c + dx if i % 2 == 0 else c + dy for i, c in enumerate(coords)]
                    self.canvas.coords(self.selected_obj, *new_coords)
                    obj["coords"] = new_coords
                elif obj["type"] == "text":
                    # Fix for text objects
                    x_old, y_old = obj["coords"]
                    self.canvas.move(self.selected_obj, dx * self.scale, dy * self.scale)
                    obj["coords"] = [x_old + dx, y_old + dy]
                elif obj["type"] == "image": # Added image handling
                    x0_old, y0_old, x1_old, y1_old = obj["coords"]
                    obj["coords"] = [x0_old + dx, y0_old + dy, x1_old + dx, y1_old + dy]
                    self.canvas.move(self.selected_obj, dx * self.scale, dy * self.scale)
                elif obj["type"] in ["triangle", "diamond"]:
                    coords = obj["coords"]
                    new_coords = [c + dx if i % 2 == 0 else c + dy for i, c in enumerate(coords)]
                    self.canvas.coords(self.selected_obj, *new_coords)
                    obj["coords"] = new_coords
                    
                # Update selection visuals
                self.update_selection_visuals()
                
            self.move_start_x = x
            self.move_start_y = y
            return
            
        # Handle canvas panning - smooth canvas scrolling
        if hasattr(self, 'is_panning') and self.is_panning:
            self.canvas.scan_dragto(event.x, event.y, 1)
            return
            
        # Selection rectangle feedback
        if self.select_mode and hasattr(self, 'rdrag_rect'):
            x1 = self.rdrag_start_x
            y1 = self.rdrag_start_y
            x2 = self.canvas.canvasx(event.x) / self.scale
            y2 = self.canvas.canvasy(event.y) / self.scale
            self.canvas.coords(self.rdrag_rect, x1, y1, x2, y2)
    
    def end_right_drag_select(self, event):
        # If we were moving an object
        if hasattr(self, '_moving_object') and self._moving_object:
            # Save the state after moving
            self.save_state_for_undo()
            # Context menu logic is now handled by middle mouse release
            self._moving_object = False
            return
        
        # End panning
        if hasattr(self, 'is_panning') and self.is_panning:
            self.is_panning = False
            return
        
        # If we were doing a selection rectangle
        if self.select_mode and hasattr(self, 'rdrag_rect'):
            x1 = self.rdrag_start_x
            y1 = self.rdrag_start_y
            x2 = self.canvas.canvasx(event.x) / self.scale
            y2 = self.canvas.canvasy(event.y) / self.scale
            xmin, xmax = min(x1, x2), max(x1, x2)
            ymin, ymax = min(y1, y2), max(y1, y2)
            
            # Clean up rectangle
            self.canvas.delete(self.rdrag_rect)
            del self.rdrag_rect
            del self.rdrag_start_x
            del self.rdrag_start_y
            
            # Select all objects whose bounding box intersects the rectangle
            self.selected_objs.clear()
            
            for tag, obj in self.objects.items():
                coords = obj["coords"]
                if obj["type"] in ("rectangle", "circle", "line", "free", "triangle", "diamond"):
                    # Get bounding box
                    if obj["type"] in ("rectangle", "circle"):
                        x0, y0, x1_, y1_ = coords
                    elif obj["type"] in ("line", "free"):
                        xs = coords[::2]  # All x coordinates
                        ys = coords[1::2]  # All y coordinates
                        if not xs or not ys:  # Skip if empty
                            continue
                        x0, x1_ = min(xs), max(xs)
                        y0, y1_ = min(ys), max(ys)
                    elif obj["type"] in ("triangle", "diamond"):
                        xs = coords[::2]  # All x coordinates
                        ys = coords[1::2]  # All y coordinates
                        if not xs or not ys:  # Skip if empty
                            continue
                        x0, x1_ = min(xs), max(xs)
                        y0, y1_ = min(ys), max(ys)
                    
                    # Check intersection with selection rectangle
                    if not (x1_ < xmin or x0 > xmax or y1_ < ymin or y0 > ymax):
                        self.selected_objs.add(tag)
                        
                elif obj["type"] == "text":
                    x, y = coords
                    if xmin <= x <= xmax and ymin <= y <= ymax:
                        self.selected_objs.add(tag)
            
            # Update selection visuals
            self.update_selection_visuals()

    def save_canvas(self):
        """Save the canvas as PNG image, capturing only the area with objects."""
        if not self.objects:
            sg.popup("Nothing to save", "Canvas is empty")
            return

        try:
            # Calculate the bounding box of all objects
            min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')
            
            for obj in self.objects.values():
                coords = obj["coords"]
                
                if obj["type"] in ["rectangle", "circle"]:
                    x1, y1, x2, y2 = coords
                    min_x = min(min_x, x1, x2)
                    min_y = min(min_y, y1, y2)
                    max_x = max(max_x, x1, x2)
                    max_y = max(max_y, y1, y2)
                elif obj["type"] in ["line", "free"]:
                    x_coords = coords[0::2]  # All x coordinates
                    y_coords = coords[1::2]  # All y coordinates
                    if x_coords and y_coords:
                        min_x = min(min_x, min(x_coords))
                        min_y = min(min_y, min(y_coords))
                        max_x = max(max_x, max(x_coords))
                        max_y = max(max_y, max(y_coords))
                elif obj["type"] == "text":
                    x, y = coords
                    # Estimate text size
                    text_size = obj.get("font_size", 12)
                    text_len = len(obj.get("text", ""))
                    min_x = min(min_x, x - text_len * text_size / 2)
                    min_y = min(min_y, y - text_size)
                    max_x = max(max_x, x + text_len * text_size / 2)
                    max_y = max(max_y, y + text_size)
                elif obj["type"] in ["triangle", "diamond"]:
                    x_coords = coords[0::2]
                    y_coords = coords[1::2]
                    min_x = min(min_x, min(x_coords))
                    min_y = min(min_y, min(y_coords))
                    max_x = max(max_x, max(x_coords))
                    max_y = max(max_y, max(y_coords))
            
            # Add some padding
            padding = 10
            min_x = max(0, min_x - padding)
            min_y = max(0, min_y - padding)
            max_x = max_x + padding
            max_y = max_y + padding

            width = int((max_x - min_x) * self.scale) + 50
            height = int((max_y - min_y) * self.scale) + 50
            # Ensure dimensions are positive
            
            if width <= 0 or height <= 0:
                sg.popup("Invalid dimensions", "Cannot save with these dimensions")
                return
            
            # Ask user for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialdir=os.path.expanduser("~"),
                title="Save Canvas as PNG"
            )
            
            if not file_path:
                return  # User cancelled
            
            # Update the canvas to ensure everything is drawn
            self.window.refresh()
            
            # Capture the canvas image
            # Convert canvas coordinate system to screen coordinates
            x = self.canvas.winfo_rootx() + int(min_x * self.scale)
            y = self.canvas.winfo_rooty() + int(min_y * self.scale)
            
            # Grab the image of the canvas
            # Note: ImageGrab coordinates are in screen coordinates
            img = ImageGrab.grab(bbox=(x, y, x+width, y+height))
            
            # Save the image
            img.save(file_path)
            
            # Copy path to clipboard
            pyperclip.copy(file_path)
            
            sg.popup(f"Image saved to {file_path}", "Path copied to clipboard!")
            
        except Exception as e:
            sg.popup_error(f"Error saving image: {e}")

    def on_canvas_resize(self, event):
        # This event triggers frequently during resize.
        # Consider debouncing if performance becomes an issue.
        if self.bg_image_pil:
            self.draw_background_image()
        
        # Full redraw might be needed if scaling affects all objects significantly
        self.redraw_all_objects()


    def draw_background_image(self):
        if not self.bg_image_pil:
            return

        canvas_width = self.canvas_widget.winfo_width()
        canvas_height = self.canvas_widget.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1: # Canvas not yet realized or too small
            return

        # Clear previous background image(s)
        self.canvas.delete("background_image_tag")

        img_width, img_height = self.bg_image_pil.size
        if img_width == 0 or img_height == 0: return

        img_aspect = img_width / img_height
        canvas_aspect = canvas_width / canvas_height

        if img_aspect > canvas_aspect:
            # Image is wider or less tall than canvas, fit to width
            new_width = canvas_width
            new_height = int(new_width / img_aspect)
        else:
            # Image is taller or less wide than canvas, fit to height
            new_height = canvas_height
            new_width = int(new_height * img_aspect)
        
        if new_width <= 0 or new_height <= 0: return

        try:
            resized_img_pil = self.bg_image_pil.resize((new_width, new_height), Image.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(resized_img_pil) # Keep reference

            # Draw new background image at the center, and at the bottom of the stack
            self.canvas.create_image(0, 0, image=self.bg_image_tk, tags="background_image_tag", anchor="nw") # Draw at 0,0
            # Or centered: self.canvas.create_image(canvas_width / 2, canvas_height / 2, image=self.bg_image_tk, tags="background_image_tag", anchor="center")
            self.canvas.tag_lower("background_image_tag")
        except Exception as e:
            print(f"Error drawing background image: {e}")


    def import_background_image(self):
        try:
            filepath = filedialog.askopenfilename(
                title="Select Background Image",
                filetypes=(("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*"))
            )
            if not filepath:
                return

            self.bg_image_pil = Image.open(filepath)
            self.draw_background_image() # Draw it immediately
            # No undo/redo for background image for now, it's not part of self.objects
        except Exception as e:
            sg.popup_error(f"Error loading background image: {e}")
            self.bg_image_pil = None # Reset on error

    def import_picture_as_object(self):
        try:
            filepath = filedialog.askopenfilename(
                title="Select Picture to Import",
                filetypes=(("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*"))
            )
            if not filepath:
                return

            pil_image = Image.open(filepath)
            img_width_orig, img_height_orig = pil_image.size

            # For now, place it at a default logical position, e.g., (50, 50) unscaled
            # Or let user click to place? For now, fixed position.
            # Scale if too large? For now, original size in logical units.
            # Let's make initial display size somewhat manageable, e.g., max 200 logical pixels
            max_dim_logical = 200.0
            scale_factor = 1.0
            if img_width_orig > max_dim_logical or img_height_orig > max_dim_logical:
                if img_width_orig > img_height_orig:
                    scale_factor = max_dim_logical / img_width_orig
                else:
                    scale_factor = max_dim_logical / img_height_orig
            
            img_display_width_logical = img_width_orig * scale_factor
            img_display_height_logical = img_height_orig * scale_factor

            # Position (logical coordinates)
            # TODO: Get these from a click or center of view
            x0_logical, y0_logical = 50 / self.scale, 50 / self.scale # Example: place near screen 50,50
            x1_logical = x0_logical + img_display_width_logical
            y1_logical = y0_logical + img_display_height_logical
            
            tag = f"obj_{len(self.objects)}"
            
            self.objects[tag] = {
                "type": "image",
                "coords": [x0_logical, y0_logical, x1_logical, y1_logical], # Store as logical bounding box
                "filepath": filepath,
                "original_width": img_width_orig, # Store original dimensions for aspect ratio
                "original_height": img_height_orig,
                "color": None, # Not applicable
                "thickness": None # Not applicable
            }
            
            # Store the PIL image in active cache; it will be used by redraw_all_objects
            self.active_pil_images[tag] = pil_image 
            
            self.save_state_for_undo()
            self.redraw_all_objects() # Redraw to display the new image
            self.canvas.tag_raise(tag) # Bring to front initially

        except Exception as e:
            sg.popup_error(f"Error importing picture: {e}")

    def resize_selected_image(self, factor):
        if not self.selected_obj:
            return

        tags = self.canvas.gettags(self.selected_obj)
        if not tags:
            return
        tag = tags[0]

        if tag in self.objects and self.objects[tag]["type"] == "image":
            obj = self.objects[tag]
            x0, y0, x1, y1 = obj["coords"]
            
            current_w_logical = x1 - x0
            current_h_logical = y1 - y0
            
            new_w_logical = current_w_logical * factor
            new_h_logical = current_h_logical * factor
            
            # Update coords, keeping top-left fixed
            obj["coords"] = [x0, y0, x0 + new_w_logical, y0 + new_h_logical]
            
            self.save_state_for_undo()
            self.redraw_all_objects()
            self.update_selection_visuals() # Re-apply selection visuals as redraw clears them

    def run(self):
        # Main event loop
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            elif event == '-RECTANGLE-':
                self.set_shape("rectangle")
            elif event == '-CIRCLE-':
                self.set_shape("circle")
            elif event == '-LINE-':
                self.set_shape("line")
            elif event == '-FREE-':
                self.set_shape("free")
            elif event == '-TRIANGLE-':
                self.set_shape("triangle")
            elif event == '-DIAMOND-':
                self.set_shape("diamond")
            elif event == '-BLACK-':
                self.set_color("black")
            elif event == '-RED-':
                self.set_color("red")
            elif event == '-GREEN-':
                self.set_color("green")
            elif event == '-CUSTOM-COLOR-':
                self.choose_color()
            elif event == '-THIN-':
                self.set_thickness("thin")
            elif event == '-THICK-':
                self.set_thickness("thick")
            elif event == '-CLEAR-' or event == 'Clear All':
                self.clear_canvas()            
            elif event == '-UNDO-' or event == 'Undo':
                self.undo_last_action()
            elif event == '-REDO-' or event == 'Redo':
                self.redo_last_action()
            elif event == '-SAVE-' or event == 'Save':
                self.save_canvas()
            elif event == 'About':
                sg.popup('Simple Drawing App', 'Created with FreeSimpleGUI and Tkinter')
            elif event == 'New':
                self.clear_canvas()
            elif event == 'Open':
                # This would be implemented with file loading functionality
                sg.popup('Open functionality not implemented yet')
            # New import buttons
            elif event == '-IMPORT-BACKGROUND-': self.import_background_image()
            elif event == '-IMPORT-PICTURE-': self.import_picture_as_object()
        
        self.window.close()

def main():
    app = DrawingApp()
    app.run()
