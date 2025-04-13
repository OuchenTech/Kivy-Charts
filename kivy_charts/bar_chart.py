from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, RoundedRectangle, Point, PushMatrix, PopMatrix, Rotate
from kivy.uix.label import Label
from kivy.properties import DictProperty, ListProperty, NumericProperty, ColorProperty, BooleanProperty, OptionProperty, StringProperty
from kivy.utils import get_color_from_hex
from kivy_gradient import Gradient
from kivy.uix.bubble import Bubble, BubbleContent
from kivy.clock import Clock
import re

class BarChart(Widget):
    """
    A customizable bar chart widget for Kivy applications.

    This widget creates a bar chart based on the provided data. It supports various
    customization options such as bar colors, grid, labels, and interactive mode.

    Attributes:
        data (DictProperty): A dictionary of label-value pairs for the chart.
        chart_mode (OptionProperty): Mode of the chart ('standard' or 'interactive').
        bubble_color (ColorProperty): Background color of the bubble displayed in interactive mode.
        color_style (OptionProperty): Color style of bars ('standard' or 'gradient').
        colors (ListProperty): List of colors for bars.
        bar_default_color (ColorProperty): Default color for bars.
        gradient_colors (ListProperty): Colors for gradient style.
        bar_radius (NumericProperty): Radius of bar corners.
        font_name (StringProperty): Font name for labels.
        value_color (ColorProperty): Color for value labels displayed above bars.
        value_font_size (NumericProperty): Font size for value labels displayed above bars.
        axis_label_color (ColorProperty): Color for x and y axis labels.
        axis_label_font_size (NumericProperty): Font size for x and y axis labels.
        x_axis_label_rotation (OptionProperty): Rotation angle for x-axis labels ('no-rotation', 'left-up', 'left-down').
        y_axis_labels (BooleanProperty): Whether to show y-axis labels.
        grid (BooleanProperty): Whether to show grid lines.
        grid_style (OptionProperty): Style of grid ('line', 'dashed', or 'dotted').
        grid_color (ColorProperty): Color of grid lines.
        title (StringProperty): Title of the chart.
        title_font_size (NumericProperty): Font size for the chart title.
        title_color (ColorProperty): Color for the chart title.
        no_data_text (StringProperty): Message to display when there is no data.
        no_data_font_size (NumericProperty): Font size for the no data text.
        no_data_text_color (ColorProperty): Color for the no data text.
    """
    data = DictProperty({})
    chart_mode = OptionProperty("standard", options=["standard", "interactive"])
    bubble_color = ColorProperty("skyblue")  # Default Skyblue color
    color_style = OptionProperty("standard", options=["standard", "gradient"])
    colors = ListProperty(None)
    bar_default_color = ColorProperty("#3498db")
    gradient_colors = ListProperty(["#33ff66", "#C3FF66"])
    bar_radius = NumericProperty(0)
    font_name = StringProperty("Roboto")
    value_color = ColorProperty((0, 0, 0, 1))
    value_font_size = NumericProperty(14)
    axis_label_color = ColorProperty((0, 0, 0, 1))
    axis_label_font_size = NumericProperty(14)
    x_axis_label_rotation = OptionProperty("no-rotation", options=["no-rotation", "left-up", "left-down"])
    y_axis_labels = BooleanProperty(False)
    grid = BooleanProperty(False)
    grid_style = OptionProperty("line", options=["line", "dashed", "dotted"])
    grid_color = ColorProperty([0.5, 0.5, 0.5, 0.5])
    title = StringProperty("")
    title_font_size = NumericProperty(16)
    title_color = ColorProperty((0, 0, 0, 1))
    no_data_text = StringProperty("No data available")
    no_data_font_size = NumericProperty(20)
    no_data_text_color = ColorProperty((0, 0, 0, 1))

    def __init__(self, **kwargs):
        """Initialize the BarChart widget."""
        super().__init__(**kwargs)
        self.bind(pos=self.update_chart, size=self.update_chart, 
                  data=self.update_chart, colors=self.update_chart,
                  gradient_colors=self.update_chart, grid=self.update_chart,
                  bar_radius=self.update_chart, grid_style=self.update_chart,
                  grid_color=self.update_chart, chart_mode=self.update_chart,
                  x_axis_label_rotation=self.update_chart)
        self.bar_infos = []

    def validate_input(self):
        """Validate the input data."""
        if not isinstance(self.data, dict):
            raise ValueError("Data must be a dictionary")

    def update_chart(self, *args):
        """
        Update the chart based on current properties.

        This method is called whenever a relevant property changes. It clears the
        existing chart and redraws it with the updated properties.
        """
        # Clear existing chart
        self.canvas.clear()
        self.clear_widgets()
        self.validate_input()
        
        if not self.data:
            if self.no_data_text:
                # Calculate center position relative to parent
                center_x = self.x + self.width / 2
                center_y = self.y + self.height / 2
                
                # Create the no data label
                no_data_label = Label(
                    text=self.no_data_text,
                    font_size=self.no_data_font_size,
                    font_name=self.font_name,
                    color=self.no_data_text_color,
                    size_hint=(None, None),
                )
                
                # Ensure the label has proper dimensions
                no_data_label.texture_update()
                label_width = no_data_label.texture_size[0] + 20  # Add some padding
                label_height = no_data_label.texture_size[1] + 10
                
                # Set the final size and position
                no_data_label.size = (label_width, label_height)
                no_data_label.pos = (
                    center_x - label_width / 2,
                    center_y - label_height / 2
                )
                
                # Add to widget tree
                self.add_widget(no_data_label)
            return
        
        # Generate gradient texture if needed
        if self.color_style == "gradient":
            try:
                self.gradient_texture = self.generate_gradient_texture()
            except ValueError as e:
                print(f"Error generating gradient texture: {e}")
                self.color_style = 'standard'

        # Calculate chart dimensions
        num_bars = len(self.data)
        max_value = max(self.data.values())
        title_height = 40 if self.title else 10
        
        # Increase bottom padding to provide more space for labels
        # Adjust based on rotation and screen resolution
        bottom_padding = 100 if self.x_axis_label_rotation != "no-rotation" else 70
        
        top_padding = 30
        left_padding = 60 if self.grid and self.y_axis_labels else 20
        right_padding = 30 if self.grid and self.y_axis_labels else 20

        chart_width = self.width - left_padding - right_padding
        chart_height = self.height - title_height - bottom_padding - top_padding
        
        bar_width = min((chart_width) / (num_bars * 1.5), 50)
        spacing = bar_width / 2
        total_bar_width = num_bars * bar_width + (num_bars - 1) * spacing
        
        # Center the chart
        start_x = self.x + left_padding + (chart_width - total_bar_width) / 2
        start_y = self.y + bottom_padding

        # Add title if present
        if self.title:
            title_label = Label(text=self.title, font_size=self.title_font_size, font_name=self.font_name,
                                color=self.title_color, size_hint=(None, None), size=(self.width, title_height))
            title_label.pos = (self.x, self.top - title_height)
            self.add_widget(title_label)

        # Draw grid if enabled
        if self.grid:
            self.draw_grid(start_x, total_bar_width, chart_height, max_value, start_y)

        self.bar_infos = []  # Reset bar info for interactive mode

        # Draw bars and labels
        for i, (label, value) in enumerate(self.data.items()):
            bar_height = (value / max_value) * chart_height
            bar_x = start_x + i * (bar_width + spacing)
            bar_y = start_y

            self.bar_infos.append({
                "x": bar_x,
                "y": bar_y,
                "width": bar_width,
                "height": bar_height,
                "value": value
            })

            # Draw bar
            with self.canvas:
                if self.color_style == "gradient" and self.gradient_texture:
                    Color(1, 1, 1, 1)
                    RoundedRectangle(
                        pos=(bar_x, bar_y), size=(bar_width, bar_height), radius=[self.bar_radius], texture=self.gradient_texture
                    )
                else:
                    Color(*self.get_color(i))
                    RoundedRectangle(
                        pos=(bar_x, bar_y), size=(bar_width, bar_height), radius=[self.bar_radius]
                    )

            # Add value label for standard mode
            if self.chart_mode == "standard":
                value_label = Label(
                    text=str(value), font_size=self.value_font_size, 
                    font_name=self.font_name, color=self.value_color, 
                    size_hint=(None, None),
                    )
                
                value_label.texture_update()
                value_label.size = value_label.texture_size
                # Center the label horizontally with the bar
                value_label.pos = (bar_x + (bar_width - value_label.width) / 2, bar_y + bar_height + 5)
                self.add_widget(value_label)

            # Add x-axis label
            x_axis_label = Label(
                text=label, font_size=self.axis_label_font_size,
                color=self.axis_label_color, size_hint=(None, None), 
                font_name=self.font_name
                )
            
            x_axis_label.texture_update()
            x_axis_label.size = (bar_width, x_axis_label.texture_size[1])  # Set height based on content
            
            # Position labels further away from the bars to prevent overlap
            # Use more spacing for rotated labels
            if self.x_axis_label_rotation == "no-rotation":
                label_y_pos = start_y - (bottom_padding/1.6)  # Increased distance from bars
            else:
                label_y_pos = start_y - (bottom_padding/1.8)  
                
            x_axis_label.pos = (bar_x, label_y_pos)
            
            # Rotate x-axis label 
            angle = 0
            if self.x_axis_label_rotation == "left-up":
                angle = 45
            elif self.x_axis_label_rotation == "left-down":
                angle = 315
                
            x_axis_label.canvas.before.clear()
            
            with x_axis_label.canvas.before:
                PushMatrix()
                Rotate(origin=x_axis_label.center, angle=angle)
            with x_axis_label.canvas.after:
                PopMatrix()
            self.add_widget(x_axis_label)

    def draw_grid(self, start_x, total_width, chart_height, max_value, start_y):
        """
        Draw the grid lines on the chart.

        Args:
            start_x (float): Starting x-coordinate of the chart area.
            total_width (float): Total width of the chart area.
            chart_height (float): Height of the chart area.
            max_value (float): Maximum value in the data.
            start_y (float): Starting y-coordinate of the chart area.
        """
        step = max_value / 5
        for i in range(6):
            value = max_value - step * i
            y = start_y + chart_height * (value / max_value)
            
            with self.canvas:
                Color(*self.grid_color)
                if self.grid_style == "line":
                    Line(points=[start_x - 10, y, start_x + total_width + 10, y], width=1)
                elif self.grid_style == "dashed":
                    for x in range(int(start_x - 10), int(start_x + total_width + 10), 20):
                        Line(points=[x, y, x + 10, y], width=1)
                else:  # dotted
                    for x in range(int(start_x - 10), int(start_x + total_width + 10), 10):
                        Point(points=[x, y], pointsize=1)
                        
            # Draw y-axis labels if enabled
            if self.y_axis_labels:
                y_axis_label = Label(
                    text=str(int(value)), font_size=self.axis_label_font_size, 
                    color=self.axis_label_color, size_hint=(None, None), 
                    font_name=self.font_name,
                    )
                
                y_axis_label.texture_update()
                y_axis_label.size = y_axis_label.texture_size
                # Right-align the label and position it to the left of the grid
                y_axis_label.pos = (start_x - y_axis_label.width - 15, y - y_axis_label.height/2)
                self.add_widget(y_axis_label)

    def is_valid_hex(self, color):
        """
        Check if a color string is a valid hex color.

        Args:
            color (str): The color string to check.

        Returns:
            bool: True if the color is a valid hex color, False otherwise.
        """
        return bool(re.match(r'^#[0-9a-fA-F]{6}$', color))
    
    def get_color(self, index):
        """
        Retrieve the color for a bar at the specified index.

        Args:
            index (int): The index of the bar.

        Returns:
            tuple: The RGBA color values as a tuple, with each component in the range [0, 1].

        Raises:
            ValueError: If the color format is invalid. This includes cases where:
                - The hex color string is not in the correct format (#RRGGBB).
                - The RGBA tuple/list does not have exactly 4 components.
                - The RGBA values are not within the range [0, 1].
        """
        if self.colors:
            color = self.colors[index % len(self.colors)]
            if isinstance(color, str):
                if color.startswith('#'):
                    if self.is_valid_hex(color):
                        return get_color_from_hex(color)
                    else:
                        raise ValueError(f"Invalid hex color format: {color}. Must be #RRGGBB (6 digits)")
                else:
                    raise ValueError(f"Invalid color format: {color}. String colors must be hex values starting with '#'")
            elif isinstance(color, (tuple, list)):
                if len(color) == 4:
                    if all(0 <= c <= 1 for c in color):
                        return color
                    else:
                        raise ValueError(f"Invalid RGBA color values: {color}. Values must be between 0 and 1.")
                else:
                    raise ValueError(f"Invalid RGBA color: {color}. Must be RGBA (4 values).")
            else:
                raise ValueError(f"Invalid color format: {color}. Must be a 6-digit hex string or RGBA tuple/list.")
        return self.bar_default_color
    
    def generate_gradient_texture(self):
        """
        Generate a gradient texture for the bars.

        Returns:
            Texture: The generated gradient texture.

        Raises:
            ValueError: If there are not enough colors or if the color format is invalid.
        """
        if len(self.gradient_colors) < 2:
            raise ValueError("At least two colors are required for a gradient.")
            
        for color in self.gradient_colors:   
            if isinstance(color, str):
                if not color.startswith('#') or not self.is_valid_hex(color):
                    raise ValueError(f"Invalid hex color format: {color}. Must be #RRGGBB (6 digits)")
            else: 
                raise ValueError(f"Invalid color format for gradient: {color}. Must be a 6-digit hex string.")
                
        _gradient_colors = [get_color_from_hex(color) for color in self.gradient_colors]
        return Gradient.vertical(*_gradient_colors)

    def on_touch_down(self, touch):
        """
        Handle touch events on the chart.

        This method is used in interactive mode to show value bubbles when bars are touched.

        Args:
            touch: The touch event.

        Returns:
            bool: True if the touch event was handled, False otherwise.
        """
        if self.chart_mode == 'interactive' and self.collide_point(*touch.pos):
            for bar_info in self.bar_infos:
                if self.point_inside_bar(touch.pos, bar_info):
                    self.show_value_bubble(bar_info['x'], bar_info['y'] + bar_info['height'], bar_info['value'])
                    return True
        return super().on_touch_down(touch)

    def point_inside_bar(self, point, bar_info):
        """
        Check if a point is inside a bar.

        Args:
            point (tuple): The (x, y) coordinates of the point.
            bar_info (dict): Information about the bar's position and size.

        Returns:
            bool: True if the point is inside the bar, False otherwise.
        """
        x, y = point
        return (bar_info['x'] <= x <= bar_info['x'] + bar_info['width'] and
                bar_info['y'] <= y <= bar_info['y'] + bar_info['height'])
    
    def show_value_bubble(self, x, y, value):
        """
        Show a bubble with the bar's value when touched in interactive mode.

        Args:
            x (float): The x-coordinate of the bar.
            y (float): The y-coordinate of the top of the bar.
            value: The value to display in the bubble.
        """
        # Calculate width based on the value length
        bubble_width = max(60, len(str(value)) * 15)
        
        # Calculate the center position of the bar
        bar_center_x = x + self.bar_infos[0]['width'] / 2
        
        # Position the bubble centered above the bar
        bubble_x = bar_center_x - bubble_width / 2
        bubble_y = y + 10  # Position it above the bar
        
        # Create the bubble without an arrow
        bubble = Bubble(
            size_hint=(None, None),
            size=(bubble_width, 0),  # Height will be set after label creation
            pos=(bubble_x, bubble_y),
            show_arrow=False  # No arrow
        )
        
        # Create bubble content with custom background
        content = BubbleContent(
            orientation="vertical",
            padding=[10, 10, 10, 10],  # Equal padding on all sides
            background_image="",
            background_color=self.bubble_color,  # Use bubble_color if defined, else default blue,
            border_auto_scale="both_lower",
            size_hint=(1, None),  # Allow height to adjust to content
            height=0  # Will be set once the label is added
        )
        
        # Add value label to the content, allowing its height to be natural
        bubble_label = Label(
            text=str(value),
            font_size=self.value_font_size,
            color=self.value_color,  
            font_name=self.font_name,
            size_hint=(1, None)  # No fixed height
        )
        
        # Update the texture to get the actual size
        bubble_label.texture_update()
        bubble_label.height = bubble_label.texture_size[1]
        
        # Add the label to the content
        content.add_widget(bubble_label)
        
        # Calculate proper heights based on label size
        label_height = bubble_label.texture_size[1]
        content_height = label_height + content.padding[1] + content.padding[3]  # Add top and bottom padding
        content.height = content_height
        bubble.height = content_height
        
        # Add the content to the bubble
        bubble.add_widget(content)
        
        # Add the bubble to the chart
        self.add_widget(bubble)
        
        # Remove the bubble after 2 seconds
        Clock.schedule_once(lambda dt: self.remove_widget(bubble), 2)
