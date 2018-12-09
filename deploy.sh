#!/bin/bash

if [ -x "$(command -v docker)" ]; then
	echo "docker detected"
	sudo docker build -t flask-sample-one:latest .
	sudo docker run -d -p 8080:8080 flask-sample-one
else
    echo "please install docker first"
fi
