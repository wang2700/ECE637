#!/bin/bash

../bin/area_fill img22gd2.tif 67 45 1 1
mv output.tif T1.tif

../bin/area_fill img22gd2.tif 67 45 2 1
mv output.tif T2.tif

../bin/area_fill img22gd2.tif 67 45 3 1
mv output.tif T3.tif

# ../bin/SurrogateFunctionExample > output/data.txt

# Run this matlab script to plot the data
# matlab PlotData.m

