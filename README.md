# gimpToSVG
Version: 0.3.4, License: GPL v3-or-later

##Objective
**Normal mode:**
Convert the current Gimp document to an SVG file.
Main features:
- Optionaly export hidden layers
- Flatten all layers to one image only
- Crop each image layer to the size of the layer and position it in the proper location within the image
- Recreate layers of any depth (Inkscape)
- Export text as a text element or as an image
- Optional legacy and current SVG 96DPI mode.

**Batch mode:**
- All the previous features
- Also wrap into SVG PNG, JPG, TIFF, BMP and GIF files
- Work inside Gimp or on the command line

##Requirements
- Gimp 2.8
- python-lxml

##Installation
Copy the three "*.py" files from the git repository's working copy to
Gimp’s plug-ins folder.<br />
If on a Unix-like system, make the "gimp_*" files executables.<br />
The plugin can be invoked from the File->Export->SVG menu.<br />

##Changelog
###0.1.0 Initial release
Author: Erdem Guven and Chris Mohler [original code](http://registry.gimp.org/node/25049)
###0.2.0 Allow option to export text as text to the result SVG.**
Added [pangoToSVG](https://github.com/jabiertxof/pangoToSVG). See know issues in this git
###0.3.0 batch process.
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
- **urlencode_files**: bool, Files are URL encoded

To run from command line:
```
gimp -i -b '(python-fu-batch-export-as-svg RUN-NONINTERACTIVE "origin_path" "dest_path" bool bool bool bool bool bool)' -b '(gimp-quit 0)'
```
###0.3.1 bug fixes.
- Safe URLs
- Images in relative mode

###0.3.2 bug fix.
- Fix a name bug on XCF exported layers

###0.3.3 bug fix.
- Remove warning duplicate pdb.

###0.3.4 add optional URL encode.
- Add a optional URL encode to file names.

##Credits

```
Copyright 2010 Erdem Guven
Copyright 2009 Chris Mohler
Copyright 2015 Jabiertxo Arraiza
```
Based on  http://registry.gimp.org/node/18440 and http://registry.gimp.org/node/25049<br />
Thanks to Geyup, the first issuer of the project and to the contributors who came later like Haakon.<br />
Thanks to [Shlomi Fish](http://www.shlomifish.org) for helping me on my english on README.md.
