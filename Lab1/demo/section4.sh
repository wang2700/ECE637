#!/bin/bash

../bin/SharpeningFilter imgblur.tif 0.2
mv sharpen.tif output/sharpen_0_2.tif

../bin/SharpeningFilter imgblur.tif 0.8
mv sharpen.tif output/sharpen_0_8.tif

../bin/SharpeningFilter imgblur.tif 1.5
mv sharpen.tif output/sharpen_1_5.tif

# Run this matlab script to plot the data
# matlab PlotData.m

