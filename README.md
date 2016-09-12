# gimp-export-to-svg
## Version: 0.4.1, License: GPL v3+, Author: Erdem Guven
# pango-to-svg
## Version: 0.3, License: GPL v3+, Author: Jabiertxo Arraiza

###Requeriments
- Gimp 2.8
- python-lxml and his requeriments. Thanks Geyup!

###Install
Install on GIMP: put the 3 .py files in the repo on Gimp plug-ins folder. 
If linux, put the "gimp_..." files executables
The plugin is located in File->Export->SVG menu

###Changelog
####0.1 Allow option to export text as text to the result SVG.**
Know issues in export as text:
- Text can be moved a bit
- Gimp fixed width box not fit perfect
- Gimp indentation dont work

####0.2 batch process.
**Required**:
- **origin**: directory of images to process
- **dest**: path of output

**Optional**:
- **only_visible**: not export invisible layers
- **flatten**: not made layers
- **remove_offsets**:remove offsets,
- **crop**: each image to data only,
- **inkscape_layers**: add inkscape layers -a group with custom inkscape attribute
- **text_layers**: Layers as text
- **resolution_96**:96 DPI current svg DPI. False 90 DPI legacy SVG DPI

####0.3 bug fixes.
- Safe urls
- Images in relative mode

To run from command line:
```
gimp -i -b '(python-fu-batch-export-as-svg RUN-NONINTERACTIVE "_folder_input_" "_folder_output_" 0 0 0 0 1 1 1)' -b '(gimp-quit 0)'
```
Thanks Haakon!
```
Copyright 2010 Erdem Guven
Copyright 2009 Chris Mohler
Copyright 2015 Jabiertxo Arraiza
"Only Visible" and filename formatting introduced by mh
"Retain visibility", "Layer Groups to nested Inkscape layers" "Crop layer" introduced by Jabiertxof
"Flattern" "Offset" introduced by Jabiertxof based on  http://registry.gimp.org/node/18440
Update to 0.4 code http://registry.gimp.org/node/25049
Based on  http://registry.gimp.org/node/18440

