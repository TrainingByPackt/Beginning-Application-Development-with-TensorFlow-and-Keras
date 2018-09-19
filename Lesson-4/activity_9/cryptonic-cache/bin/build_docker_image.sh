#!/bin/bash
#
#  Builds Docker image for the
#  backend Redis cache used by Cryptonic.
#
VERSION=$1
docker build --tag cryptonic-cache:$VERSION \
             --tag cryptonic-cache:latest \
             ./cryptonic-cache/