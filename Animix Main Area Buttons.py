bl_info = {
    "name": "AniMix Main Window Topbar Area Buttons",
    "author": "Adam Earle",
    "version": (1, 0),
    "blender": (2, 91, 0),
    "location": "Top bar > Window",
    "description": "Adds Button to the Topbar of the main window",
    "category": "UI",
}

# Import required libraries
import bpy
import os

# Define a custom Operator class
class OpenAreaWindowOperator(bpy.types.Operator):
    # Define blender's ID name and label for the Operator
    bl_idname = "object.open_area_window"
    bl_label = ""  # Set to an empty string so the operator shows only an icon
    
    # Define custom properties for the Operator
    area_type: bpy.props.StringProperty()
    ui_mode: bpy.props.StringProperty(default='')

    # Method to set window size, works only on Windows
    def set_window_size(self):
        if os.name == 'nt':
            try:
                import ctypes
                # Get handle of the current window
                hWnd = ctypes.windll.user32.GetForegroundWindow()
                user32 = ctypes.windll.user32
                
                # Get the screen size
                screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
                # Define the new window size
                windowSize = (1000, 475)
                # Calculate the position to center the window
                x = (screenSize[0] - windowSize[0]) // 2
                y = (screenSize[1] - windowSize[1]) // 2
                # Set window size and position
                ctypes.windll.user32.SetWindowPos(hWnd, 0, x, y, windowSize[0], windowSize[1], 0)
            except Exception as e:
                print(f'Error setting window size: {e}')
        else:
            print('Window resizing is currently supported only on Windows.')
    
    # Execute method is called when the operator is run
    def execute(self, context):
        bpy.ops.wm.window_new() # Open new window
        bpy.context.area.ui_type = self.area_type # Set area type
        self.set_window_size() # Set window size
        # Set UI mode if specified
        if self.ui_mode:
            bpy.context.space_data.ui_mode = self.ui_mode
        return {'FINISHED'}

# Define a custom Menu class
class AreaVisibilityMenu(bpy.types.Menu):
    # Define blender's ID name and label for the Menu
    bl_label = "Area Types Visibility"
    bl_idname = "AREA_MT_visibility_menu"
    
    # Draw method defines how the Menu is displayed
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        # Add toggle button to layout
        layout.operator("wm.toggle_all_buttons", text="All Areas On Off")

        # Loop through button_groups and add them to layout
        for idx, button_group in enumerate(button_groups):
            for button_idx, button in enumerate(button_group):
                if button is not None:
                    area, icon, *ui_mode, custom_label = button
                    prop_id = f"show_button_{idx}_{button_idx}"
                    layout.prop(wm, prop_id, text=custom_label, icon=icon)
            
            # Add separator after each group
            layout.separator()

# Define a custom Operator to toggle visibility of all buttons
class WM_OT_ToggleAllButtons(bpy.types.Operator):
    bl_idname = "wm.toggle_all_buttons"
    bl_label = "Toggle All Area Buttons"

    # Execute method toggles visibility state for all buttons
    def execute(self, context):
        wm = context.window_manager
        new_state = not getattr(wm, "show_button_0_0", True)
        for idx, button_group in enumerate(button_groups):
            for button_idx, _ in enumerate(button_group):
                prop_id = f"show_button_{idx}_{button_idx}"
                setattr(wm, prop_id, new_state)
        return {'FINISHED'}


# Updated button_groups with custom text labels
button_groups = [
    #(Area,Icon,Module,LabEL)
    [('VIEW_3D', 'VIEW3D', None, '3D View')],
    [('OUTLINER', 'OUTLINER', None, 'Outliner'), 
     ('PROPERTIES', 'PROPERTIES', None, 'Properties'),
     None],
    [('ASSETS', 'ASSET_MANAGER', None, 'Asset Manager'), 
     ('FILES', 'FILE_FOLDER', None, 'File Browser'), 
    None],
    [('IMAGE_EDITOR', 'IMAGE','VIEW', 'Image Editor View'),
     ('IMAGE_EDITOR', 'TPAINT_HLT','PAINT', 'Image Editor Mask'), 
     ('IMAGE_EDITOR', 'MOD_MASK','MASK', 'Image Editor Paint'),
     None],
    [('TextureNodeTree', 'NODE_TEXTURE', 'WORLD', 'Texture Editor World'),
     ('TextureNodeTree', 'BRUSH_DATA', 'BRUSH', 'Texture Editor Brush'),
     ('TextureNodeTree', 'LINE_DATA', 'LINESTYLE', 'Texture Editor Line Style'),
     None],
    [('UV', 'UV', None, 'UV Editor'), 
     None],
    [('CompositorNodeTree','NODE_COMPOSITING', None,'Compositor'),
    None], 
    [('GeometryNodeTree', 'GEOMETRY_NODES', None, 'Geometry Node Editor'),
     ('SPREADSHEET', 'SPREADSHEET', None, 'Spread Sheet'), 
    None],  
    [('ShaderNodeTree', 'NODE_MATERIAL', 'OBJECT', 'Shader Editor Object'),
     ('ShaderNodeTree', 'WORLD', 'WORLD', 'Shader Editor World'),
     ('ShaderNodeTree', 'LINE_DATA', 'LINESTYLE', 'Shader Editor Line Style'), 
    None],
    [('TIMELINE', 'TIME', None, 'Timeline'), 
     ('DOPESHEET', 'ACTION', 'DOPESHEET', 'Dope Sheet'), 
     ('FCURVES', 'GRAPH', None, 'Graph Editor'), 
     ('NLA_EDITOR', 'NLA', None, 'Nonlinear Animation'),
     ('DOPESHEET', 'OBJECT_DATAMODE', 'ACTION', 'Action Editor'),
     None],
    [('DOPESHEET', 'GREASEPENCIL', 'GPENCIL', 'Grease Pencil'),
     ('DOPESHEET', 'SHAPEKEY_DATA', 'SHAPEKEY', 'Shape Key Editor'),
     ('DOPESHEET', 'MOD_MASK', 'MASK', 'Mask'),
     ('DOPESHEET', 'FILE', 'CACHEFILE', 'Cache File'),
     ('SEQUENCE_EDITOR', 'SEQUENCE', 'SEQUENCER', 'Video Sequencer'),
     ('CLIP_EDITOR', 'TRACKER', None, 'Tracker'), 
     None],
    [('TEXT_EDITOR', 'TEXT', None, 'Text Editor'),
     ('CONSOLE', 'CONSOLE', None, 'Console'), 
     ('INFO', 'INFO', None, 'Info'),
     None],
    [('PREFERENCES', 'PREFERENCES', None, 'Preferences')]
    ]


