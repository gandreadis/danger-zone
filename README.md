# danger-zone

## Installation
Make sure to have Python 3 (and PIP) installed. Once those are ready, run the following command from a terminal in this directory.

```commandline
pip install -r requirements.txt
```

**Windows-Users:** The 'Shapely' dependency will need to be installed separately. A possibility is using the .whl files from [this repository](https://www.lfd.uci.edu/~gohlke/pythonlibs#shapely) (install through `pip install <whl-file-name>`).

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
