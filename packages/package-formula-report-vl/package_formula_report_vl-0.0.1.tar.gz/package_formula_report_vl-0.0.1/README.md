# Formula 1 Report Package

This is a simple Python package for processing log files and generating Formula 1 racing reports.

## Installation

To install the package locally from the project root, run the following command in your terminal: 

```bash
pip install .
```

Alternative installation option:

```bash
pip install package-formula-report-vl
```
## Usage

After installation, you can use the package as follows:
```
from report.formula_report import build_report, print_report

report = build_report(folder_path='report/data', order='asc')
print_report(report)
    
```
## CLI Usage
 
After installing the package, you can use the command-line interface:

```
python -m report --path <folder_path>

```