#!/usr/bin/env python
# -*- coding: <utf-8> -*-
# Author: Erdem Guven <zuencap@yahoo.com>
# Copyright 2010 Erdem Guven
# Copyright 2009 Chris Mohler
# Copyright 2015 Jabiertxof
# "Only Visible" and filename formatting introduced by mh
# "Groups" "Crop layer" introduced by Jabiertxof
# "Flattern" "Offset" introduced by Jabiertxof from http://registry.gimp.org/node/18440 V0.6
# License: GPL v3+
# Version 0.2
# GIMP plugin to export as SVG

from gimpfu import *
import os, re

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

counter = 0;

def format_filename(img, layer):
    imgname = img.name.decode('utf-8')
    layername = layer.name.decode('utf-8')
    regex = re.compile("[^-\w]", re.UNICODE) 
    filename = regex.sub('_', imgname) + '-' + regex.sub('_', layername) + '.png'
    return filename

def get_image_name(img):
    imgname = img.name.decode('utf-8')
    regex = re.compile("[^-\w]", re.UNICODE) 
    return regex.sub('_', imgname)

def get_layers(layers, only_visible):
    result = []
    for layer in layers:
        if not pdb.gimp_item_get_parent(layer):
            result.append(layer)
    return result

def layer_process(layers, only_visible, dupe, path, flatten=False, remove_offsets=False, crop=False, inkscape_layers=True):
    images = ""
    for layer in layers:
        if only_visible:
            if not layer.visible:
                continue
        image = ""
        pdb.gimp_image_set_active_layer(dupe, layer)
        filename = format_filename(dupe, layer)
        fullpath = os.path.join(path, filename);
        tmp = False
        if not pdb.gimp_item_is_group(layer):
            is_visible = layer.visible
            layer.visible = 1
            tmp = pdb.gimp_image_new(pdb.gimp_image_width(dupe), pdb.gimp_image_height(dupe), pdb.gimp_image_base_type(dupe))
            pdb.gimp_image_insert_layer(tmp, pdb.gimp_layer_new_from_drawable(pdb.gimp_image_get_active_drawable(dupe), tmp), None, 0)
            if (flatten):
                    tmp.flatten()
            if (crop):
                pdb.plug_in_autocrop_layer(tmp, tmp.layers[0])
            if (remove_offsets):
                tmp.layers[0].set_offsets(0, 0) 
            pdb.file_png_save(dupe, tmp.layers[0], fullpath, filename, 0, 9, 1, 1, 1, 1, 1)
            layer.visible = is_visible
        style=""
        if layer.opacity != 100.0:
            style="opacity:"+str(layer.opacity/100.0)+";"
        if not layer.visible:
            style+="display:none"
        if style != "":
            style = 'style="'+style+'"'
        if inkscape_layers:
            image = '<g inkscape:groupmode="layer" inkscape:label="%s" %s>' % (layer.name.decode('utf-8'),style)
            style = ""
        if not pdb.gimp_item_is_group(layer):
            image += ('<image xlink:href="%s" x="%d" y="%d" width="%d" height="%d" %s/>\n' % 
                (fullpath,tmp.layers[0].offsets[0],tmp.layers[0].offsets[1],tmp.layers[0].width,tmp.layers[0].height,style))
        if pdb.gimp_item_is_group(layer):
            image += layer_process(layer.children, only_visible, dupe, path, flatten, remove_offsets, crop, inkscape_layers)
        if inkscape_layers:
            image += '</g>'
        images = image + images
        dupe.remove_layer(layer)
    return images

def export_as_svg(img, drw, path, only_visible=False, flatten=False, remove_offsets=False, crop=False, inkscape_layers=True):
    imagename = get_image_name(img)
    dupe = img.duplicate()
    layers = get_layers(dupe.layers, only_visible)
    images = layer_process(layers, only_visible, dupe, path, flatten, remove_offsets, crop, inkscape_layers)
    svgpath = os.path.join(path, imagename+".svg");
    svgfile = open(svgpath, "w")
    svgfile.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Generator: GIMP export as svg plugin -->

<svg xmlns:xlink="http://www.w3.org/1999/xlink" """)
    if inkscape_layers:
        svgfile.write('xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" ')
    svgfile.write('width="%d" height="%d">' % (img.width, img.height));
    svgfile.write(images);
    svgfile.write("</svg>");

register(
    proc_name=("python-fu-export-as-svg"),
    blurb=("Export as SVG"),
    help=("Export an svg file and an individual PNG file per layer."),
    author=("Erdem Guven <zuencap@yahoo.com>"),
    copyright=("Erdem Guven"),
    date=("2015"),
    label=("Export as SVG"),
    imagetypes=("*"),
    params=[
        (PF_IMAGE, "img", "Image", None),
        (PF_DRAWABLE, "drw", "Drawable", None),
        (PF_DIRNAME, "path", "Save PNGs here", os.getcwd()),
        (PF_BOOL, "only_visible", "Only Visible Layers?", False),
        (PF_BOOL, "flatten", "Flatten Images?", False),
        (PF_BOOL, "remove_offsets", "Remove Offsets?", False),
        (PF_BOOL, "crop", "Auto Crop", False),
        (PF_BOOL, "inkscape_layers", "Create Inkscape Layers?", True),
        ],
    results=[],
    function=(export_as_svg), 
    menu=("<Image>/File"), 
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
