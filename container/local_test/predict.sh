#!/bin/bash

image_payload=$1

curl -F "image=@${image_payload}" http://localhost:8080/invocations
