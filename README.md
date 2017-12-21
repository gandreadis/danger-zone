# danger-zone

## Installation
Make sure to have Python 3 (and PIP) installed. Once those are ready, run the following command from a terminal in this directory.

```commandline
pip install -r requirements.txt
```

## Usage

### Simulation
Run the following command to get a list of all possible commands for the simulation tool:

```commandline
python main.py -h
```

### Playback
Run the following command to get a list of all possible commands for the playback tool:

```commandline
python visualizer.py -h
```

## Building the Report
The report is written in LaTeX, so you'll need to have a standard LaTeX distribution installed on your system. We recommend [TeX Live](https://www.tug.org/texlive/acquire-netinstall.html). Once you have this set up, run the following command from within the `report` directory:

```commandline
pdflatex main.tex
```

The compiled PDF will be placed in that same `report` folder, with the name `main.pdf`.

## Map Format Specification
`danger-zone` uses a text-based map definition system. A mapping from characters to tiles can be found in `danger_zone/map/tile_types.py`.