# GimpToSVG
## Version: 0.4.5, License: GPL v3+

###Requeriments
- Gimp 2.8
- python-lxml

###Install
Put the tree ".py" files in the repo on Gimp plug-ins folder.<br />
If in linux, put the "gimp_*" files executables.<br />
The plugin is located in File->Export->SVG menu.<br />

###Changelog
####0.1.0 Initial release
Author: Erdem Guven and Chris Mohler [original code](http://registry.gimp.org/node/25049)
####0.2.0 Allow option to export text as text to the result SVG.**
Know issues in export as text:
- Text can be moved a bit
- Gimp fixed width box not fit perfect
- Gimp indentation dont work

####0.3.0 batch process.
**Required**:
- **origin**: path, directory of images to process
- **dest**: path, directory of output

**Optional**:
- **only_visible**: bool, not export invisible layers
- **flatten**: bool, not made layers
- **remove_offsets**: bool, remove offsets
- **crop**: bool, each image to data only
- **inkscape_layers**: bool, add inkscape layers -a group with custom inkscape attribute
- **text_layers**: bool, Layers as text
- **resolution_96**: bool,96 DPI current svg DPI. False 90 DPI legacy SVG DPI

To run from command line:
```
gimp -i -b '(python-fu-batch-export-as-svg RUN-NONINTERACTIVE "origin_path" "dest_path" bool bool bool bool bool bool)' -b '(gimp-quit 0)'
```
####0.3.1 bug fixes.
- Safe urls
- Images in relative mode

####0.3.2 bug fix.
- Fix a name bug on XCF exported layers

###Credits

```
Copyright 2010 Erdem Guven
Copyright 2009 Chris Mohler
Copyright 2015 Jabiertxo Arraiza
Based on  http://registry.gimp.org/node/18440 and http://registry.gimp.org/node/25049

Thanks to Geyup, the first issuer of the proyect and the people came later like Haakon, I hope this code is useful to us
```


