# dog-breed-classifier-app
Building a simple dog breed classification app for Android with deployment on Amazon SageMaker. 

(Note: still under development)

### 1) Model

**Description**:

The dog breed classification model follows the implementation by [Kirill Panarin](https://www.linkedin.com/in/panarin/) described [here](https://towardsdatascience.com/dog-breed-classification-hands-on-approach-b5e4f88c333e). This approach uses transfer learning, with a frozen pretrained Inception model forming the base layers, upon which we add a "head" comprised of dense layers that we train to specialize in our specific classification task using the [Stanford Dogs Dataset](http://vision.stanford.edu/aditya86/ImageNetDogs/). 

Model source files are found within the `/model` directory. The model was built using scripts adopted from [this repository](https://github.com/stormy-ua/dog-breeds-classification) with some minor modifications. You can build your own variation of this model by following the instructions in the repo's README. The trained model is frozen and exported as a `.pb` file extension. In our case, the model is saved as `dbc_stanford_10_23.pb`. Accuracy on the training and testing datasets was roughly 98%. 

**Testing/Usage**:

To perform inference on a raw JPG image, use `classify.py` via the terminal command `python -m classify file <JPG Image Path>` while within the `/model` directory (run the bash file `test.sh`for an example). The `classify.py` script unfreezes our model (from the `.pb` file extension) into a TensorFlow graph and starts a TensorFlow session to perform the inference. Preprocessing of the raw image is already included within the model definition.


### 2) Containerized Web App

Uses the [nginx](https://www.nginx.com/) --> [gunicorn](https://gunicorn.org/) --> [Flask](http://flask.pocoo.org/) Python stack. For a guide outlining a similar approach, see [this AWS SageMaker example](https://github.com/awslabs/amazon-sagemaker-examples/blob/master/advanced_functionality/scikit_bring_your_own/scikit_bring_your_own.ipynb).

**Relevant Directories**: 
* `/flask_dev`: Contains development files for deploying and testing the classifier locally via Flask (without the added complexity of nginx, gunicorn, or Docker). You can run the app via the terminal command `$ python predictor.py`. The shell scripts `ping.sh`, `predict.sh`, and `run_tests.sh` can be used for testing and debugging. The subdirectory `/test_dir` contains the frozen model, list of classes (breeds.csv), and two ipython notebooks that were used to test a consolidated implementation (all-in-one-file) of the classifier. 

* `/container`: Holds all the files necessary for building and testing a Docker image of the web app using the nginx-->gunicorn-->Flask stack. To build the container locally, run `build_local.sh` from this directory (first ensure you have set up Docker to [run without sudo privileges](https://docs.docker.com/install/linux/linux-postinstall/)). The script `build_and_push.sh` will be used later when deploying the container via AWS SageMaker. Within `/local_test`, run `serve_local.sh` to locally host the container, and use `run_tests.sh` and `predict.sh` for testing and debugging. Executing the terminal command `$ ./predict.sh <JPG Image Path>` from this directory will send an image to the locally-hosted container and retrieve the inferred dog breed. The inferences are returned as a .csv, showing the top 5 most probable breeds and their associated probabilities. The subdirectory `/test_dir` contains the files needed for model and one-hot-decoder construction. 

**Sample Output**:
After executing `run_tests.sh` from terminal for a locally-hosted docker container with the included test images:

![sample output](https://raw.githubusercontent.com/Ryan-Marchildon/dog-breed-classifier-app/master/container/local_test/run_tests-output.png)
