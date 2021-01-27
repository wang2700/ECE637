#!/bin/bash

../bin/LowPassFilter img03.tif
mv lowpass_filter.tif output

# Run this matlab script to plot the data
# matlab PlotData.m

