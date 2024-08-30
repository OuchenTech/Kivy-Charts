# Kivy Charts

Kivy Charts is a customizable chart library for Kivy applications. This library allows developers to easily integrate charts into their Kivy apps, with support for various customization options to tailor the charts to specific needs. Currently, the library includes a Bar Chart widget, with more chart types to be added in the future.

## Table of Contents
- [Installation](#installation)
- [Requirements](#requirements)
- [Charts](#charts)
  - [Bar Chart](#bar-chart)
    - [Features](#features)
    - [Usage](#usage)
    - [BarChart Properties](#barchart-properties)
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
```

## Requirements

- Python 3.7+
- Kivy = 2.3.0
- Kivymd = 2.0.1.dev0
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

- `data`:
  - Type: DictProperty
  - Description: A dictionary containing the labels and their corresponding values.
  - Default: {}
  - Usage: Set the data to be displayed in the bar chart.

- `chart_mode`:
  - Type: OptionProperty
  - Options: 'standard', 'interactive'
  - Description: Mode of the chart; in 'interactive' mode, values are displayed on touch.
  - Default: 'standard'
  - Usage: Use 'interactive' to show values on touch; otherwise, use 'standard'.

- `color_style`:
  - Type: OptionProperty
  - Options: 'standard', 'gradient'
  - Description: Color style of the bars. If set to 'gradient', bars will use gradient colors defined in gradient_colors.
  - Default: 'standard'

- `colors`:
  - Type: ListProperty
  - Description: A list of colors for the bars (Accept colors in RGBA and hex format). Only applicable when color_style is set to 'standard'.
  - Default: None

- `bar_default_color`:
  - Type: ColorProperty
  - Description: Default color for bars if colors are not provided. Applies when color_style is set to 'standard'.
  - Default: '#3498db'

- `gradient_colors`:
  - Type: ListProperty
  - Description: Colors used for gradient bars. This property is only used when color_style is set to 'gradient'.
  - Default: ['#33ff66', '#C3FF66']

- `bar_radius`:
  - Type: NumericProperty
  - Description: Radius of the bar corners.
  - Default: 0
  - Usage: Set this property to give rounded corners to the bars.

- `label_font_name`:
  - Type: StringProperty
  - Description: Font name used for the labels.
  - Default: 'Roboto'

- `label_size`:
  - Type: NumericProperty
  - Description: Font size for the labels.
  - Default: 14

- `label_color`:
  - Type: ColorProperty
  - Description: Color of the labels.
  - Default: (0, 0, 0, 1)

- `x_axis_label_rotation`:
  - Type: OptionProperty
  - Options: 'no-rotation', 'left-up', 'left-down'
  - Description: Rotation angle for x-axis labels.
  - Default: 'no-rotation'

- `y_axis_labels`:
  - Type: BooleanProperty
  - Description: Whether to show y-axis labels.
  - Default: False

- `grid`:
  - Type: BooleanProperty
  - Description: Whether to show grid lines.
  - Default: False

- `grid_style`:
  - Type: OptionProperty
  - Options: 'line', 'dashed', 'dotted'
  - Description: Style of the grid lines. Only applies when grid is True.
  - Default: 'line'

- `grid_color`:
  - Type: ColorProperty
  - Description: Color of the grid lines. Only applies when grid is True.
  - Default: [0.5, 0.5, 0.5, 0.5]

- `title`:
  - Type: StringProperty
  - Description: Title of the chart.
  - Default: ""
  - Usage: Set this property to display a title at the top of the chart.

#### Examples

Example 1:

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

Output:
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/example1.PNG)


Example 2:

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

Output:
![](https://github.com/OuchenTech/Kivy-Charts/blob/main/screenshots/example1.PNG)


Example 3:

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


Example 4:

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



Example 5:

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


Example 6:

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

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
