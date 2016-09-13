#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015 Jabiertxof
# License: GPL v3+
# Version 0.1.1
# Pango to SVG
# https://github.com/jabiertxof/pangoToSVG

import os, re, random, pango, gtk, pangocairo, math
import lxml.etree as etree
from StringIO import StringIO

class PangoToSVG:
    def __init__(self, markup):
        self.SVG = ""
        self.markup = markup
        self.container_line_height = 0
        self.container_letter_spacing = 0
        self.container_direction = "ltr"
        self.container_indent = 0
        self.container_width = 0
        self.container_height = 0
        self.container_offset_X = 0
        self.container_offset_Y = 0
        self.container_font = pango.FontDescription("serif")
        self.container_font_size = 12
        self.container_color = [0,0,0,255]
        self.input_resolution = 72.0
        self.output_resolution = 96.0
        self.pango_stretch = { pango.STRETCH_ULTRA_CONDENSED : "ultra-condensed",
                               pango.STRETCH_EXTRA_CONDENSED : "extra-condensed",
                               pango.STRETCH_CONDENSED : "condensed",
                               pango.STRETCH_SEMI_CONDENSED : "semi-condensed",
                               pango.STRETCH_NORMAL : "normal",
                               pango.STRETCH_SEMI_EXPANDED : "semi-expanded",
                               pango.STRETCH_EXPANDED : "expanded",
                               pango.STRETCH_EXTRA_EXPANDED : "extra-expanded",
                               pango.STRETCH_ULTRA_EXPANDED: "ultra-expanded" }
        self.pango_weight = {   pango.WEIGHT_ULTRALIGHT : "200",
                               pango.WEIGHT_LIGHT : "300",
                               pango.WEIGHT_NORMAL : "400",
                               pango.WEIGHT_BOLD : "700",
                               pango.WEIGHT_ULTRABOLD : "800",
                               pango.WEIGHT_HEAVY : "900"}
        self.pango_variant = { pango.VARIANT_NORMAL : "normal",
                               pango.VARIANT_SMALL_CAPS : "small-caps"}
        self.pango_style = {   pango.STYLE_NORMAL : "normal",
                               pango.STYLE_ITALIC : "italic",
                               pango.STYLE_OBLIQUE : "oblique"}
        self.factor = self.input_resolution/self.output_resolution
        self.counter = random.randint(1000,9000)


    def setContainerLineHeight(self, container_line_height):
        self.container_line_height = container_line_height

    def setContainerLetterSpacing(self, container_letter_spacing):
        self.container_letter_spacing = container_letter_spacing
    
    def setContainerDirection(self, container_direction):
        self.container_direction = container_direction

    def setContainerIndent(self, container_indent):
        self.container_indent

    def setContainerWidth(self,container_width):
        self.container_width = container_width

    def setContainerHeight(self,container_height):
        self.container_height = container_height
    
    def setContainerOffsetX(self,container_offset_X):
        self.container_offset_X = container_offset_X

    def setContainerOffsetY(self,container_offset_Y):
        self.container_offset_Y = container_offset_Y

    def setContainerFont(self, container_font):
        self.container_font = container_font

    def setContainerFontSize(self,container_font_size):
        self.container_font_size = container_font_size

    def setContainerColor(self, container_color):
        self.container_color = container_color

    def setInputResolution(self, input_resolution):
        self.input_resolution = input_resolution
    
    def setOutputResolution(self, output_resolution):
        self.output_resolution = output_resolution

    def parse(self):
        attr_list, text, accel = pango.parse_markup( self.markup )
        minIndex = 0
        maxIndex = 0
        out = "<flowRoot "
        out += ' xml:space="preserve"'
        out += ' style="'
        out += 'letter-spacing:' + str(self.container_letter_spacing) +";"
        out += "font-style:"+ str(self.pango_style[self.container_font.get_style()]) +";"
        out += "font-weight:"+ str(self.pango_weight[self.container_font.get_weight()]) +";"
        out += "font-variant:"+ str(self.pango_variant[self.container_font.get_variant()]) +";"
        out += "font-family:'"+ self.container_font.get_family() + "';"
        out += "font-stretch:"+ str(self.pango_stretch[self.container_font.get_stretch()]) + ";"
        out += "-inkscape-font-specification:'" + str(self.container_font) + "';"
        out += "font-size:" + str(math.ceil(self.container_font_size)) + "px;"
        out += "fill:rgb(" + str(self.container_color[0]) +"," + str(self.container_color[1]) +"," + str(self.container_color[2]) + ");"
        out += "fill-opacity:" + str(self.container_color[3]/255.0) + ";"
        out += '"'
        out += ' direction="' + self.container_direction + '"'
        out += ' x="' + str(self.container_offset_X) + '"'
        out += ' y="' + str(self.container_offset_Y) + '"'
        out += '>'
        out += '<flowRegion>';
        out += '<rect'
        out += ' width="' + str(self.container_width - self.container_indent) + '"'
        out += ' height="' + str(self.container_height + self.getTopExents(attr_list, text)) + '"'
        out += ' x="' + str(self.container_offset_X + self.container_indent) + '"'
        out += ' y="' + str(self.container_offset_Y) + '"'
        out += ' />';
        out += '</flowRegion>';
        outText = text
        
        data = self.toSvg(attr_list, text)
        data.sort(key = lambda x : x[0])
        gap = 0
        for el in data:
            if el[1] != "</flowPara>" and el[1] != "</flowSpan>":
                el[1] = el[1].replace("flowPara", 'flowPara id="' + str(self.counter) + '"')
            outText = outText[:el[0] + gap] + el[1] + outText[el[0] + gap:]
            gap += len(el[1])
            self.counter += 1
        return out + outText.replace('style=""','').replace("\n","") + "</flowRoot>"
    
    def getTopExents(self, attr_list, text):
        c = pango.FontMap.create_context(pangocairo.cairo_font_map_get_default())
        l = pango.Layout(c)
        l.set_attributes(attr_list)
        l.set_text(text)
        line = l.get_line(0)
        return (line.get_pixel_extents()[1][3]-line.get_pixel_extents()[0][3])  * (self.input_resolution/self.output_resolution)
    
    def toSvg(self, attr_list, text):
        attr_array = self.attrListToArr(attr_list)
        attr_array = self.getAttrs(attr_array, text)
        attr_array = self.cleanAttrList(attr_array)
        return self.flattern(attr_array, text)

    def attrListToArr(self, attr_list):
        attr_array = []
        val = True
        attr_iter = attr_list.get_iterator()
        while val:
            for attr in attr_iter.get_attrs():
                attr_array.append(attr)
            val = attr_iter.next()
        return attr_array

    def arrToAttrList(self, attr_arr):
        attr_list = pango.AttrList()
        val = True
        for attr in attr_arr:
            attr_list.insert(attr)
        return attr_list

    def getAttrs(self, attr_array, text):
        attr_array_tmp = []
        newlines = [x for x, v in enumerate(text) if v == '\n']
        startIndex = 0
        for line in newlines:
            attr_array_tmp += self.getLineAttrs(attr_array, startIndex, line)
            startIndex = line
        attr_array_tmp += self.getLineAttrs(attr_array, startIndex, len(text))
        return attr_array_tmp

    def getLineAttrs(self, attr_array, start, end):
        attr_array_tmp = []
        container = pango.AttrBackground(54321, 12345, 6553, start, end)
        attr_array_tmp.append(container)
        for attr in attr_array:
            if attr.end_index <= start:continue
            if attr.start_index >= end:continue
            attr_copy = attr.copy()
            if attr_copy.end_index > end:
                attr_copy.end_index = end
            if attr.start_index < start:
                attr_copy.start_index = start
            attr_array_tmp.append(attr_copy)
        return attr_array_tmp

    def attrEqual(self, attr, attr2):
        if attr.start_index != attr2.start_index:return False
        if attr.end_index != attr2.end_index:return False
        if attr.type != attr2.type:return False
        if attr.type == 10 and attr2.type == 10:
            color = getattr( attr, 'color' )
            color2 = getattr( attr2, 'color' )
            if color.red != color2.red:return False
            if color.green != color2.green:return False
            if color.blue != color2.blue:return False
        return True

    def inAttrList(self, attr, attr_array):
        for attr2 in attr_array:
            if self.attrEqual(attr, attr2):
                return True
        return False

    def cleanAttrList(self, attr_array):
        attr_array_tmp = []
        for attr in attr_array:
            attr_copy = attr.copy()
            if not self.inAttrList(attr, attr_array_tmp):
                attr_array_tmp.append(attr_copy)
        return attr_array_tmp

    def flattern(self, attr_array, text):
        data = []
        attr_values = ('value', 'desc', 'color')
        style = { pango.STYLE_NORMAL : 'normal', pango.STYLE_ITALIC : 'italic', pango.STYLE_OBLIQUE : 'oblique'}
        previous_start = 0
        previous_end = 0
        acumulated_line_height = 0;
        c = pango.FontMap.create_context(pangocairo.cairo_font_map_get_default())
        l = pango.Layout(c)
        last_font = str(self.container_font)
        line_index = 0
        for attr in attr_array:
            name = attr.type
            start = attr.start_index
            end = attr.end_index
            if start == end:
                continue
            name = pango.AttrType(name).value_nick
            value = False
            for attr_value in attr_values:
                if hasattr( attr, attr_value ):
                    value = getattr( attr, attr_value )
                    break
            
            fill = ""
            if name == "foreground":
                fill = "fill:rgb(" + str((value.red*255)/65535) + "," + str((value.green*255)/65535) + "," + str((value.blue*255)/65535) + ");"
            
            underline = ""
            if name == "underline":
                underline = "text-decoration:underline;"
            
            strike = ""
            if name == "strikethrough":
                strike = "text-decoration:line-through;"

            font_style = ""
            font_weight = ""
            font_variant = ""
            font_family = ""
            font_stretch = ""
            inkscape_font_specification = ""
            if name == "font-desc":
                font_attrb = value.get_set_fields();
                last_font = str(value)
                if(font_attrb & pango.FONT_MASK_STYLE):
                    font_style = "font-style:"+ str(self.pango_style[value.get_style()]) +";"
                if(font_attrb & pango.FONT_MASK_WEIGHT):
                    font_weight = "font-weight:"+ str(self.pango_weight[value.get_weight()]) +";"
                if(font_attrb & pango.FONT_MASK_VARIANT):
                    font_variant = "font-variant:"+ str(self.pango_variant[value.get_variant()]) +";"
                if(font_attrb & pango.FONT_MASK_FAMILY):
                    font_family = "font-family:'"+ value.get_family() + "';"
                    inkscape_font_specification = "-inkscape-font-specification:'" + str(value) + "';"
                if(font_attrb & pango.FONT_MASK_STRETCH):
                    font_stretch = "font-stretch:"+ str(self.pango_stretch[value.get_stretch()]) + ";"
            
            letter_spacing = ""
            if name == "letter-spacing":
                letter_spacing = "letter-spacing:" + str((((value/1024.0) / (self.input_resolution/self.output_resolution))/10)) + "px;"

            size = ""
            if name == "size":
                size = "font-size:" + str(math.ceil((value/1024.0) * (72.0/72.27))) + "px;"

            sub_super = ""
            if name == "scale":
                if value < 1:
                    sub_super = "font-size:" + str(value * 100) + "%;baseline-shift:sub;"
                elif value > 1:
                    sub_super = "font-size:" + str(value * 100) + "%;baseline-shift:super;"

            rise = ""
            if name == "rise" and value != 1024:
                rise = "baseline-shift:" + str((value/1024.0)) + ";"

            line_height = ""
            flowPara = False
            if name == "background" and value.red == 54321 and value.green == 12345 and value.blue == 6553:
                flowPara = True
                attr_list_full = self.arrToAttrList(attr_array)
                l.set_attributes(attr_list_full)
                l.set_text(text)
                line = l.get_line(line_index)
                line_index += 1
                if line_index == 1:
                    line_height = "line-height:" + str(math.floor(line.get_pixel_extents()[1][3] + (line.get_pixel_extents()[1][3]-line.get_pixel_extents()[0][3]))  * (self.input_resolution/self.output_resolution)) + "px;"
                else:
                    line_height = "line-height:" + str(math.floor(line.get_pixel_extents()[1][3])  * (self.input_resolution/self.output_resolution)) + "px;"
             
            if previous_start == start and previous_end == end:
                start_tag = data[len(data)-2]
                if ';fill:' not in start_tag[1] and '"fill:' not in start_tag[1]:
                    start_tag[1] = start_tag[1].replace('style="','style="' + fill)
                if ';text-decoration:' not in start_tag[1] and '"text-decoration:' not in start_tag[1]:
                    start_tag[1] = start_tag[1].replace('style="','style="' + underline + strike)
                if ';font-style:' not in start_tag[1] and '"font-style:' not in start_tag[1]:
                    start_tag[1] = start_tag[1].replace('style="','style="' + font_style)
                if ';font-weight:' not in start_tag[1] and '"font-weight:' not in start_tag[1]:
                    start_tag[1] = start_tag[1].replace('style="','style="' + font_weight)
                if ';font-stretch:' not in start_tag[1] and '"font-stretch:' not in start_tag[1]:
                    start_tag[1] = start_tag[1].replace('style="','style="' + font_stretch)
                if ';font-variant:' not in start_tag[1] and '"font-variant:' not in start_tag[1]:
                    start_tag[1] = start_tag[1].replace('style="','style="' + font_variant)
                if ';font-family:' not in start_tag[1] and '"font-family:' not in start_tag[1]:
                    start_tag[1] = start_tag[1].replace('style="','style="' + font_family)
                if ';-inkscape-font-specification:' not in start_tag[1] and '"-inkscape-font-specification:' not in start_tag[1]:
                    start_tag[1] = start_tag[1].replace('style="','style="' + inkscape_font_specification)
                if ';letter-spacing:' not in start_tag[1] and '"letter-spacing:' not in start_tag[1]:
                    start_tag[1] = start_tag[1].replace('style="','style="' + letter_spacing)
                if ';font-size:' not in start_tag[1] and '"font-size:' not in start_tag[1]:
                    start_tag[1] = start_tag[1].replace('style="','style="' + size)
                if ';baseline-shift:' not in start_tag[1] and '"baseline-shift:' not in start_tag[1]:
                    start_tag[1] = start_tag[1].replace('style="','style="' + rise)
            else:
                if flowPara:
                    element = "flowPara"
                else:
                    element = "flowSpan"
                data.append([start,'<' + element  + ' style="' + rise + fill + underline + font_stretch + font_weight + font_variant + font_style + font_family + inkscape_font_specification + letter_spacing + size + sub_super + line_height + '">'])
                data.append([end, '</'+ element +'>'])
            previous_start = attr.start_index
            previous_end = attr.end_index
        return data
