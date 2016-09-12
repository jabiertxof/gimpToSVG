# GimpToSVG
## Version: 0.4.5, License: GPL v3+

###Requeriments
- Gimp 2.8
- python-lxml

###Install
Put the tree ".py" files in the repo on Gimp plug-ins folder.<br />
If in linux, put the "gimp_..." files executables.<br />
The plugin is located in File->Export->SVG menu.<br />

###Changelog
####0.4.2 Allow option to export text as text to the result SVG.**
Know issues in export as text:
- Text can be moved a bit
- Gimp fixed width box not fit perfect
- Gimp indentation dont work

####0.4.3 batch process.
**Required**:
- **origin**: directory of images to process
- **dest**: directory of output

**Optional**:
- **only_visible**: boolean, not export invisible layers
- **flatten**: boolean, not made layers
- **remove_offsets**: boolean, remove offsets
- **crop**: boolean, each image to data only
- **inkscape_layers**: boolean, add inkscape layers -a group with custom inkscape attribute
- **text_layers**: boolean, Layers as text
- **resolution_96**: boolean,96 DPI current svg DPI. False 90 DPI legacy SVG DPI

To run from command line:
```
gimp -i -b '(python-fu-batch-export-as-svg RUN-NONINTERACTIVE "_folder_input_" "_folder_output_" bool bool bool bool bool bool)' -b '(gimp-quit 0)'
```
####0.4.4 bug fixes.
- Safe urls
- Images in relative mode

####0.4.5 bug fix.
- Fix a name bug on XCF exported layers

###Credits

```
Copyright 2010 Erdem Guven
Copyright 2009 Chris Mohler
Copyright 2015 Jabiertxo Arraiza
Based on  http://registry.gimp.org/node/18440 and http://registry.gimp.org/node/25049

Thanks to Geyup, the first issuer of the proyect and the people came later like Haakon, I hope this code is useful to us
```

