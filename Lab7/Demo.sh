#!/bin/bash

./bin/weightedMedian ./input/img14bl.tif
mv output.tif output/bl_output.tif

./bin/weightedMedian ./input/img14gn.tif
mv output.tif output/gn_output.tif

./bin/weightedMedian ./input/img14sp.tif
mv output.tif output/sp_output.tif