# Define a custom Panel class
class AreaVisibilityPanel(bpy.types.Panel):
    # Define blender's ID name, space type, region type, and category for the Panel
    bl_label = "Area Types Visibility"
    bl_idname = "AREA_PT_visibility_panel"
    bl_space_type = 'TOPBAR'
    bl_region_type = 'HEADER'
    bl_category = "Visibility"

    # Draw method defines how the Panel is displayed
    def draw(self, context):
        layout = self.layout  # Get the layout of the panel
        wm = context.window_manager  # Get the window manager

        # Add a button to the layout that toggles the visibility of all areas
        layout.operator("wm.toggle_all_buttons", text="All Areas On Off")

        # Loop through each group of buttons
        for idx, button_group in enumerate(button_groups):
            for button_idx, button in enumerate(button_group):  # Loop through each button in the group
                if button is not None:  # If the button is not None (i.e., it exists)
                    area, icon, *ui_mode, custom_label = button  # Unpack the button data
                    prop_id = f"show_button_{idx}_{button_idx}"  # Create a unique ID for the button property
                    row = layout.row(align=True)  # Create a new row for each button
                    split = row.split(factor = 0.105)  # Split the row into two regions, with the left region taking up 15% of the width
                    split.scale_x = 0.7 # Reduce the horizontal scale of the left region to 70% to make the button more square
                    split.prop(wm, prop_id, text="", icon=icon, icon_only=True)  # Add a button to the left region with only an icon (no text)
                    split.scale_x = .5  # Reset the horizontal scale to avoid affecting subsequent UI elements
                    split.label(text=custom_label)  # Add a label to the right region
            
            # Add separator after each group
            layout.scale_y = 0.0  # Reduce the vertical scale to 50% to make the space between groups smaller
            layout.separator()  # Add a separator after each group
            layout.scale_y = 0.95  # Reset the vertical scale to avoid affecting subsequent UI elements







# Function to draw custom buttons in the top bar
def draw_func(self, context):
    if context.region.alignment == 'RIGHT':
        layout = self.layout
        row = layout.row(align=True)
        wm = context.window_manager

        # Define the number of separators to add after each group
        num_separators = 2

        # Loop through buttons and add them to the top bar
        for idx, button_group in enumerate(button_groups):
            group_has_visible_button = False
            for button_idx, button in enumerate(button_group):
                if button and getattr(wm, f"show_button_{idx}_{button_idx}", True):
                    area, icon, module, custom_label = button  # Unpack custom_label
                    # Removed text parameter from operator so only icon shows
                    op = row.operator("object.open_area_window", emboss=False, icon=icon)
                    op.area_type = area
                    if module:
                        op.ui_mode = module
                    group_has_visible_button = True
            # Add separators after each group that has at least one visible button
            if group_has_visible_button:
                for _ in range(num_separators):
                    row.separator()

        row.popover(panel="AREA_PT_visibility_panel", text="", icon="RESTRICT_VIEW_OFF")

# Register function
def register():
    bpy.utils.register_class(OpenAreaWindowOperator)
    bpy.utils.register_class(AreaVisibilityPanel)
    bpy.utils.register_class(WM_OT_ToggleAllButtons)

    # Add custom properties to WindowManager
    for idx, button_group in enumerate(button_groups):
        for button_idx, _ in enumerate(button_group):
            prop_id = f"show_button_{idx}_{button_idx}"
            setattr(bpy.types.WindowManager, prop_id, bpy.props.BoolProperty(default=True))

    # Add draw_func to top bar
    bpy.types.TOPBAR_HT_upper_bar.prepend(draw_func)

# Unregister function
def unregister():
    # Remove draw_func from top bar
    bpy.types.TOPBAR_HT_upper_bar.remove(draw_func)

    # Remove custom properties from WindowManager
    for idx, button_group in enumerate(button_groups):
        for button_idx, _ in enumerate(button_group):
            prop_id = f"show_button_{idx}_{button_idx}"
            delattr(bpy.types.WindowManager, prop_id)
