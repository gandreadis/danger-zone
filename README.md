# danger-zone

## Installation
Make sure to have Python 3 (and PIP) installed. Once those are ready, run the following command from a terminal in this directory.

```commandline
pip install -r requirements.txt
```

## Usage
Run the following command to get a list of all possible commands:

```commandline
python main.py -h
```

## Building the Report
The report is written in LaTeX, so you'll need to have a standard LaTeX distribution installed on your system. We recommend [TeX Live](https://www.tug.org/texlive/acquire-netinstall.html). Once you have this set up, run the following command from within the `report` directory:

```commandline
pdflatex main.tex
```

The compiled PDF will be placed in that same `report` folder, with the name `main.pdf`.

## Map Format Specification
`danger-zone` uses a text-based map definition system. A mapping from characters to tiles is presented below:

```text
# Danger Zones
^ - Car tile, moving North
> - Car tile, moving East
v - Car tile, moving South
< - Car tile, moving West
o - Pedestrian tile
w - Neutral (crosswalk) tile, moving North
d - Neutral (crosswalk) tile, moving East
s - Neutral (crosswalk) tile, moving South
a - Neutral (crosswalk) tile, moving West

# Spawn and Target Areas
i - Car spawn / target tile, moving North
l - Car spawn / target tile, moving East
k - Car spawn / target tile, moving South
j - Car spawn / target tile, moving West
p - Pedestrian spawn / target tile

# Objects
| - Car
x - Pedestrian
```
