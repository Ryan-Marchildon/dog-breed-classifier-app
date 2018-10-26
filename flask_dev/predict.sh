#!/bin/bash

image_payload=$1

curl -F "image=@${image_payload}" http://127.0.0.1:5000/invocations
