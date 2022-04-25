# Statistical Analyzer Codebase

## Contents:
* GUI.py
* Analyzer.py
* visualize.py
* Data.py

### GUI.py
This file runs all the other files and interacts with the user. Basically the 'driver' for
the codebase.

### Analyzer.py
This is the mathematics library for our project. It has a driver to call a function given 
the function name and data, or each function can be called separately. The input for each 
operation is 'data', a numpy array of any given size. This driver function returns the results
of the given function to the caller.

### visualize.py
This is the file to hold all data display/saving functionality. 

### Data.py
The class to read in or take in data from numpy array or csv/tab-delimited file. It holds the
data as a numpy array, the data type as a string, and the column/row labels as arrays. 

## Dependencies:
* Python 3.x (3.6-3.9 is best)
* Numpy
* Scipy
* Matplotlib

## Environment Setup:

> git clone https://github.com/ian-mcnichols/CS_499
> 
> cd CS_499
> 
> conda create -f env.yml
> 
> conda activate 499
 
## Documentation:
We use Sphinx to auto-generate documentation from docstrings. To run this, make sure
you have Sphinx installed using pip install -U Sphinx or conda install -c anaconda sphinx.
Navigate inside the CS_499 folder where all the .py files are before running the following.

To generate .rst 
>  sphinx-apidoc -o ./documentation .

To generate html
> make html

Open in any html viewer.

## Running the program:

> python ./GUI.py

## Alternative: .exe script

Click and run GUI.exe file for the program to execute.
