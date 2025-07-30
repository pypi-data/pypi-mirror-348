
# ROX Vectors

A lightweight and simple 2D vector class for Python, providing essential vector operations, geometric transformations, and utility functions. Perfect for mathematical simulations and robotics.

## Features

- Basic Vector Operations: Addition, subtraction, multiplication, division, negation.
- Geometric Properties: Vector length, angle, normalization, and perpendicular vectors.
- Transformation Utilities: Translation and rotation.
- Dot and Cross Product calculations.
- Line Segment manipulation and properties.

## Installation

```sh
pip install rox-vectors
```

## Usage Examples

### Creating Vectors

```python
from rox_vectors import Vector

v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(v1)  # (3.000, 4.000)
print(v2)  # (1.000, 2.000)
```

### Basic Operations

```python
v3 = v1 + v2  # (4.000, 6.000)
v4 = v1 - v2  # (2.000, 2.000)
v5 = v1 * 2   # (6.000, 8.000)
v6 = v1 / 2   # (1.500, 2.000)
v7 = -v1      # (-3.000, -4.000)
```

### Geometric Properties

```python
length = v1.r        # 5.0
angle = v1.phi       # 0.927 (in radians)
v8 = v1.u            # (0.600, 0.800)
v9 = v1.v            # (-0.800, 0.600)
```

### Dot and Cross Products

```python
dot_product = v1.dot(v2)       # 11.0
cross_product = v1.cross(v2)   # 2.0
```

### Vector Transformation

```python
v10 = v1.translate(2, 3)       # (5.000, 7.000)
v11 = v1.rotate(math.radians(90))  # (-4.000, 3.000)
```

### Line Segment

```python
from rox_vectors import Line

line = Line(Vector(0, 0), Vector(1, 1))
line.shift_y(1)
print(line)  # <Line(start=(0.000,1.000), end=(1.000,2.000))>
line_angle = line.phi  # 0.785 (in radians)
```

### Distance and Projection Utilities

```python
from rox_vectors import point_on_line, distance_to_line, distance_to_b

a = Vector(0, 0)
b = Vector(4, 4)
x = Vector(2, 3)

projection = point_on_line(a, b, x)  # (2.500, 2.500)
distance = distance_to_line(a, b, x) # 0.707
distance_b = distance_to_b(a, b, x)  # -0.707
```


## Development

1. Init host system with `init_host.sh`. This will build a dev image.
2. Launch in VSCode devcontainer.


1. develop and test in devcontainer (VSCode)
2. trigger ci builds by bumping version with a tag. (see `.gitlab-ci.yml`)

## Tooling

* Automation: `invoke` - run `invoke -l` to list available commands. (uses `tasks.py`)
* Verisoning : `bump2version`
* Linting and formatting : `ruff`
* Typechecking: `mypy`

## What goes where
* `src/rox_vectors` app code. `pip install .` .
* `tasks.py` automation tasks.
* `.gitlab-ci.yml` takes care of the building steps.
