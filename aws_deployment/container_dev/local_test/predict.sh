#!/bin/bash

image_payload=$1

curl -i -X POST \
-H "Content-Type: application/x-image" \
-F "image=@${image_payload}" \
https://osbh7tvzj3.execute-api.us-east-2.amazonaws.com/beta/classifydogbreed
