# Statistical Analyzer Codebase

## Contents:
* driver.py
* Analyzer.py
* visualize.py
* Data.py

### driver.py
This file contains the main function to call the other files as needed. It takes user input and calls appropriate functions. This is also where the library that maps data types to applicable functions and charts.

### Analyzer.py
This is the mathematics 'library' for our project. It has a driver to call a function given the function name and data, or each function can be called separately. The input for each operation is 'data', a numpy array of any given size. Each operation should check that the shape is correct before running.

### visualize.py
This is the file to hold all data display/saving functionality. It should take in results and plot type, then use matplotlib to either display or save depending on the user's input. Mostly undeveloped.

### Data.py
The class to read in or take in data from numpy array or csv/tab-delimited file. It holds the data as a numpy array, and the data type as a string. In the future it should also have functionality to only access specific rows/columns, although right now that can be done by accessing the numpy array. 

## Dependencies:
* Python 3.x (3.6-3.9 is best)
* Numpy 1.21.x
* Scipy 1.7.x
* Matplotlib
- These can be installed using conda install or pip install. The internet should have specific install instructions.

## Operations: 
* mean
* median
* mode
* standard deviation
* variance
* coefficient of variance
* percentiles
* probability distribution
* binomial distribution
* least square line
* 2 (Chi Square)
* correlation coefficient
* sign test
* rank sum test
* Spearman rank correlation coefficient
