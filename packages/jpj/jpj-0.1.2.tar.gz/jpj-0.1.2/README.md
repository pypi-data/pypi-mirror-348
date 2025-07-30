# Led Zeppelin's John Paul Jones' symbol

Draws Led Zeppelin's John Paul Jones' symbol ([more info](#more-info)).

![John Paul Jones' symbol](doc/media/jpj_symbol.svg "Black")

## Install

### `pypi`

The package can be installed via `pypi`:

```bash
pip install jpj
```

### Build locally

If you do any modifications, you can build the package locally:

```bash
python3 -m build
pip install dist/jpj-0.1.0-py3-none-any.whl
```

## Usage

```python
jpj
```

plots the symbol as shown above.

### Rapidly save figure

To save the figure hiding the plot window, run

```python
jpj -n -o
```

### Customization

The script can be customized.
Please run

```python
jpj -h
```

for additional information, or refer to the following sections.

#### Colored version

A colored version is available with:

```python
jpj -c
```

#### Drawing

To see support structures for drawing, run:

```python
jpj -c -s -p
```

#### Custom dimensions

To set custom radius or angle, run:

```python
jpj -a 10 -r 2
```

**Note:** Setting an angle different than the default (15 degrees) might mess up the symbol.

## More info

[John Paul Jones](https://en.wikipedia.org/wiki/John_Paul_Jones_(musician)) played as bassist for the famous hard rock band [Led Zeppelin](https://en.wikipedia.org/wiki/Led_Zeppelin).
In 1971, the members signed their [untitled fourth album](https://en.wikipedia.org/wiki/Led_Zeppelin_IV) (containing, among the other, their masterpiece [Stairway to Heaven](https://en.wikipedia.org/wiki/Stairway_to_Heaven)) with [four symbols](https://ledzeppelin.fandom.com/wiki/Four_Symbols) instead of the band name.
A simplified version of John Paul Jones' is drawn with this repository: the symbol represents the Holy Trinity by Christians.
