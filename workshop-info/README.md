# BC Data Science Workshop

## Project 2 Details: BC Safety Authority

### Background summary

The [Safety Authority](https://www.safetyauthority.ca/) is responsible
for all of the inspection and permitting in British Columbia &mdash;
whether it be elevators, chairlifts, boilers or home renos. Large
amounts of data are collected for inspection and inicdent alike. This
data elucidates the state of building and maintenance practices, as
well as accident prevention practices. Unfortunately, this data is
time consuming to process, and no clear method exists for using this
data to predict optimal inspection strategies for harm and incident
mitigation.

Inspection sites can be rated as complaint and
non-compliant. Presently, compliance categorizations are determined by
field employees with expertise in safety and inspection codes. These
employees document on-site materials with photographs and reports,
which include an overall hazard rating (on a scale of 1 through 5).

It would improve both efficacy and efficiency of the inspection
process to automate the compliance classification. A method to achieve
this includes classifying compliance of on-site inspection and
incident images by predicting their hazard rating. A second
possibility is the automated determination of hazardous objects in
inspection and incident images.

While state of the art methods for image classification exist,
classifying high-level salient concepts from raw image data is still a
highly non-trivial task.

### Technical Information and Resources

In this project, you will capitalize on the skills you developed in
the first week &mdash; as well as your resourcefulness as graduate
students &mdash; to rapdily prototype a magnificent duct tape
structure capable of state-of-the-art image classification.

Available to you are the following resources:

1. An AWS S3 bucket of approximately 10 000 training images. Aaron will show you how to access this material using `boto3` via [`s3Download.py`](../s3Download.py). 
2. A publicly available implementation of a state of the art [neural network for image classification](https://github.com/fastai/courses/blob/master/deeplearning1/nbs/vgg16.py).
3. Publicly [available material](https://kratzert.github.io/2017/02/24/finetuning-alexnet-with-tensorflow.html) that could be useful in modifying the above network to take advantage of *transfer learning*.
4. The above material is implemented in `keras` and `tensorflow`. [Associated methods](https://keras.io/preprocessing/image/) could, perhaps, be chained together (or modified) with `boto3` to help with preprocessing/training.
5. There's a [plethora](ftp://ftp.cs.wisc.edu/machine-learning/shavlik-group/torrey.handbook09.pdf) of [information](https://medium.com/towards-data-science/transfer-learning-using-keras-d804b2e04ef8) on [transfer learning](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-016-0043-6). This includes the [tensorflow blog](https://www.tensorflow.org/tutorials/image_retraining) and [other online blogs](https://www.analyticsvidhya.com/blog/2017/06/transfer-learning-the-art-of-fine-tuning-a-pre-trained-model/). 


Optionally available:

1. Methods for Active Learning with Bayesian CNNs are [available on GitHub](https://github.com/Riashat/Active-Learning-Bayesian-Convolutional-Neural-Networks); [posters](https://riashatislam.files.wordpress.com/2017/07/2017-icml-deep_active_learning-poster.pdf) and [publications](http://bayesiandeeplearning.org/papers/BDL_35.pdf) are available.
2. If your computational power isn't cutting it, let me know and we can see about other options. 
