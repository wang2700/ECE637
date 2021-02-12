#!/bin/bash

../bin/img_seg img22gd2.tif 1
mv output.tif section2/T1.tif

../bin/img_seg img22gd2.tif 2
mv output.tif section2/T2.tif

../bin/img_seg img22gd2.tif 3
mv output.tif section2/T3.tif

# Run this matlab script to plot the data
# matlab PlotData.m

