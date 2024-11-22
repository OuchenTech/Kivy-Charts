# Kivy Charts

Kivy Charts is a customizable chart library for Kivy applications. This library allows developers to easily integrate charts into their Kivy apps, with support for various customization options to tailor the charts to specific needs. Currently, the library includes a Bar Chart, Pie Chart, and Donut Chart widgets, with more chart types to be added in the future.

## Table of Contents
- [Installation](#installation)
- [Requirements](#requirements)
- [Charts](#charts)
  - [Bar Chart](#bar-chart)
    - [Features](#features)
    - [Usage](#usage)
    - [BarChart Properties](#barchart-properties)
    - [Examples](#examples)
  - [Pie Chart](#pie-chart)
    - [Features](#features)
    - [Usage](#usage)
    - [PieChart Properties](#piechart-properties)
    - [Examples](#examples)
  - [Donut Chart](#donut-chart)
    - [Features](#features)
    - [Usage](#usage)
    - [DonutChart Properties](#donutchart-properties)
    - [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the Kivy Charts library, clone this repository and include it in your Kivy project:

```bash
git clone https://github.com/OuchenTech/kivy_charts.git
```

Then, in your Kivy project, import the required chart widget:

```python
from kivy_charts.bar_chart import BarChart
from kivy_charts.pie_chart import PieChart, DonutChart
```

## Requirements

- Python 3.7+
- Kivy = 2.3.0
- Kivymd = https://github.com/kivymd/KivyMD/archive/master.zip
- KivyGradient = 0.0.5

## Charts

### Bar Chart

The BarChart widget provides a customizable bar chart for visualizing data in your Kivy applications.

#### Features

- Customizable bar charts with support for gradient and standard color styles.
- Configurable grid styles and labels.
- Support for rotating x-axis labels.
- Interactive mode for displaying values on touch.

#### Usage

To use the BarChart widget in your Kivy app, simply add it to your layout and set the desired properties:

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_charts.bar_chart import BarChart

class MyChartApp(App):

    def build(self):
        layout = BoxLayout()
        data = {"A": 10, "B": 20, "C": 30}
        bar_chart = BarChart(data=data, title="My Bar Chart")
        layout.add_widget(bar_chart)
        return layout

if __name__ == '__main__':
    MyChartApp().run()
```

#### BarChart Properties

Here are all the properties available for the BarChart widget, allowing for extensive customization:

##### `data`:
- **Type:** `DictProperty`
- **Description:** A dictionary containing the keys and their corresponding values.
- **Default:** `{}`
- **Usage:** Set the data to be displayed in the bar chart.

##### `chart_mode`:
- **Type:** `OptionProperty`
- **Options:** `'standard'`, `'interactive'`
- **Description:** Mode of the chart; in 'interactive' mode, values are displayed on touch.
- **Default:** `'standard'`
- **Usage:** Use `'interactive'` to show values on touch; otherwise, use `'standard'`.

##### `color_style`:
- **Type:** `OptionProperty`
- **Options:** `'standard'`, `'gradient'`
- **Description:** Color style of the bars. If set to 'gradient', bars will use gradient colors defined in gradient_colors.
- **Default:** `'standard'`

##### `colors`:
- **Type:** `ListProperty`
- **Description:** A list of colors for the bars (Accept colors in RGBA and hex format). Only applicable when color_style is set to `'standard'`.
- **Default:** `None`

##### `bar_default_color`:
- **Type:** `ColorProperty`
- **Description:** Default color for bars if colors are not provided. Applies when color_style is set to `'standard'`.
- **Default:** '#3498db'

##### `gradient_colors`:
- **Type:** `ListProperty`
- **Description:** Colors used for gradient bars. This property is only used when color_style is set to 'gradient'.
- **Default:** `['#33ff66', '#C3FF66']`

##### `bar_radius`:
- **Type:** `NumericProperty`
- **Description:** Radius of the bar corners.
- **Default:** `0`
- **Usage:** Set this property to give rounded corners to the bars.

##### `label_font_name`:
- **Type:** `StringProperty`
- **Description:** Font name used for the labels.
- **Default:** 'Roboto'

##### `label_size`:
- **Type:** `NumericProperty`
- **Description:** Font size for the labels.
- **Default:** `14`

##### `label_color`:
- **Type:** `ColorProperty`
- **Description:** Color of the labels.
- **Default:** `(0, 0, 0, 1)`

##### `x_axis_label_rotation`:
- **Type:** `OptionProperty`
- **Options:** `'no-rotation'`, `'left-up'`, `'left-down'`.
- **Description:** Rotation angle for x-axis labels.
- **Default:** `'no-rotation'`

##### `y_axis_labels`:
- **Type:** `BooleanProperty`
- **Description:** Whether to show y-axis labels.
- **Default:** `False`

##### `grid`:
- **Type:** `BooleanProperty`
- **Description:** Whether to show grid lines.
- **Default:** `False`

##### `grid_style`:
- **Type:** `OptionProperty`
- **Options:** `'line'`, `'dashed'`, `'dotted'`.
- **Description:** Style of the grid lines. Only applies when grid is True.
- **Default:** `'line'`

##### `grid_color`:
- **Type:** `ColorProperty`
- **Description:** Color of the grid lines. Only applies when grid is True.
- **Default:** `[0.5, 0.5, 0.5, 0.5]`

##### `title`:
- **Type:** `StringProperty`
- **Description:** Title of the chart.
- **Default:** `""`
- **Usage:** Set this property to display a title at the top of the chart.

#### Examples

##### Example 1:

```python
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy_charts.bar_chart import BarChart

class MainApp(MDApp):

    def build(self):

        main_layout = MDFloatLayout(md_bg_color='skyblue')

        box_layout = MDBoxLayout(
            size_hint=(None, None),
            size=(500, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color='white'
        )

        data = {'Jan': 300, 'Feb': 500, 'Mar': 250, 'Apr': 800, 'Mai': 400, 'Jun': 120, 'Jul': 450}
        
        chart = BarChart(
            data=data, 
            title="Monthly Sales ($)",
            size_hint=(1, 1),
        )
        
        box_layout.add_widget(chart)
        main_layout.add_widget(box_layout)

        return main_layout

if __name__ == '__main__':
    MainApp().run()
```


##### Output:
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/bar_chart/example1.PNG)


##### Example 2:

```python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy_charts.bar_chart import BarChart

class MainApp(MDApp):
    
    def build(self):

        main_layout = MDFloatLayout(md_bg_color='skyblue')

        box_layout = MDBoxLayout(
            size_hint=(None, None),
            size=(500, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color='white'
        )

        data = {'Jan': 300, 'Feb': 500, 'Mar': 250, 'Apr': 800, 'Mai': 400, 'Jun': 120, 'Jul': 450}
        
        chart = BarChart(
            data=data, 
            title="Monthly Sales ($)",
            colors=['#C9190B', '#F4C145', '#8F4700', (1, 1, 0, 1), (1, 0, .5, 1), (0, 1, 1, 1), (.3, .3, .2, 1)],
            size_hint=(1, 1),
        )
        
        box_layout.add_widget(chart)
        main_layout.add_widget(box_layout)

        return main_layout

if __name__ == '__main__':
    MainApp().run()
```


##### Output:
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/bar_chart/example2.PNG)


##### Example 3:

```python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy_charts.bar_chart import BarChart

class MainApp(MDApp):
    
    def build(self):

        main_layout = MDFloatLayout(md_bg_color='skyblue')

        box_layout = MDBoxLayout(
            size_hint=(None, None),
            size=(500, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color='white'
        )

        data = {'Jan': 300, 'Feb': 500, 'Mar': 250, 'Apr': 800, 'Mai': 400, 'Jun': 120, 'Jul': 450}
        
        chart = BarChart(
            data=data, 
            title="Monthly Sales ($)",
            color_style='gradient',
            size_hint=(1, 1),
        )
        
        box_layout.add_widget(chart)
        main_layout.add_widget(box_layout)

        return main_layout

if __name__ == '__main__':
    MainApp().run()
```


##### Output:
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/bar_chart/example3.PNG)


##### Example 4:

```python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy_charts.bar_chart import BarChart

class MainApp(MDApp):
    
    def build(self):

        main_layout = MDFloatLayout(md_bg_color='skyblue')

        box_layout = MDBoxLayout(
            size_hint=(None, None),
            size=(500, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color='white'
        )

        data = {'Jan': 300, 'Feb': 500, 'Mar': 250, 'Apr': 800, 'Mai': 400, 'Jun': 120, 'Jul': 450}
        
        chart = BarChart(
            data=data, 
            title="Monthly Sales ($)",
            color_style='gradient',
            gradient_colors=['#25aae1', '#eb72ac'],
            bar_radius=10,
            size_hint=(1, 1),
        )
        
        box_layout.add_widget(chart)
        main_layout.add_widget(box_layout)

        return main_layout

if __name__ == '__main__':
    MainApp().run()
```


##### Output:
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/bar_chart/example4.PNG)


##### Example 5:

```python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy_charts.bar_chart import BarChart

class MainApp(MDApp):
    
    def build(self):

        main_layout = MDFloatLayout(md_bg_color='skyblue')

        box_layout = MDBoxLayout(
            size_hint=(None, None),
            size=(500, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color='white'
        )

        data = {'Jan': 300, 'Feb': 500, 'Mar': 250, 'Apr': 800, 'Mai': 400, 'Jun': 120, 'Jul': 450}
        
        chart = BarChart(
            data=data, 
            title="Monthly Sales ($)",
            color_style='gradient',
            gradient_colors=['#25aae1', '#eb72ac'],
            bar_radius=10,
            grid=True,
            grid_style='dotted',
            x_axis_label_rotation = 'left-down',
            size_hint=(1, 1),
        )
        
        box_layout.add_widget(chart)
        main_layout.add_widget(box_layout)

        return main_layout

if __name__ == '__main__':
    MainApp().run()
```


##### Output:
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/bar_chart/example5.PNG)


##### Example 6:

```python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy_charts.bar_chart import BarChart

class MainApp(MDApp):
    
    def build(self):

        main_layout = MDFloatLayout(md_bg_color='skyblue')

        box_layout = MDBoxLayout(
            size_hint=(None, None),
            size=(500, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color='white'
        )

        data = {'Jan': 300, 'Feb': 500, 'Mar': 250, 'Apr': 800, 'Mai': 400, 'Jun': 120, 'Jul': 450}
        
        chart = BarChart(
            data=data, 
            title="Monthly Sales ($)",
            colors = ['#C9190B', '#F4C145', '#8F4700', (1, 1, 0, 1), (1, 0, .5, 1), (0, 1, 1, 1), (.3, .3, .2, 1)],
            bar_radius=10,
            grid=True,
            grid_style='line',
            y_axis_labels=True,
            size_hint=(1, 1),
        )
        
        box_layout.add_widget(chart)
        main_layout.add_widget(box_layout)

        return main_layout

if __name__ == '__main__':
    MainApp().run()
```


##### Output:
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/bar_chart/example6.PNG)

---

### Pie Chart

The PieChart widget provides a customizable pie chart for visualizing data.

#### Features

- Configurable legend with customizable shapes and styles.
- Support for percentage labels on the pie chart.
- Options for customizing fonts, colors, and label positions.
- Interactive legend alignment (top, center, bottom) and positioning (left, right).
  
#### Usage

To use the PieChart widget in your Kivy app, simply add it to your layout and set the desired properties:

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_charts.pie_chart import PieChart

class MyChartApp(App):

    def build(self):
        layout = BoxLayout()
        data = {"Category A": 30, "Category B": 70, "Category C": 50}
        pie_chart = PieChart(data=data, colors=['#ff6347', '#4682b4', '#32cd32'])
        layout.add_widget(pie_chart)
        return layout

if __name__ == '__main__':
    MyChartApp().run()
```

#### PieChart Properties

Here are all the properties available for the PieChart widget, allowing for extensive customization:

##### `data`
- **Type:** `DictProperty`
- **Description:** Data for the chart. Keys represent the labels, and values represent the respective values to be converted into parcentages.
- **Default:** `{}`
- **Usage:** Set the data to be displayed in the pie chart.

##### `colors`
- **Type:** `ListProperty`
- **Description:** A list of colors for pie chart segments (Accept colors in RGBA and hex format).
- **Default:** Defaults to a predefined color palette.

##### `font_name`
- **Type:** `StringProperty`
- **Description:** Font name for percentage and legend labels.
- **Default:** `Roboto`

##### `percentage_color`
- **Type:** `ColorProperty`
- **Description:** Color of the percentage labels.
- **Default:** `(0, 0, 0, 1)`

##### `percentage_font_size`
- **Type:** `NumericProperty`
- **Description:** Font size for percentage labels.
- **Default:** `14`

##### `percentage_distance_factor`
- **Type:** `NumericProperty`
- **Description:** Determines how far percentage labels are placed from the chart center.
- **Default:** `0.5`

##### `legend_valign`
- **Type:** `OptionProperty`
- **Options:** `'top'`, `'bottom'`, `'center'`
- **Description:** Vertical alignment of the legend.
- **Default:** `'center'`

##### `legend_position`
- **Type:** `OptionProperty`
- **Options:** `'left'`, `'right'`
- **Description:** Position of the legend relative to the pie chart.
- **Default:** `'left'`

##### `legend_label_color`
- **Type:** `ColorProperty`
- **Description:** Color of the legend text labels.
- **Default:** `(0, 0, 0, 1)`

##### `legend_label_font_size`
- **Type:** `NumericProperty`
- **Description:** Font size for legend text labels.
- **Default:** `14`

##### `legend_key_shape`
- **Type:** `OptionProperty`
- **Options:** `'circle'`, `'square'`, `'diamond'`, `'hexagon'`, `'star'`
- **Description:** Shape of the legend keys.
- **Default:** `'circle'`

##### `legend_key_style`
- **Type:** `OptionProperty`
- **Options:** `'filled'`, `'outlined'`
- **Description:** Style of legend keys.
- **Default:** `'filled'`

#### Examples

##### Example 1:

```python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from pie_chart import PieChart

class MainApp(MDApp):

    def build(self):

        main_layout = MDFloatLayout(md_bg_color='skyblue')

        box_layout = MDBoxLayout(
            size_hint=(None, None),
            size=(600, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color='white'
        )

        chart_data = {'Category A': 30, 'Category B': 70, 'Category C': 50, 'Category D': 25, 'Category E': 40}

        pie_chart = PieChart(
            data=chart_data,
            size_hint=(1, 1)
        )

        box_layout.add_widget(pie_chart)
        main_layout.add_widget(box_layout)

        return main_layout

if __name__ == '__main__':
    MainApp().run()
```


##### Output
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/pie_chart/example1.PNG)


##### Example 2:

```python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from pie_chart import PieChart

class MainApp(MDApp):

    def build(self):

        main_layout = MDFloatLayout(md_bg_color='skyblue')

        box_layout = MDBoxLayout(
            size_hint=(None, None),
            size=(600, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color='white'
        )

        chart_data = {'Category A': 30, 'Category B': 70, 'Category C': 50, 'Category D': 25, 'Category E': 40}
        chart_colors= ['#f4a261', (38/255, 70/255, 83/255, 1), '#2a9d8f', '#e9c46a', '#e76f51']

        pie_chart = PieChart(
            data=chart_data,
            size_hint=(1, 1),
            colors=chart_colors,
            percentage_color='white',
            percentage_font_size=16,
            percentage_distance_factor=0.75,
            legend_key_shape='square',
            legend_valign='top'
        )

        box_layout.add_widget(pie_chart)
        main_layout.add_widget(box_layout)

        return main_layout

if __name__ == '__main__':
    MainApp().run()
```

##### Output
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/pie_chart/example2.PNG)

##### Example 3:

```python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from pie_chart import PieChart

class MainApp(MDApp):

    def build(self):

        main_layout = MDFloatLayout(md_bg_color='skyblue')

        box_layout = MDBoxLayout(
            size_hint=(None, None),
            size=(600, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color='white'
        )

        chart_data = {'Category A': 35, 'Category B': 30, 'Category C': 55, 'Category D': 25, 'Category E': 40}
        chart_colors= ['#59c3c3', '#247ba0','#fcbf49', '#f77f00', '#b5af8d']

        pie_chart = PieChart(
            data=chart_data,
            size_hint=(1, 1),
            colors=chart_colors,
            percentage_color='white',
            percentage_font_size=16,
            percentage_distance_factor=0.75,
            legend_position='right',
            legend_key_shape='star',
            legend_key_style='outlined',    
        )

        box_layout.add_widget(pie_chart)
        main_layout.add_widget(box_layout)

        return main_layout

if __name__ == '__main__':
    MainApp().run()
```

##### Output
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/pie_chart/example3.PNG)

---

### Donut Chart

The DonutChart widget provides a donut-shaped visualization of data. It is an extension of the PieChart widget.

#### Features

- Adds a central hole to the pie chart with a configurable radius and color.
- Dynamically positions percentage labels to avoid overlap with the hole.
- All features of the PieChart widget.
  
#### Usage

To use the DonutChart widget in your Kivy app, simply add it to your layout and set the desired properties:

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_charts.pie_chart import DonutChart

class MyChartApp(App):

    def build(self):
        layout = BoxLayout()
        data = {"Category A": 30, "Category B": 70, "Category C": 50}
        donut_chart = DonutChart(
            data=data,
            colors=['#ff6347', '#4682b4', '#32cd32']
        )
        layout.add_widget(donut_chart)
        return layout

if __name__ == '__main__':
    MyChartApp().run()
```

#### DonutChart Properties

##### All properties from the PieChart widget.

##### `donut_radius`
- **Type:** `NumericProperty`
- **Description:** Radius of the donut hole, relative to the chart radius.
- **Default:** `0.5`
- **Range:** `0.2` to `0.8`

##### `donut_hole_color`
- **Type:** `ColorProperty`
- **Description:** Color of the central donut hole.
- **Default:** `(1, 1, 1, 1)`

#### Examples

##### Example 1:

```python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from pie_chart import DonutChart

class MainApp(MDApp):

    def build(self):

        main_layout = MDFloatLayout(md_bg_color='skyblue')

        box_layout = MDBoxLayout(
            size_hint=(None, None),
            size=(600, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color='white'
        )

        chart_data = {'Category A': 35, 'Category B': 30, 'Category C': 55, 'Category D': 25, 'Category E': 40}
        chart_colors= ['#59c3c3', '#247ba0','#fcbf49', '#f77f00', '#b5af8d']

        pie_chart = DonutChart(
            data=chart_data,
            size_hint=(1, 1),
            colors=chart_colors,
            percentage_color='white',
            percentage_font_size=16,
            legend_key_shape='diamond',
        )

        box_layout.add_widget(pie_chart)
        main_layout.add_widget(box_layout)

        return main_layout

if __name__ == '__main__':
    MainApp().run()
```

##### Output
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/donut_chart/example1.PNG)


##### Example 2:

```python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from pie_chart import DonutChart

class MainApp(MDApp):
    
    def build(self):
        
        main_layout = MDFloatLayout(md_bg_color='skyblue')

        box_layout = MDBoxLayout(
            size_hint=(None, None),
            size=(600, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color='black'
        )

        chart_data = {'Category A': 35, 'Category B': 30, 'Category C': 55, 'Category D': 25, 'Category E': 40}
        chart_colors= ['#54f291', '#1ec6f7', '#3053ef', '#af4eff', '#eef0ef']

        pie_chart = DonutChart(
            data=chart_data,
            size_hint=(1, 1),
            colors=chart_colors,
            donut_hole_color='black',
            donut_radius=0.6,
            percentage_font_size=16,
            legend_position='right',
            legend_label_color='white',
            legend_label_font_size=16,
            legend_key_shape='star',
        )

        box_layout.add_widget(pie_chart)
        main_layout.add_widget(box_layout)

        return main_layout

if __name__ == '__main__':
    MainApp().run()
```

##### Output
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/donut_chart/example2.PNG)
 

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

© *OuchenTech 2024*
