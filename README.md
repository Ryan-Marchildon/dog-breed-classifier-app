# dog-breed-classifier-app
Building a simple dog breed classification app for Android with deployment on Amazon SageMaker. 

Special thanks to Kirill Panarin for providing this helpful [tutorial](https://towardsdatascience.com/dog-breed-classification-hands-on-approach-b5e4f88c333e) and [repository](https://github.com/stormy-ua/dog-breeds-classification) which were used during model creation. 


**Usage**: *(still under development)*

1. From the repo root directory, run `./setup/setup.sh` in your linux terminal. This defines the data and model directories, and downloads/extracts: (a) the Stanford dog breed dataset; (b) Google's Inception model as a frozen TensorFlow graph that we can use for transfer learning. 
