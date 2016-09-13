#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Erdem Guven <zuencap@yahoo.com>
# Copyright 2010 Erdem Guven
# Copyright 2009 Chris Mohler
# Copyright 2015 Jabiertxof
# "Only Visible" and filename formatting introduced by mh
# "Groups" "Crop layer" introduced by Jabiertxof
# "Export as text" "Flattern" "Offset" introduced by Jabiertxof from http://registry.gimp.org/node/18440
# License: GPL v3+
# Version 0.3.6
# GIMP plugin to export as SVG

from gimpfu import *
import os, re, random, pango
from lxml import etree
from StringIO import StringIO
from pango_to_svg import *
import urllib

def format_filename(img, layer, urlencode_files, strip_extension):
    filename = img.name + '-' + layer.name + '.png'
    if strip_extension :
        filename = os.path.splitext(img.name)[0] + '-' + layer.name + '.png'
    if not urlencode_files:
        return filename.decode('utf-8')
    return urllib.quote(filename)

def get_image_name(img, urlencode_files):
    if not urlencode_files:
        imgname = img.name.decode('utf-8')
        return imgname
    return urllib.quote(img.name)

def get_layers(layers, only_visible):
    result = []
    for layer in layers:
        if not pdb.gimp_item_get_parent(layer):
            result.append(layer)
    return result

def layer_process(img, layers, only_visible, dupe, path, flatten=False, remove_offsets=False, crop=False, inkscape_layers=True, text_layers=True, resolution_96=True, non_xcf=False, urlencode_files = True, strip_extension = False):
    svg = ""
    version = gimp.version[0:2]
    is_2dot8_up = version[0] >= 2 and version[1] >= 8
    get_resolution = pdb.gimp_image_get_resolution(dupe)
    resolution = (get_resolution[0] + get_resolution[1])/2.0
    output_resolution = 90.0
    if resolution_96:
        output_resolution = 96.0
    for layer in layers:
        if only_visible:
            if not layer.visible:
                continue
        data = ""
        pdb.gimp_image_set_active_layer(dupe, layer)
        if non_xcf:
            image = pdb.gimp_image_get_uri(img)
            filename = os.path.basename(image)
            if not urlencode_files:
                imgname = img.name.decode('utf-8')
                filename = imgname
        else:
            filename = format_filename(img, layer, urlencode_files, strip_extension)
        fullpath = os.path.join(path, filename);
        tmp = False
        if (not is_2dot8_up or not pdb.gimp_item_is_group(layer)) and (not pdb.gimp_item_is_text_layer(layer) or not text_layers):
            is_visible = layer.visible
            layer.visible = 1
            tmp = pdb.gimp_image_new(pdb.gimp_image_width(dupe), pdb.gimp_image_height(dupe), pdb.gimp_image_base_type(dupe))
            pdb.gimp_image_insert_layer(tmp, pdb.gimp_layer_new_from_drawable(pdb.gimp_image_get_active_drawable(dupe), tmp), None, 0)
            if flatten:
                tmp.flatten()
            if crop:
                pdb.plug_in_autocrop_layer(tmp, tmp.layers[0])
            if remove_offsets:
                tmp.layers[0].set_offsets(0, 0) 
            if not non_xcf:
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
            data = '<g inkscape:groupmode="layer" inkscape:label="%s" %s>' % (layer.name.decode('utf-8'),style)
            style = ""
        if (not is_2dot8_up or not pdb.gimp_item_is_group(layer)) and not pdb.gimp_item_is_text_layer(layer):
            data += ('<image xlink:href="%s" x="%d" y="%d" width="%d" height="%d" %s/>\n' % 
                (filename,tmp.layers[0].offsets[0],tmp.layers[0].offsets[1],tmp.layers[0].width,tmp.layers[0].height,style))
        if pdb.gimp_item_is_text_layer(layer) and text_layers:
            color = pdb.gimp_text_layer_get_color(layer)
            font_info = pango.FontDescription(pdb.gimp_text_layer_get_font(layer))
            container_line_height = pdb.gimp_text_layer_get_line_spacing(layer)
            indent = pdb.gimp_text_layer_get_indent(layer)
            markup = pdb.gimp_text_layer_get_markup(pdb.gimp_image_get_active_drawable(dupe))
            if not markup:
                markup = "<markup>" + pdb.gimp_text_layer_get_text(pdb.gimp_image_get_active_drawable(dupe)) + "<markup>"
            fontsize = pdb.gimp_text_layer_get_font_size(layer)
            factor = pdb.gimp_unit_get_factor(fontsize[1])
            hackToTypoGr = 1.0
            if fontsize[1] < 9:
                hackToTypoGr =72.2/72.0
            if fontsize:
                if factor > 0:
                    container_font_size = (fontsize[0] / (factor/resolution)) * hackToTypoGr
                else:
                    container_font_size = math.floor(fontsize[0] * hackToTypoGr)
            container_letter_spacing = pdb.gimp_text_layer_get_letter_spacing(layer)
            direction = pdb.gimp_text_layer_get_base_direction(layer)
            containerDirection = "rtl"
            if direction is 0:
                containerDirection = "ltr"
            svg_text = PangoToSVG(markup)
            svg_text.setContainerLineHeight(container_line_height)
            svg_text.setContainerLetterSpacing(container_letter_spacing)
            svg_text.setContainerDirection(containerDirection)
            svg_text.setContainerIndent(indent)
            svg_text.setContainerWidth(layer.width)
            svg_text.setContainerHeight(layer.height)
            svg_text.setContainerOffsetX(layer.offsets[0])
            svg_text.setContainerOffsetY(layer.offsets[1])
            svg_text.setContainerFont(font_info)
            svg_text.setContainerFontSize(container_font_size)
            svg_text.setContainerColor(color)
            svg_text.setInputResolution(resolution)
            svg_text.setOutputResolution(output_resolution)
            data += svg_text.parse()
            #pdb.gimp_message(markup)
        if is_2dot8_up and pdb.gimp_item_is_group(layer):
            data += layer_process(layer.children, only_visible, dupe, path, flatten, remove_offsets, crop, inkscape_layers)
        if inkscape_layers:
            data += '</g>'
        svg = data + svg
        dupe.remove_layer(layer)
    return svg

