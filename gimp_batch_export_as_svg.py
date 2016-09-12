#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jabiertxof <jabier.arraiza@marker.es>
# Copyright 2015 Jabiertxof
# License: GPL v3+
# Version 0.3.2
# GIMP batch plugin to export as SVG

from gimpfu import *
import os
from gimp_export_as_svg import *
from shutil import copyfile

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def batch_export_as_svg(origin, dest, only_visible=False, flatten=False, remove_offsets=False, crop=False, inkscape_layers=True, text_layers=True, resolution_96=True, block_images=False):
    #export_as_svg(img, path, only_visible, flatten, remove_offsets, crop, inkscape_layers, text_layers, resolution_96)
    allFileList = os.listdir(origin)
    for fname in allFileList:
        fnameLow = fname.lower()
        if os.path.splitext(fname)[1] == '.xcf':
            img = pdb.gimp_xcf_load(1, os.path.join(origin, fname), fname)
            export_as_svg(img, dest, only_visible, flatten, remove_offsets, crop, inkscape_layers, text_layers, resolution_96)
        if os.path.splitext(fname)[1] == '.jpg' or os.path.splitext(fname)[1] == '.jpeg' :
            img = pdb.file_jpeg_load(os.path.join(origin, fname), fname)
            image = pdb.gimp_image_get_uri(img)
            copyfile(os.path.join(origin, fname),os.path.join(dest, os.path.basename(image)))
            export_non_xcf_as_svg(img, dest, only_visible, flatten, remove_offsets, crop, inkscape_layers, text_layers, resolution_96)
        if os.path.splitext(fname)[1] == '.bmp':
            img = pdb.file_bmp_load(os.path.join(origin, fname), fname)
            image = pdb.gimp_image_get_uri(img)
            copyfile(os.path.join(origin, fname),os.path.join(dest, os.path.basename(image)))
            export_non_xcf_as_svg(img, dest, only_visible, flatten, remove_offsets, crop, inkscape_layers, text_layers, resolution_96)
        if os.path.splitext(fname)[1] == '.png':
            img = pdb.file_png_load(os.path.join(origin, fname), fname)
            image = pdb.gimp_image_get_uri(img)
            copyfile(os.path.join(origin, fname),os.path.join(dest, os.path.basename(image)))
            export_non_xcf_as_svg(img, dest, only_visible, flatten, remove_offsets, crop, inkscape_layers, text_layers, resolution_96)
        if os.path.splitext(fname)[1] == '.gif':
            img = pdb.file_gif_load(os.path.join(origin, fname), fname)
            image = pdb.gimp_image_get_uri(img)
            copyfile(os.path.join(origin, fname),os.path.join(dest, os.path.basename(image)))
            export_non_xcf_as_svg(img, dest, only_visible, flatten, remove_offsets, crop, inkscape_layers, text_layers, resolution_96)
        if os.path.splitext(fname)[1] == '.tif' or os.path.splitext(fname)[1] == '.tiff':
            img = pdb.file_tiff_load(os.path.join(origin, fname), fname)
            image = pdb.gimp_image_get_uri(img)
            copyfile(os.path.join(origin, fname),os.path.join(dest, os.path.basename(image)))
            export_non_xcf_as_svg(img, dest, only_visible, flatten, remove_offsets, crop, inkscape_layers, text_layers, resolution_96)
            
register(
    proc_name=("python-fu-batch-export-as-svg"),
    blurb=("Batch export as SVG"),
    help=("Export to svg's in batch."),
    author=("Jabiertxof <jabier.arraiza@marker.es>"),
    copyright=("Jabiertxof <jabier.arraiza@marker.es>"),
    date=("2016"),
    label=("Batch export as SVG"),
    imagetypes=("*"),
    params=[
        (PF_DIRNAME, "origin", "Images to process", os.getcwd()),
        (PF_DIRNAME, "dest", "Save here", os.getcwd()),
        (PF_BOOL, "only_visible", "Only Visible Layers?", False),
        (PF_BOOL, "flatten", "Flatten Images?", False),
        (PF_BOOL, "remove_offsets", "Remove Offsets?", False),
        (PF_BOOL, "crop", "Auto Crop", False),
        (PF_BOOL, "inkscape_layers", "Create Inkscape Layers?", True),
        (PF_BOOL, "text_layers", "Retain text layers as text?", True),
        (PF_BOOL, "resolution_96", "Use new SVG 96DPI resolution?", True),
        ],
    results=[],
    function=(batch_export_as_svg), 
    menu=("<Image>/File/Export/SVG/"), 
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
