# Geometry Calculator

A Python library for calculating areas of geometric shapes with additional features.

## Features

- Calculate area of circle by radius
- Calculate area of triangle by three sides
- Check if triangle is right-angled
- Easy to extend with new shapes
- Polymorphic area calculation

## Installation

```bash
pip install geometry-calculator
```

## Usage

```python
from geometry_calculator import Circle, Triangle, calculate_area, is_right_angled

# Circle example
circle = Circle(5)
print(calculate_area(circle))  # 78.53981633974483

# Triangle example
triangle = Triangle(3, 4, 5)
print(calculate_area(triangle))  # 6.0
print(is_right_angled(triangle))  # True
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)