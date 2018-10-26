#!/bin/bash

# call on permitted .jpg images
echo -e "\nYorkie JPG Image 1:"
./predict.sh ./test_imgs/yorkie_1.jpg

echo -e "\nYorkie JPG Image 2:"
./predict.sh ./test_imgs/yorkie_2.jpg

echo -e "\nPoodle JPG Image 1:"
./predict.sh ./test_imgs/poodle_1.jpg

echo -e "\nGerman Shepherd JPG Image 1:"
./predict.sh ./test_imgs/german_shep_1.jpg

# call on non-permitted image type (.png)
echo -e "\nGerman Shepherd PNG Image 1:"
./predict.sh ./test_imgs/german_shep_1.png

# call without an image
echo -e "\nCalling classifier without an image:"
./predict.sh

