# gdal-issue-gti-num-threads

This repository contains code to reproduce issues generating large GTIff image from a single GTI mosaic.

# main.py

Contains code to 
- generate 1000 2000x2000 uint8 GTiff images, in both EPSG:26910 and EPSG:26911 to be used as source files for GTI mosaic
- generate mosaic GTI in EPSG:3857
- generate GTiff from GTI with `SPARSE_OK=TRUE` and `BIGTIFF=YES`


# run.sh

Serves as an entrypoint to run `main.py` using the `ghcr.io/osgeo/gdal:ubuntu-full-latest-amd64` image.
