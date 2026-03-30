#!/bin/bash

set -e

# the issue is not reproducible with GDAL_NUM_THREADS=1 and GTI_NUM_THREADS=1
docker run \
    --rm \
    -v $(pwd)/main.py:/scripts/main.py \
    -v $(pwd):/scratch \
    --workdir /scratch \
    --user $UID:$GID \
    -e GDAL_NUM_THREADS=ALL_CPUS \
    -e GTI_NUM_THREADS=ALL_CPUS \
    --name gdal-issue-gti-num-threads \
    --cpus=4 \
    --memory=4g \
    --memory-swap=4g \
    ghcr.io/osgeo/gdal:ubuntu-full-latest-amd64 \
    python /scripts/main.py
