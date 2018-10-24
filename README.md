# dog-breed-classifier-app
Building a simple dog breed classification app for Android with deployment on Amazon SageMaker. 

### Model

**Description**:

The dog breed classification model follows the implementation by [Kirill Panarin](https://www.linkedin.com/in/panarin/) described [here](https://towardsdatascience.com/dog-breed-classification-hands-on-approach-b5e4f88c333e). This approach uses transfer learning, with a frozen pretrained Inception model forming the base layers, upon which we add a "head" comprised of dense layers that we train to specialize in our specific classification task using the [Stanford Dogs Dataset](http://vision.stanford.edu/aditya86/ImageNetDogs/). 

Model source files are found within the `/model` directory. The model was built using scripts adopted from [this repository](https://github.com/stormy-ua/dog-breeds-classification) with some minor modifications. You can build your own variation of this model by following the instructions in the repo's README. The trained model is frozen and exported as a `.pb` file extension. In our case, the model is saved as `dbc_stanford_10_23.pb`. Accuracy on the training and testing datasets was roughly 98%. 

**Testing/Usage**:

To perform inference on a raw JPG image, use `classify.py` via the terminal command `python -m classify file <JPG Image Path>` while within the `/model` directory (run the bash file `test.sh`for an example). The `classify.py` script unfreezes our model (from the `.pb` file extension) into a TensorFlow graph and starts a TensorFlow session to perform the inference. Preprocessing of the raw image is already included within the model definition.

Special thanks to Kirill Panarin for providing this helpful [tutorial](https://towardsdatascience.com/dog-breed-classification-hands-on-approach-b5e4f88c333e) and [repository](https://github.com/stormy-ua/dog-breeds-classification) which were used during model creation. 


**Usage**: *(still under development)*

1. From the repo root directory, run `./setup/setup.sh` in your linux terminal. This defines the data and model directories, and downloads/extracts: (a) the Stanford dog breed dataset; (b) Google's Inception model as a frozen TensorFlow graph that we can use for transfer learning. 
