#!/bin/bash

sudo docker run --name sso-api -d -p 5000:5000 sso-api

curl localhost:5000/api/users

