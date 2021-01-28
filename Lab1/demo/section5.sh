#!/bin/bash

../bin/IIR_Filter img03.tif h_out.tif
mv iir_filter.tif output

# Run this matlab script to plot the data
# matlab PlotData.m

