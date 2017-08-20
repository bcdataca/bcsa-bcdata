# BCSA Data

## Introduction

The data accessible via this interface was kindly provided by the BC Safety
Authority, under the conditions of the disclaimer below, in association with
their lecture in the [BC Data Colloquium](http://bcdata.ca).

### Jupyter and Syzygy

The interface used to access this data is coded in Python using a
[Jupyter](http://jupyter.org/) Notebook available through
<https://ubc.syzygy.ca/> and <https://sfu.syzygy.ca>. To learn more about
Jupyter notebooks, check out the
[Jupyter documentation](http://jupyter-notebook.readthedocs.io/en/latest/); for
an introduction to Jupyter notebooks and Python for data science, see
[this description](https://github.com/barbagroup/jupyter-tutorial/blob/master/World-of-Jupyter.md)
and the associated mini-tutorials:

1. [The Notebook](http://nbviewer.jupyter.org/github/barbagroup/jupyter-tutorial/blob/master/1--The%20Notebook.ipynb)
2. [The Python World of Science and Data](http://nbviewer.jupyter.org/github/barbagroup/jupyter-tutorial/blob/master/2--The%20Python%20world%20of%20science%20and%20data.ipynb)
3. [Jupyter like a pro](http://nbviewer.jupyter.org/github/barbagroup/jupyter-tutorial/blob/master/3--Jupyter%20like%20a%20pro.ipynb)

While Python encodes the download script, it is not the only option for
exploring the data &mdash; Jupyter notebooks allow the user to load different
kernels. Once the data is downloaded to a user's Syzygy account, it is possible
to load the data into a Jupyter notebook running Python, R or Julia. See the
above tutorials for instructions on switching kernels.

### Python

There are many resources for learning Python available freely online. For a
tutorial on using Python, see for example [[1]], [[2]] or [[3]]. To brush up on
rusty coding habits, check out projects like
[Project Euclid](https://projecteuclid.org/) or
[Advent of Code](https://adventofcode.com/).

[1]: https://engineering.ucsb.edu/~shell/che210d/numpy.pdf
[2]: https://www.youtube.com/playlist?list=PLYx7XA2nY5Gf37zYZMw6OqGFRPjB1jCy6
[3]: https://www.codecademy.com/learn/python


## Accessing the data

1. Log in to <https://ubc.syzygy.ca> or <https://sfu.syzygy.ca> (respectively)
using your CWL.
2. Press the "Start My Server" button.
3. Open a new Terminal by clicking `New` > `Terminal`.
4. In the terminal, navigate to a directory of your choice, then input

		git clone https://github.com/bcdataca/bcsa-bcdata.git
		cd bcsa-bcdata
		pip install --user --upgrade boto3 botocore

5. Close the terminal window and in the main Jupyter window, navigate to the
directory above.
6. Once inside the `bcsa-bcdata` directory, click to open `Pull and Import BCSA
Data.ipynb`.
7. Click on the `Kernel` menu item and click `Run All`.
8. Verify that the download was successful by checking:
   1. there are no error messages in the notebook
   2. the last cell contains the output

			{'2015': (6305, 34), '2016': (8172, 34)}
			{'incident': (6390, 143)}

### Options

The files, by default, are stored in the directory `bcsa-data/tmp/`. To change
this behaviour, you can change the value of the `target` variable to a
different directory. 

## BC Data Workshop: Project Information

To get familiar with accessing data using `boto3`, play around with the data and notebooks accessible via the above instructions. To access the data and reference material for the image classification project, please refer to the documents inside the [workshop-info](./workshop-info/) folder. 

## Conditions for Use

The following is a disclaimer on the use of the data.

This information was provided expressly to those in attendance at the BC Data colloquium. This information is confidential and may not be disclosed without the prior written consent of BC Safety Authority.
