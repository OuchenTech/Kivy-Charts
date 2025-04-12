from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line, Triangle
from kivy.uix.label import Label
from kivy.properties import DictProperty, ListProperty, NumericProperty, ColorProperty, OptionProperty, StringProperty, BooleanProperty
from kivy.utils import get_color_from_hex
import math

class PieChart(Widget):
    """
    PieChart Widget

    A base class for creating pie charts with legends and percentage labels.
    This class provides various customization options for fonts, colors, legends, 
    and percentage label positioning.

    Attributes:
    -----------
    data : DictProperty
        Data for the chart. Keys represent the labels, and values represent the respective values for each segment.

    colors : ListProperty
        List of colors for the chart segments. Defaults to a predefined set if not provided.

    font_name : StringProperty
        Font name for percentage and legend labels. Defaults to "Roboto".

    percentage_color : ColorProperty
        Color of percentage labels. Defaults to black `(0, 0, 0, 1)`.

    percentage_font_size : NumericProperty
        Font size of percentage labels. Defaults to `14`.

    percentage_distance_factor : NumericProperty
        Determines how far percentage labels are placed from the center of the pie chart. Defaults to `0.5`.

    show_legend : BooleanProperty
        Whether to display the legend. Defaults to `False`.

    legend_valign : OptionProperty
        Vertical alignment of the legend. Options: `'top'`, `'bottom'`, `'center'`. Defaults to `'center'`.

    legend_position : OptionProperty
        Position of the legend relative to the pie chart. Options: `'left'`, `'right'`. Defaults to `'left'`.

    legend_label_color : ColorProperty
        Color of the legend text labels. Defaults to black `(0, 0, 0, 1)`.

    legend_label_font_size : NumericProperty
        Font size for legend text labels. Defaults to `14`.

    legend_key_shape : OptionProperty
        Shape of the legend keys. Options: `'circle'`, `'square'`, `'diamond'`, `'hexagon'`, `'star'`. Defaults to `'circle'`.

    legend_key_style : OptionProperty
        Style of legend keys. Options: `'filled'`, `'outlined'`. Defaults to `'filled'`.

    no_data_text : StringProperty
        Text to display when no data is available. Defaults to "No data available".

    no_data_font_size : NumericProperty
        Font size for no data text. Defaults to `20`.

    no_data_text_color : ColorProperty
        Color of no data text. Defaults to black `(0, 0, 0, 1)`.

    Methods:
    --------
    update_chart():
        Updates the pie chart and redraws all components based on current data and properties.

    draw_legend_item(x, y, color, label):
        Draws a single legend item, including the shape and the text label.

    draw_polygon(cx, cy, radius, sides, filled):
        Draws a regular polygon with the given number of sides, radius, and fill style.

    draw_star(cx, cy, radius, points, filled):
        Draws a star with the given number of points, radius, and fill style.
    """
    
    data = DictProperty({})
    colors = ListProperty([])
    font_name = StringProperty("Roboto")
    percentage_color = ColorProperty((0, 0, 0, 1))  
    percentage_font_size = NumericProperty(14)      
    percentage_distance_factor = NumericProperty(0.5)
    show_legend = BooleanProperty(False)
    legend_valign = OptionProperty('center', options=['top', 'bottom', 'center'])  
    legend_position = OptionProperty('left', options=['left', 'right'])  
    legend_label_color = ColorProperty((0, 0, 0, 1))      
    legend_label_font_size = NumericProperty(14)          
    legend_key_shape = OptionProperty('circle', options=['circle', 'square', 'diamond', 'hexagon', 'star'])
    legend_key_style = OptionProperty('filled', options=['filled', 'outlined'])
    no_data_text = StringProperty("No data available")
    no_data_font_size = NumericProperty(20)
    no_data_text_color = ColorProperty((0, 0, 0, 1))

    def __init__(self, **kwargs):
        """
        Initializes the PieChart with default properties and binds updates to property changes.
        """
        super().__init__(**kwargs)
        self.bind(pos=self.update_chart, size=self.update_chart, data=self.update_chart,
                  colors=self.update_chart, percentage_distance_factor=self.update_chart,
                  legend_position=self.update_chart, legend_valign=self.update_chart, 
                  legend_key_shape=self.update_chart, legend_key_style=self.update_chart)

    def update_chart(self, *args):
        """
        Updates the pie chart whenever any relevant property changes or new data is provided.
        Redraws the chart, percentage labels, and the legend.
        """
        self.canvas.clear()
        self.clear_widgets()
        
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
        
        # Compute the total value to calculate percentages
        total_value = sum(self.data.values())
        if total_value == 0:
            return
        
        # Calculate dimensions and positions based on legend position
        if self.show_legend:
            legend_width = self.width / 3
            chart_width = 2 * self.width / 3
            
            if self.legend_position == 'right':
                legend_x = self.x + chart_width + 10
                chart_center_x = self.x + chart_width / 2
            else:  # legend_position == 'left'
                legend_x = self.x + 10
                chart_center_x = self.x + legend_width + (chart_width / 2)

            # Define some dimensions for the chart
            chart_radius = min(chart_width, self.height) / 2 - 10

            # Calculate the total height required for legend items
            legend_item_height = 30  # Each legend item height (including spacing)
            num_items = len(self.data)
            total_legend_height = num_items * legend_item_height

            # Determine the starting y position based on legend alignment
            if self.legend_valign == 'top':
                legend_y = self.top - 30
            elif self.legend_valign == 'bottom':
                legend_y = self.y + total_legend_height
            elif self.legend_valign == 'center':
                legend_y = self.y + (self.height - total_legend_height) / 2 + total_legend_height - legend_item_height
        else:
            # Without legend: Use full width for chart
            chart_width = self.width
            chart_center_x = self.x + (self.width / 2)
            chart_radius = min(self.width, self.height) / 2 - 10
            
        center_y = self.y + self.height / 2
        start_angle = 0
        
        # Store segment information for later label positioning
        segments = []

        # First pass: Draw pie segments
        for index, (label, value) in enumerate(self.data.items()):
            percentage = (value / total_value) * 100
            angle = (value / total_value) * 360

            # Get color for the segment
            segment_color = self.get_color(index)
            
            # Draw pie segment
            with self.canvas:
                Color(*segment_color)
                Ellipse(pos=(chart_center_x - chart_radius, center_y - chart_radius), 
                        size=(2 * chart_radius, 2 * chart_radius),
                        angle_start=start_angle, angle_end=start_angle + angle)

            # Store segment information for label positioning
            segments.append({
                'label': label,
                'percentage': percentage,
                'start_angle': start_angle,
                'end_angle': start_angle + angle,
                'color': segment_color
            })

            # Update the start angle for the next segment
            start_angle += angle

        # Second pass: Add percentage labels
        for segment in segments:
            # Calculate label position for the percentage
            mid_angle = math.radians((segment['start_angle'] + segment['end_angle']) / 2)
            label_x = chart_center_x + (chart_radius * self.percentage_distance_factor) * math.sin(mid_angle)
            label_y = center_y + (chart_radius * self.percentage_distance_factor) * math.cos(mid_angle)

            # Add percentage label
            percentage_label = Label(
                text=f"{segment['percentage']:.1f}%", 
                font_size=self.percentage_font_size,
                font_name=self.font_name,
                color=self.percentage_color, 
                size_hint=(None, None), 
            )
            percentage_label.texture_update()
            percentage_label.size = percentage_label.texture_size
            percentage_label.center = (label_x, label_y)
            self.add_widget(percentage_label)

            # Draw legend
            if self.show_legend:
                self.draw_legend_item(legend_x, legend_y, segment['color'], segment['label'])
                legend_y -= legend_item_height  # Move to the next legend item position

    def get_color(self, index):
        """
        Retrieves the color for the given index. Defaults to a predefined set of colors if none are provided.

        Parameters:
        -----------
        index : int
            Index of the segment.

        Returns:
        --------
        tuple
            RGBA color tuple for the segment.
        """
        default_colors = [
            "#ffd92f", "#a6d854", "#e78ac3", "#8da0cb", "#fc8d62", "#66c2a5", "#d0d0d0", "#ffb8bc"
        ]
        if self.colors:
            color = self.colors[index % len(self.colors)]
            return get_color_from_hex(color) if isinstance(color, str) else color
        else:
            color = default_colors[index % len(default_colors)]
            return get_color_from_hex(color)

    def draw_legend_item(self, x, y, color, label):
        """
        Draws a single legend item consisting of a key (shape) and its label.

        Parameters:
        -----------
        x : float
            X-coordinate for the position of the legend key.
        y : float
            Y-coordinate for the position of the legend key.
        color : tuple
            RGBA color of the legend key.
        label : str
            Text label for the legend item.
        """
        # Set color for the shape
        with self.canvas:
            Color(*color)
            
            if self.legend_key_shape == 'square':
                if self.legend_key_style == 'filled':
                    Rectangle(pos=(x, y), size=(10, 10))
                else:
                    Line(rectangle=(x, y, 15, 15), width=1.5)
            elif self.legend_key_shape == 'circle':
                if self.legend_key_style == 'filled':
                    Ellipse(pos=(x, y), size=(15, 15))
                else:
                    Line(circle=(x + 10, y + 10, 10), width=1.5)
            elif self.legend_key_shape == 'diamond':
                self.draw_polygon(x + 10, y + 10, 10, 4, filled=(self.legend_key_style == 'filled'))
            elif self.legend_key_shape == 'hexagon':
                self.draw_polygon(x + 10, y + 10, 10, 6, filled=(self.legend_key_style == 'filled'))
            elif self.legend_key_shape == 'star':
                self.draw_star(x + 10, y + 10, 10, 5, filled=(self.legend_key_style == 'filled'))
        
        # Add legend label 
        legend_label = Label(
            text=f"{label}", 
            font_size=self.legend_label_font_size,
            color=self.legend_label_color, 
            font_name=self.font_name,
            size_hint=(None, None), 
            size=(200, 20)
        )
        # Adjust alignment settings
        legend_label.halign = 'left'
        legend_label.text_size = legend_label.size
        legend_label.pos = (x + 30, y)
        self.add_widget(legend_label)

    def draw_polygon(self, cx, cy, radius, sides, filled=False):
        """
        Draws a regular polygon (e.g., hexagon, diamond) with a given number of sides.

        Parameters:
        -----------
        cx : float
            X-coordinate of the polygon's center.
        cy : float
            Y-coordinate of the polygon's center.
        radius : float
            Radius of the polygon.
        sides : int
            Number of sides for the polygon.
        filled : bool
            Whether the polygon should be filled or outlined.
        """
        angle_step = 2 * math.pi / sides
        points = []

        for i in range(sides):
            angle = i * angle_step
            x = cx + radius * math.sin(angle)
            y = cy + radius * math.cos(angle)
            points.append((x, y))

        if filled:
            # Draw filled polygon using triangles
            with self.canvas:
                for i in range(sides):
                    # Create triangles from center to each edge
                    p1 = points[i]
                    p2 = points[(i + 1) % sides]
                    self.canvas.add(Triangle(points=(cx, cy, p1[0], p1[1], p2[0], p2[1])))
        else:
            # Draw outlined polygon using lines
            with self.canvas:
                polygon_points = []
                for point in points:
                    polygon_points.extend(point)
                polygon_points.extend(points[0])  # Close the polygon
                Line(points=polygon_points, width=1.5)

    def draw_star(self, cx, cy, radius, points, filled=False):
        """
        Draws a star with a specified number of points.

        Parameters:
        -----------
        cx : float
            X-coordinate of the star's center.
        cy : float
            Y-coordinate of the star's center.
        radius : float
            Radius of the star's outermost points.
        points : int
            Number of points on the star.
        filled : bool
            Whether the star should be filled or outlined.
        """

        angle_step = math.pi / points
        star_points = []

        for i in range(2 * points):
            r = radius if i % 2 == 0 else radius / 2  # Alternate between outer and inner radius
            angle = i * angle_step
            x = cx + r * math.sin(angle)
            y = cy + r * math.cos(angle)
            star_points.append((x, y))

        if filled:
            # Draw filled star using triangles
            with self.canvas:
                for i in range(2 * points):
                    # Create triangles from center to each star point
                    p1 = star_points[i]
                    p2 = star_points[(i + 1) % (2 * points)]
                    self.canvas.add(Triangle(points=(cx, cy, p1[0], p1[1], p2[0], p2[1])))
        else:
            # Draw outlined star using lines
            with self.canvas:
                star_outline_points = []
                for point in star_points:
                    star_outline_points.extend(point)
                star_outline_points.extend(star_points[0])  # Close the star shape
                Line(points=star_outline_points, width=1.5)

