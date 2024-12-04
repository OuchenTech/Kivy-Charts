from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Triangle, Ellipse, Rectangle
from kivy.uix.label import Label
from kivy.properties import DictProperty, ListProperty, NumericProperty, ColorProperty, BooleanProperty, OptionProperty, StringProperty
from kivy.utils import get_color_from_hex
import math

class RadarChart(Widget):
    
    """
    A customizable Radar Chart widget for Kivy.
    
    Features:
    ---------
    - Visualizes multiple datasets on a radar chart.
    - Concentric polygonal or circular grid.
    - Adjustable dataset appearance (filled, outlined, or mixed styles).
    - Dynamic legend with customizable key shapes and labels.
    - Category labels and scale values displayed on the axes.
    
    Attributes:
    -----------
    max_value: NumericProperty
        Maximum value represented on the chart axes. Default is 100.
        
    font_name : StringProperty
        Font name for all radar chart labels. Defaults to "Roboto".
        
    data : DictProperty:
        Dictionary containing dataset names as keys and list of values as items.
        
    adjust_data : BooleanProperty:
        If True, adjusts datasets to match the number of categories. Default is False.
        
    missing_value_fill : NumericProperty
        Value used to fill missing dataset values. Default is 0.
        
    categories : ListProperty
        List of category names for the radar chart axes.
        
    category_label_offset : NumericProperty
        Spacing between the category labels and the grid. Default is 5.
        
    category_label_color : ColorProperty
        Color of category labels. Default is black (0, 0, 0, 1).
        
    category_label_font_size : NumericProperty
        Font size of category labels. Default is 14.
    
    num_grid_lines : NumericProperty
        Number of concentric grid lines. Default is 5.
    
    grid_style : OptionProperty
        Style of the grid ('polygonal' or 'circular'). Default is 'polygonal'.
    
    grid_color : ColorProperty
        Color of the grid lines. Default is gray (0.7, 0.7, 0.7, 0.5).
    
    grid_line_width : NumericProperty 
        Width of the grid lines. Default is 1.
    
    axis_line_color : ColorProperty 
        Color of the axis lines. Default is gray (0.7, 0.7, 0.7, 0.5).
    
    axis_line_width : NumericProperty 
        Width of the axis lines. Default is 1.5.
    
    dataset_colors : ListProperty 
        List of colors for the datasets. Default is a pre defined list colors.
    
    dataset_plot_style : OptionProperty
        Style of dataset visualization ('outlined', 'filled', 'mixed'). Default is 'outlined'.
    
    dataset_transparency : NumericProperty 
        Transparency level for filled dataset polygons (0 to 1). Default is 0.3.
        
    dataset_line_width : NumericProperty 
        Width of dataset lines. Default is 1.5.
    
    show_markers : BooleanProperty
        Whether to display markers on data points. Default is False.
    
    show_scale_values : BooleanProperty
        Whether to display scale values on the first axis. Default is True.
    
    scale_value_color : ColorProperty 
        Color of scale value labels. Default is black (0, 0, 0, 1).
    
    scale_value_font_size : NumericProperty
        Font size of scale value labels. Default is 12.
    
    show_legend : BooleanProperty
        Whether to display the legend. Default is False.
        
    legend_valign : OptionProperty 
        Vertical position of the legend ('top' or 'bottom'). Default is 'bottom'.
        
    legend_key_shape (OptionProperty): 
        Shape of legend keys ('square', 'circle', 'rectangle'). Default is 'square'.
    
    legend_label_color : ColorProperty
        Color of legend labels. Default is black (0, 0, 0, 1).
    
    legend_label_font_size : NumericProperty 
        Font size of legend labels. Default is 14.

    Methods:
    --------
    update_chart: 
        Redraws the radar chart when properties change.
        
    validate_data: 
        Ensures the `data` property is correctly formatted.
        
    validate_categories: 
        Ensures the `categories` property is correctly formatted.
        
    validate_missing_data_values: 
        Checks for mismatches between datasets and categories.
        
    adjust_data_to_categories: 
        Fills or truncates datasets to match the number of categories.
        
    draw_grid: 
        Draws concentric grid lines (polygonal or circular).
        
    draw_axes: 
        Draws the axis lines for each category.
        
    draw_category_labels: 
        Draws labels for each category.
        
    draw_scale_values: 
        Displays scale values on the first axis.
        
    plot_datasets: 
        Plots the datasets on the radar chart.
        
    draw_outlined_polygon: 
        Draws outlined polygons for datasets.
        
    draw_filled_polygon: 
        Draws filled polygons for datasets.
        
    draw_markers: 
        Adds markers to dataset points.
        
    draw_legend: 
        Dynamically creates rows of legend elements based on available width.
        
    get_label_width: 
        Estimates the width of a label based on its text and font size.
        
    adjust_alpha: 
        Adjusts the alpha (transparency) of a color.
        
    convert_to_rgba: 
        Converts a color from hex to RGBA format if needed.
        
    get_color:
        Retrieves the color for the given index.
    """
    
    max_value = NumericProperty(100)
    font_name = StringProperty('Roboto')
    data = DictProperty({})
    adjust_data = BooleanProperty(False)  
    missing_value_fill = NumericProperty(0)  
    categories = ListProperty([])
    category_label_offset = NumericProperty(5)
    category_label_color = ColorProperty((0, 0, 0, 1))
    category_label_font_size = NumericProperty(14)
    num_grid_lines = NumericProperty(5)
    grid_style = OptionProperty('polygonal', options=['polygonal', 'circular'])
    grid_color = ColorProperty((0.7, 0.7, 0.7, 0.5)) 
    grid_line_width = NumericProperty(1)
    axis_line_color = ColorProperty((0.7, 0.7, 0.7, 0.5))
    axis_line_width = NumericProperty(1.5)
    dataset_colors = ListProperty([])  
    dataset_plot_style = OptionProperty('outlined', options=['outlined', 'filled', 'mixed'])  
    dataset_transparency = NumericProperty(0.3) 
    dataset_line_width = NumericProperty(1.5)
    show_markers = BooleanProperty(False)   
    show_scale_values = BooleanProperty(True)
    scale_value_color = ColorProperty((0, 0, 0, 1))
    scale_value_font_size = NumericProperty(12)
    show_legend = BooleanProperty(False)  
    legend_valign = OptionProperty('bottom', options=['top', 'bottom'])
    legend_key_shape = OptionProperty('square', options=['square', 'circle', 'rectangle'])
    legend_label_color = ColorProperty((0, 0, 0, 1))
    legend_label_font_size = NumericProperty(14)

    def __init__(self, **kwargs):
        """
        Initializes the RadarChart with default properties and binds updates to property changes.
        """
        super().__init__(**kwargs)
        self.legend_container = None  # Initially no legend container
        self.bind(pos=self.update_chart, size=self.update_chart,
                  data=self.update_chart, categories=self.update_chart,
                  grid_style=self.update_chart, dataset_plot_style=self.update_chart, 
                  show_legend=self.handle_legend_container
                  )

    def update_chart(self, *args):
        """
        Redraws the radar chart whenever relevant properties change.

        The method validates data and category inputs, adjusts the chart layout
        (grid, axes, datasets, labels, and legend), and clears any previous drawings
        and widgets to avoid duplication.
        """
        
        # Validate the type and structure of data and categories 
        self.validate_data()
        self.validate_categories()
        
        # Validate or adjust data
        if not self.adjust_data:
            self.validate_missing_data_values()
        else:
            self.data = self.adjust_data_to_categories()
            
        # Handle legend container
        self.handle_legend_container()
        
        # Clear the canvas and widgets to avoid duplications
        self.canvas.clear()  
        self.clear_widgets() 

        if not self.data or not self.categories:
            return
        
        # Adjust radar chart and legend dimensions
        legend_height = self.height * 0.2 if self.show_legend else 0
        chart_area_height = self.height - legend_height
        center_x = self.center_x
        if self.show_legend and self.legend_valign == 'bottom':
            center_y = self.y + legend_height + chart_area_height / 2
        elif self.show_legend and self.legend_valign == 'top':
            center_y = self.y + chart_area_height / 2
        else:
            center_y = self.center_y
        radius = min(self.width, chart_area_height) / 2 - 40
        angle_step = 2 * math.pi / len(self.categories)

        # Draw grid lines (concentric polygons/ circles)
        self.draw_grid(center_x, center_y, radius, angle_step)

        # Draw axis lines
        self.draw_axes(center_x, center_y, radius, angle_step)

        # Draw category labels separately
        self.draw_category_labels(center_x, center_y, radius, angle_step)

        # Draw scale values on the first axis
        if self.show_scale_values:
            self.draw_scale_values(center_x, center_y, radius, angle_step)

        # Plot datasets
        self.plot_datasets(center_x, center_y, radius, angle_step)
        
        # Draw legend if enabled
        if self.show_legend:
            self.draw_legend(legend_height)
   
    def validate_data(self):
        """
        Validates that the `data` property is a dictionary with valid keys and list values.
        
        Raises:
        -------
        ValueError:
            - If `data` is not a dictionary.
            - If keys in `data` are not strings.
            - If values in `data` are not lists of numerical values.
        """
        if not isinstance(self.data, dict):
            raise ValueError("The `data` property must be a dictionary.")
        for key, values in self.data.items():
            if not isinstance(key, str):
                raise ValueError("Each key in `data` must be a string representing a dataset name.")
            if not isinstance(values, list):
                raise ValueError(f"The values for dataset '{key}' must be a list of numerical values.")
            if not all(isinstance(value, (int, float)) for value in values):
                raise ValueError(f"All values in dataset '{key}' must be integers or floats.")
                
    def validate_categories(self):
        """
        Validates that the `categories` property is a list of strings.

        Raises:
        -------
        ValueError:
            - If `categories` is not a list.
            - If any element in `categories` is not a string.
        """
        if not isinstance(self.categories, list):
            raise ValueError("The `categories` property must be a list.")
        if not all(isinstance(category, str) for category in self.categories):
            raise ValueError("All items in `categories` must be strings.")
        
    def validate_missing_data_values(self):
        """
        Ensures that each dataset in `data` matches the number of `categories`.

        Raises:
        -------
        ValueError:
            - If a dataset's values do not match the number of categories.
        """
        for dataset_label, values in self.data.items():
            if len(values) != len(self.categories):
                raise ValueError(
                    f"Dataset '{dataset_label}' has {len(values)} values, but {len(self.categories)} values are expected."
                )

    def adjust_data_to_categories(self):
        """
        Adjusts datasets to match the number of categories.

        Missing values are filled using the `missing_value_fill` property,
        and excess values are truncated.

        Returns:
        --------
        dict:
            The adjusted data dictionary.
        """
        adjusted_data = {}
        num_categories = len(self.categories)

        for dataset_label, values in self.data.items():
            if len(values) < num_categories:
                adjusted_values = values + [self.missing_value_fill] * (num_categories - len(values))
            else:
                adjusted_values = values[:num_categories]
            adjusted_data[dataset_label] = adjusted_values

        return adjusted_data

    def draw_grid(self, center_x, center_y, radius, angle_step):
        """
        Draws the concentric grid lines (polygonal or circular) for the radar chart.

        Parameters:
        -----------
        center_x : float
            X-coordinate of the chart's center.
        center_y : float
            Y-coordinate of the chart's center.
        radius : float
            The radius of the chart's outermost grid.
        angle_step : float
            Angle between each category in radians.
        """
        with self.canvas:
            Color(*self.grid_color)
            for i in range(1, self.num_grid_lines + 1):
                if self.grid_style == 'polygonal':
                    # Concentric Polygonal Grid
                    points = []
                    for j in range(len(self.categories)):
                        x = center_x + (radius * (i / self.num_grid_lines)) * math.sin(j * angle_step)
                        y = center_y + (radius * (i / self.num_grid_lines)) * math.cos(j * angle_step)
                        points.extend([x, y])
                    points.extend([points[0], points[1]])  # Close the shape
                    Line(points=points, width=self.grid_line_width)
                elif self.grid_style == 'circular':
                    # Concentric Circular Grid
                    r = radius * (i / self.num_grid_lines)
                    Line(circle=(center_x, center_y, r), width=self.grid_line_width)

    def draw_axes(self, center_x, center_y, radius, angle_step):
        """
        Draws the axes connecting the chart's center to the grid points.

        Parameters:
        -----------
        center_x : float
            X-coordinate of the chart's center.
        center_y : float
            Y-coordinate of the chart's center.
        radius : float
            The radius of the chart's outermost grid.
        angle_step : float
            Angle between each category in radians.
        """
        with self.canvas:
            Color(*self.axis_line_color)  # Set the color for axis lines
            for i in range(len(self.categories)):
                # Draw the axis line
                x = center_x + radius * math.sin(i * angle_step)
                y = center_y + radius * math.cos(i * angle_step)
                Line(points=[center_x, center_y, x, y], width=self.axis_line_width)

    def draw_category_labels(self, center_x, center_y, radius, angle_step):
        """
        Draws the labels for each category at the outer edge of the chart, with dynamic positioning
        to prevent overlap based on label alignment and spacing.

        Parameters:
        -----------
        center_x : float
            X-coordinate of the chart's center.
        center_y : float
            Y-coordinate of the chart's center.
        radius : float
            The radius of the chart's outermost grid.
        angle_step : float
            Angle between each category in radians.
        """
        for i, category in enumerate(self.categories):
            # Calculate the angle for this category
            angle = i * angle_step
            x = center_x + (radius + self.category_label_offset) * math.sin(angle)
            y = center_y + (radius + self.category_label_offset) * math.cos(angle)

            # Create the category label
            category_label = Label(
                text=category,
                font_name=self.font_name,
                font_size=self.category_label_font_size,
                color=self.category_label_color,
                size_hint=(None, None),
                size=(100, 30),
                valign="middle",
            )
            category_label.text_size = category_label.size  # Enable text wrapping if needed

            # Adjust label position and alignment
            if 0 < angle < math.pi:  # Top-right to bottom-right (0° < angle < 180°)
                category_label.halign = "left"
                category_label.x = x + 10  # Shift to the right of the grid
                category_label.y = y - category_label.height / 2
            elif math.pi < angle < 2 * math.pi:  # Bottom-left to top-left (180° < angle < 360°)
                category_label.halign = "right"
                category_label.x = x - category_label.width - 10  # Shift to the left of the grid
                category_label.y = y - category_label.height / 2
            elif angle == 0:  # Directly at the top (0°)
                category_label.halign = "center"
                category_label.x = x - category_label.width / 2
                category_label.y = y
            elif angle == math.pi:  # Directly at the bottom (180°)
                category_label.halign = "center"
                category_label.x = x - category_label.width / 2
                category_label.y = y - category_label.height

            # Add the label to the chart
            self.add_widget(category_label)

    def draw_scale_values(self, center_x, center_y, radius, angle_step):
        """
        Draws scale values along the first axis to represent grid line intervals.

        Parameters:
        -----------
        center_x : float
            X-coordinate of the chart's center.
        center_y : float
            Y-coordinate of the chart's center.
        radius : float
            The radius of the chart's outermost grid.
        angle_step : float
            Angle between each category in radians.
        """
        for i in range(1, self.num_grid_lines + 1):
            # Calculate the position for each scale value
            value = (i / self.num_grid_lines) * self.max_value
            x = center_x + (radius * (i / self.num_grid_lines)) * math.sin(0 * angle_step)
            y = center_y + (radius * (i / self.num_grid_lines)) * math.cos(0 * angle_step)
            
            # Create a label for the scale value
            scale_label = Label(
                text=str(int(value)),
                font_name = self.font_name,
                font_size=self.scale_value_font_size,
                color=self.scale_value_color,
                size_hint=(None, None),
                size=(30, 20),
            )
            scale_label.center = (x + 15, y)  # Adjust to prevent overlap with the axis line
            self.add_widget(scale_label)

    def plot_datasets(self, center_x, center_y, radius, angle_step):
        """
        Plots datasets as polygons or outlines on the radar chart.

        Parameters:
        -----------
        center_x : float
            X-coordinate of the chart's center.
        center_y : float
            Y-coordinate of the chart's center.
        radius : float
            The radius of the chart's outermost grid.
        angle_step : float
            Angle between each category in radians.
        """
        for idx, (dataset_label, values) in enumerate(self.data.items()):
            if len(values) != len(self.categories):
                continue

            # Retrieve and convert the color for the dataset
            get_color = self.get_color(idx)
            dataset_color = self.convert_to_rgba(get_color)
            points = []
            for i, value in enumerate(values):
                value_ratio = value / self.max_value
                x = center_x + (radius * value_ratio) * math.sin(i * angle_step)
                y = center_y + (radius * value_ratio) * math.cos(i * angle_step)
                points.extend([x, y])
            
            points.extend([points[0], points[1]])  # Close the shape
            
            # Handle different plot styles
            if self.dataset_plot_style in ['filled', 'mixed']:
                self.draw_filled_polygon(center_x, center_y, points, dataset_color)

            if self.dataset_plot_style in ['outlined', 'mixed']:
                self.draw_outlined_polygon(points, dataset_color)

            # Draw markers if enabled
            if self.show_markers and self.dataset_plot_style in ['outlined', 'mixed']:
                self.draw_markers(center_x, center_y, values, radius, angle_step, dataset_color)
                
    def draw_outlined_polygon(self, points, color):
        """
        Draws the outline of a polygon representing a dataset.
        
        Parameters:
        -----------
        points : list
            List of coordinates forming the polygon's vertices.
        color : tuple
            RGBA color for the outline.
        """
        with self.canvas:
            Color(*color)  # Fully opaque for the outline
            Line(points=points, width=self.dataset_line_width, close=True)
                
    def draw_filled_polygon(self, center_x, center_y, points, color):
        """
        Draws a filled polygon representing a dataset.

        Parameters:
        -----------
        center_x : float
            X-coordinate of the chart's center.
        center_y : float
            Y-coordinate of the chart's center.
        points : list
            List of coordinates forming the polygon's vertices.
        color : tuple
            RGBA color for the fill.
        """
        transparent_color = self.adjust_alpha(color, self.dataset_transparency)
        with self.canvas:
            Color(*transparent_color)
            for i in range(0, len(points) - 2, 2):
                Triangle(points=(center_x, center_y, points[i], points[i + 1], points[i + 2], points[i + 3]))
    
    def draw_markers(self, center_x, center_y, values, radius, angle_step, color):
        """
        Draws markers at each data point on the radar chart.

        Parameters:
        -----------
        center_x : float
            X-coordinate of the chart's center.
        center_y : float
            Y-coordinate of the chart's center.
        values : list
            Data points to be marked.
        radius : float
            The radius of the chart's outermost grid.
        angle_step : float
            Angle between each category in radians.
        color : tuple
            RGBA color for the markers.
        """
        with self.canvas:
            Color(*color)
            for i, value in enumerate(values):
                value_ratio = value / self.max_value
                x = center_x + (radius * value_ratio) * math.sin(i * angle_step)
                y = center_y + (radius * value_ratio) * math.cos(i * angle_step)
                Ellipse(pos=(x - 4, y - 4), size=(6, 6))
                
    def handle_legend_container(self, *args):
        """
        Manages the creation or removal of the legend container widget based on the `show_legend` property.

        Parameters:
        -----------
        *args : tuple
            Positional arguments passed automatically during property binding or method invocation.
            These arguments are not used within the method but are required for compatibility with Kivy's
            event binding system.
        """
        if self.show_legend:
            if not self.legend_container:  # Add container if not already created
                self.legend_container = Widget()
                self.add_widget(self.legend_container)
        elif self.legend_container:  # Remove container if it exists
            self.remove_widget(self.legend_container)
            self.legend_container = None
                
    def draw_legend(self, legend_height):
        """
        Draws the legend for the radar chart, dynamically creating rows to fit the available width.

        Parameters:
        -----------
        legend_height : float
            The height of the legend area.
        """
        # Clear the legend container to remove old labels and avoid diplications
        if self.legend_container:
            self.legend_container.clear_widgets()

        legend_y = self.y if self.legend_valign == 'bottom' else self.y + self.height - legend_height

        # Parameters for layout
        key_size = 20  # Size of the key (square/rectangle)
        key_label_spacing = 10  # Space between key and label
        element_spacing = 20  # Space between elements (label-to-next-key spacing)
        row_height = key_size + 20  # Height of each row, including padding

        # Calculate the maximum label width
        max_label_width = max(self.get_label_width(label, self.legend_label_font_size) for label in self.data.keys())

        # Calculate the element width using the widest label
        element_width = key_size + key_label_spacing + max_label_width + element_spacing

        # Calculate the number of elements per row
        available_width = self.width
        max_elements_per_row = max(1, int(available_width // element_width))

        # Split legend elements into rows
        elements = list(self.data.keys())
        rows = [
            elements[i:i + max_elements_per_row]
            for i in range(0, len(elements), max_elements_per_row)
        ]

        # Calculate total legend height
        total_legend_height = len(rows) * row_height
        legend_y_start = legend_y + legend_height - total_legend_height if self.legend_valign == 'top' else legend_y

        # Draw the legend
        with self.canvas:
            for row_idx, row in enumerate(rows):
                # Calculate the y-coordinate for this row
                row_y_center = legend_y_start + total_legend_height - (row_idx + 0.5) * row_height

                # Calculate the total row width for centering
                row_width = len(row) * element_width - element_spacing  # Remove trailing spacing
                row_start_x = self.center_x - row_width / 2

                # Draw each element in the row
                current_x = row_start_x
                for dataset_label in row:
                    # Retrieve the color using get_color method
                    idx = elements.index(dataset_label)
                    get_color = self.get_color(idx)

                    # Determine the key color based on dataset_plot_style
                    if self.dataset_plot_style == 'filled':
                        key_color = self.adjust_alpha(get_color, self.dataset_transparency)
                    else:  # 'outlined' or 'mixed'
                        key_color = get_color

                    # Draw the key shape
                    Color(*key_color)
                    if self.legend_key_shape == 'square':
                        Rectangle(pos=(current_x, row_y_center - key_size / 2), size=(key_size, key_size))
                    elif self.legend_key_shape == 'circle':
                        Ellipse(pos=(current_x, row_y_center - key_size / 2), size=(key_size, key_size))
                    elif self.legend_key_shape == 'rectangle':
                        Rectangle(pos=(current_x, row_y_center - (key_size / 2) / 2), size=(key_size, key_size / 2))

                    # Adjust `current_x` for the legend label
                    current_x += key_size + key_label_spacing

                    # Calculate legend label position
                    legend_label = Label(
                        text=dataset_label,
                        font_name=self.font_name,
                        font_size=self.legend_label_font_size,
                        color=self.legend_label_color,
                        size_hint=(None, None),
                        size=(max_label_width, 20),  # Use max_label_width for consistency
                        halign="left",
                    )
                    legend_label.text_size = (max_label_width, None)  # Enable text wrapping
                    legend_label.x = current_x
                    legend_label.y = row_y_center - legend_label.height / 2

                    # Add the legend label to the legend container
                    self.legend_container.add_widget(legend_label)

                    # Move `current_x` to the next element
                    current_x += max_label_width + element_spacing

    def get_label_width(self, text, font_size):
        """
        Calculates the precise width of a label's text given its font size.
        
        Parameters:
        -----------
        text : str
            The text to measure.
        font_size : int
            The font size of the text.
        
        Returns:
        --------
        float
            The calculated width of the text.
        """
        temp_label = Label(
            text=text,
            font_name=self.font_name,
            font_size=font_size,
            size_hint=(None, None)
        )
        temp_label.texture_update()  # Ensure the texture is updated for size calculations
        return temp_label.texture_size[0]
                
    def adjust_alpha(self, color, alpha):
        """
        Adjusts the alpha (transparency) of an RGBA color.

        Parameters:
        -----------
        color : tuple
            Original RGBA color.
        alpha : float
            Desired alpha value.

        Returns:
        --------
        tuple:
            RGBA color with adjusted alpha.
        """
        if len(color) == 4:
            return (color[0], color[1], color[2], alpha)
        elif len(color) == 3:
            return (color[0], color[1], color[2], alpha)
        return color  # Return as-is if not a valid color format
    
    def convert_to_rgba(self, color):
        """Converts a color from hex to RGBA if needed.
        
        Parameters:
        -----------
        color : str or tuple
            Hex string or RGBA tuple.

        Returns:
        --------
        tuple:
            RGBA color.
        """
        if isinstance(color, str):  # If color is a hex string
            return get_color_from_hex(color)
        return color  # If already in RGBA format, return as-is
    
    def get_color(self, index):
        """
        Retrieves the color for the given index. Defaults to a predefined set of colors if none are provided.

        Parameters:
        -----------
        index : int
            Index of the dataset.

        Returns:
        --------
        tuple
            RGBA color tuple for the dataset.
        """
        default_colors = [
            "#1f77b4", # muted blue
            "#d62728", #brick red
            "#2ca02c", #cooked asparagus green
            "#ff7f0e", #safety orange
            "#9467bd", #muted purple
            "#8c564b", #chestnut brown
        ]
        
        if self.dataset_colors:
            color = self.dataset_colors[index % len(self.dataset_colors)]
            return get_color_from_hex(color) if isinstance(color, str) else color
        else:
            color = default_colors[index % len(default_colors)]
            return get_color_from_hex(color) if isinstance(color, str) else color