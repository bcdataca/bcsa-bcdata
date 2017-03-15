# BCData Colloquium Data Component 1

## BCSA Data

### Introduction

The data accessible via this interface was kindly provided by the BC Safety
Authority in association with their lecture in the [BC Data Colloquium](//bcdata.ca). 

The interface used to access this data is coded in Python using a
[Jupyter](http://jupyter.org/) Notebook available through
<https://ubc.syzygy.ca/> and <https://sfu.syzygy.ca>. For a fast and thorough
introduction to using Jupyter notebooks, check out
[this description](https://github.com/barbagroup/jupyter-tutorial/blob/master/World-of-Jupyter.md)
and in particular the associated mini-tutorials:

1. [The Notebook](http://nbviewer.jupyter.org/github/barbagroup/jupyter-tutorial/blob/master/1--The%20Notebook.ipynb)
2. [The Python World of Science and Data](http://nbviewer.jupyter.org/github/barbagroup/jupyter-tutorial/blob/master/2--The%20Python%20world%20of%20science%20and%20data.ipynb)
3. [Jupyter like a pro](http://nbviewer.jupyter.org/github/barbagroup/jupyter-tutorial/blob/master/3--Jupyter%20like%20a%20pro.ipynb)

Or, alternatively, reference the
[Jupyter documentation](http://jupyter-notebook.readthedocs.io/en/latest/).

Note that while the code used to access the data is written in Python, it is
not necessary to explore the data using Python. Because Jupyter notebooks allow
the user to load different kernels, once the data is downloaded onto a user's
syzygy account, it is possible to load the data into a Jupyter notebook running
Python, R or Julia. 


### Accessing the data

1. Log in to <https://ubc.syzygy.ca> or <https://sfu.syzygy.ca> (respectively)
using your CWL.
2. Press the "Start My Server" button.
3. Open a new Terminal by clicking `New` > `Terminal`.
4. In the terminal, navigate to a directory of your choice, then input

		git clone https://github.com/bcdataca/bcsa-bcdata.git
		cd bcsa-bcdata

5. Close the terminal window and in the main Jupyter window, navigate to the
directory above.
6. Once inside the `bcsa-bcdata` directory, click to open `Pull and Import BCSA
Data.ipynb`.
7. Run the first cell by pressing `Shift` + `Enter`. 
8. **Note:** if this script requires the pacakges `boto3` and `botocore`. If
   these packages were not previously installed and have been installed by the
   first cell, then the notebook **must be restarted** once the first cell has
   **finished** executing. To restart the notebook:
   1. Close the window
   2. Click the checkbox next to the `Pull and Import...` file.
   3. Click the `Shutdown` button above it
   4. Re-open the file.

9. Click on the `Kernel` menu item and click `Run All`.
10. Verify that the download was successful by checking:
	1. there are no error messages in the notebook
	2. the last cell contains the output

			{'2015': (6305, 34), '2016': (8172, 34)}
			{'incident': (6390, 143)}

The files, by default, are stored in the directory `bcsa-data/tmp/`. To change
this behaviour, 
   

### Conditions for Use

The following is a disclaimer on the use of the data.

This information was provided expressly to those in attendance at the BC Data colloquium. This information is confidential and may not be disclosed without the prior written consent of BC Safety Authority.

## Issues

* As of 13 March at 15:23 there still exists a permissions issue to be resolved.
* As of 13 March at 16:46 this issue was resolved.
