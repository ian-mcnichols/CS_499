# Statistical Analyzer Codebase

## Contents:
* GUI.py
* Analyzer.py
* visualize.py
* Data.py

### GUI.py
This file runs all the other files and interacts with the user.

### Analyzer.py
This is the mathematics 'library' for our project. It has a driver to call a function given 
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
 
## Running the script:

> python ./GUI.py

## Alternative: .exe script

Click and run GUI.exe file for the program to execute.