def export_non_xcf_as_svg(img, dest, only_visible=False, flatten=False, remove_offsets=False, crop=False, inkscape_layers=True, text_layers=True, resolution_96=True, urlencode_files = True, strip_extension = False):
    image = pdb.gimp_image_get_uri(img)
    imagename = os.path.basename(image)
    if not urlencode_files:
        imagename = img.name.decode('utf-8')
    if strip_extension :
        imagename = os.path.splitext(imagename)[0]
    dupe = img.duplicate()
    layers = get_layers(dupe.layers, only_visible)
    svg_procesed = layer_process(img, layers, only_visible, dupe, dest, flatten, remove_offsets, crop, inkscape_layers, text_layers, resolution_96, True, urlencode_files, strip_extension)
    svgpath = os.path.join(dest, imagename+".svg");
    svgfile = open(svgpath, "w")
    svgfile.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Generator: GIMP export as svg plugin -->

<svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" """)
    svgfile.write(' width="%dpx" height="%dpx" viewBox="0 0 %d %d" version="1.1">' % (img.width, img.height, img.width, img.height));
    svgfile.write("""<defs id="defs2" />
<sodipodi:namedview id="base" pagecolor="#ffffff" bordercolor="#666666" borderopacity="1.0" inkscape:pageopacity="0.0" inkscape:pageshadow="2" inkscape:document-units="px" showgrid="false"  inkscape:window-maximized="1" />
<metadata id="metadata5">
<rdf:RDF>
<cc:Work rdf:about="">
<dc:format>image/svg+xml</dc:format>
<dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
<dc:title></dc:title>
</cc:Work>
</rdf:RDF>
</metadata>""");
    svgfile.write(svg_procesed);
    svgfile.write("</svg>");
    
def export_as_svg(img, dest, only_visible=False, flatten=False, remove_offsets=False, crop=False, inkscape_layers=True, text_layers=True, resolution_96=True, urlencode_files = True, strip_extension = False):
    imagename = get_image_name(img, urlencode_files)
    if strip_extension :
        imagename = os.path.splitext(imagename)[0]
    dupe = img.duplicate()
    layers = get_layers(dupe.layers, only_visible)
    svg_procesed = layer_process(img, layers, only_visible, dupe, dest, flatten, remove_offsets, crop, inkscape_layers, text_layers, resolution_96, False, urlencode_files, strip_extension)
    svgpath = os.path.join(dest, imagename+".svg");
    svgfile = open(svgpath, "w")
    svgfile.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Generator: GIMP export as svg plugin -->

<svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" """)
    svgfile.write(' width="%dpx" height="%dpx" viewBox="0 0 %d %d" version="1.1">' % (img.width, img.height, img.width, img.height));
    svgfile.write("""<defs id="defs2" />
<sodipodi:namedview id="base" pagecolor="#ffffff" bordercolor="#666666" borderopacity="1.0" inkscape:pageopacity="0.0" inkscape:pageshadow="2" inkscape:document-units="px" showgrid="false"  inkscape:window-maximized="1" />
<metadata id="metadata5">
<rdf:RDF>
<cc:Work rdf:about="">
<dc:format>image/svg+xml</dc:format>
<dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
<dc:title></dc:title>
</cc:Work>
</rdf:RDF>
</metadata>""");
    svgfile.write(svg_procesed);
    svgfile.write("</svg>");

register(
    proc_name=("python-fu-export-as-svg"),
    blurb=("Export as SVG"),
    help=("Export to SVG."),
    author=("Erdem Guven <zuencap@yahoo.com>"),
    copyright=("Erdem Guven"),
    date=("2015"),
    label=("Export as SVG"),
    imagetypes=("*"),
    params=[
        (PF_IMAGE, "img", "Image", None),
        (PF_DIRNAME, "dest", "Save here", os.getcwd()),
        (PF_BOOL, "only_visible", "Only Visible Layers?", False),
        (PF_BOOL, "flatten", "Flatten Images?", False),
        (PF_BOOL, "remove_offsets", "Remove Offsets?", False),
        (PF_BOOL, "crop", "Auto Crop", False),
        (PF_BOOL, "inkscape_layers", "Create Inkscape Layers?", True),
        (PF_BOOL, "text_layers", "Retain text layers as text?", True),
        (PF_BOOL, "resolution_96", "Use new SVG 96DPI resolution?", True),
        (PF_BOOL, "urlencode_files", "URL encode file names?", True),
        (PF_BOOL, "strip_extension", "Remove original extension", False)
        ],
    results=[],
    function=(export_as_svg), 
    menu=("<Image>/File/Export/SVG/")
    )

if __name__=='__main__': main()