class DonutChart(PieChart):
    """
    DonutChart Widget

    A subclass of `PieChart` for creating donut charts with a central hole.

    Attributes:
    -----------
    donut_radius : NumericProperty
        Radius of the donut hole, relative to the chart radius. Range: `0.2` to `0.8`. Default: `0.5`.

    donut_hole_color : ColorProperty
        Color of the central hole. Defaults to white `(1, 1, 1, 1)`.

    percentage_distance_factor : NumericProperty
        Automatically calculated to position percentage labels between the donut hole and the edge of the chart.
        Users can override this if needed.
        
    center_text : StringProperty
        Text to display in the center of the donut hole. Defaults to empty string.

    center_text_color : ColorProperty
        Color of the center text. Defaults to black.

    center_text_font_size : NumericProperty
        Font size of the center text. Defaults to 14.

    center_text_font_name : StringProperty
        Font name for the center text. Defaults to "Roboto".

    center_text_lines : NumericProperty
        Maximum number of lines for center text. Defaults to 2.

    Methods:
    --------
    update_chart():
        Overrides `PieChart.update_chart` to include the central donut hole.

    draw_donut_hole():
        Draws the central donut hole with the specified radius and color.
    """
    
    donut_radius = NumericProperty(0.5)  
    donut_hole_color = ColorProperty((1, 1, 1, 1))  
    percentage_distance_factor = NumericProperty(None)
    
    # New properties for center text
    center_text = StringProperty("")
    center_text_font_name = StringProperty("Roboto")
    center_text_color = ColorProperty((0, 0, 0, 1))
    center_text_font_size = NumericProperty(14)
    center_text_lines = NumericProperty(2)

    def __init__(self, **kwargs):
        """
        Initializes the DonutChart with default properties and binds updates to property changes.
        """
        super().__init__(**kwargs)
        self.bind(
            donut_radius=self.update_chart, 
            donut_hole_color=self.update_chart,
            center_text=self.update_chart
            )

    def update_chart(self, *args):
        """
        Overrides the `update_chart` method of `PieChart` to include a donut hole in the center of the chart.
        """
        
        # First check for no-data case (let parent handle it)
        if not self.data:
            super().update_chart(*args)
            return
        
        self.donut_radius = max(0.2, min(self.donut_radius, 0.8))

        # Automatically set percentage_distance_factor if not explicitly provided
        if self.percentage_distance_factor is None:
            self.percentage_distance_factor = (1 + self.donut_radius) / 2

        # Call the parent class's update_chart method to draw the pie chart
        super().update_chart(*args)

        # Add the donut hole
        self.draw_donut_hole()
        
    def draw_donut_hole(self):
        """
        Draws the central donut hole using the specified `donut_radius` and `donut_color`.
        The hole is properly centered whether or not the legend is shown.
        """
        if self.show_legend:
            # When legend is shown, use partial width
            legend_width = self.width / 3
            chart_width = 2 * self.width / 3
            
            if self.legend_position == 'right':
                chart_center_x = self.x + chart_width / 2
            else:  # legend_position == 'left'
                chart_center_x = self.x + legend_width + (chart_width / 2)
                
            chart_radius = min(chart_width, self.height) / 2 - 10
        else:
            # When legend is hidden, use full width
            chart_width = self.width
            chart_center_x = self.x + (self.width / 2)
            chart_radius = min(self.width, self.height) / 2 - 10

        center_y = self.y + self.height / 2

        # Inner radius of the donut hole
        hole_radius = chart_radius * self.donut_radius
        
        # Draw the hole
        with self.canvas:
            Color(*self.donut_hole_color)
            Ellipse(pos=(chart_center_x - hole_radius, center_y - hole_radius),
                    size=(2 * hole_radius, 2 * hole_radius))
            
        # Add center text if provided
        if self.center_text:
            # Calculate the maximum width available for text
            max_text_width = 2 * hole_radius * 0.9  # 90% of hole diameter
            
            # Create the label with text wrapping
            center_text_label = Label(
                text=self.center_text,
                font_size=self.center_text_font_size,
                font_name=self.center_text_font_name,
                color=self.center_text_color,
                size_hint=(None, None),
                size=(max_text_width, 2 * hole_radius),
                halign='center',
                valign='center'
            )
            
            # Enable text wrapping
            center_text_label.text_size = center_text_label.size
            center_text_label.max_lines = self.center_text_lines
            center_text_label.shorten = True
            
            # Position the label in the center of the hole
            center_text_label.pos = (
                chart_center_x - max_text_width / 2,
                center_y - hole_radius + (2 * hole_radius - center_text_label.height) / 2
            )
            
            self.add_widget(center_text_label)
