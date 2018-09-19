#!/bin/bash
#
#  Builds Docker image of the
#  `Cryptonic` program.
#
VERSION=$1
docker build --tag cryptonic:$VERSION \
             --tag cryptonic:latest \
             .