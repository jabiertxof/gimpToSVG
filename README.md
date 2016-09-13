# gimpToSVG
Version: 0.3.5, License: GPL v3-or-later

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
- Optional URL encode file names

**Batch mode:**
- All the previous features
- Also wrap into SVG PNG, JPG, TIFF, BMP and GIF files
- Work inside Gimp or on the command line

Important, be sure all files has correct mimetypes, if not want a error.<br />
Ecxample: To find all ".gif" files and check his real mime types with image-magic:
> identify *.gif|grep -v GIF | wc -l

##Requirements
- Gimp 2.8
- python-lxml

##Installation
Copy the three "\*.py" files from the git repository's working copy to
Gimp’s plug-ins folder.<br />
If on a Unix-like system, make the "gimp_*" files executables.<br />
The plugin can be invoked from the File->Export->SVG menu.<br />

##Changelog
###0.1.0 Initial release
Author: Erdem Guven and Chris Mohler [original code](http://registry.gimp.org/node/25049)
###0.2.0 Allow option to export text as text to the result SVG.**
Added [pangoToSVG](https://github.com/jabiertxof/pangoToSVG). See know issues in this git
###0.3.0 Add batch process.
**Required**:
- **origin**: path, directory of images to process
- **dest**: path, directory of output

**Optional**:
- **only_visible**: bool, default 0, not export invisible layers
- **flatten**: bool, default 0, not made layers
- **remove_offsets**: bool, default 0, remove offsets
- **crop**: bool, default 0, each image to data only
- **inkscape_layers**: bool, default 1, add inkscape layers -a group with custom inkscape attribute
- **text_layers**: bool, default 1, layers as text
- **resolution_96**: bool, default 1, 96 DPI current svg DPI. False 90 DPI legacy SVG DPI
- **urlencode_files**: bool, default 1, files are URL encoded
- **strip_extension** bool, default 0, remove original extension !this can be wrong on files with the same name and diferent extension

To run from command line:
```
gimp -i -b '(python-fu-batch-export-as-svg RUN-NONINTERACTIVE "origin_path" "dest_path" bool bool bool bool bool bool bool bool bool)' -b '(gimp-quit 0)'
```
###0.3.1 Bugs fix.
- Safe URLs
- Images in relative mode

###0.3.2 Bug fix.
- Fix a name bug on XCF exported layers

###0.3.3 Bug fix.
- Remove warning duplicate pdb.

###0.3.4 Add, optional, URL encode.
- Add a optional URL encode to file names.

###0.3.5 Add, optional, strip original extension.
- Strip original extension from output.

##Credits
```
Copyright 2010 Erdem Guven
Copyright 2009 Chris Mohler
Copyright 2015 Jabiertxo Arraiza
```
Based on  http://registry.gimp.org/node/18440 and http://registry.gimp.org/node/25049<br />
Thanks to Geyup, the first issuer of the project and to the contributors who came later like Haakon.<br />
Thanks to [Shlomi Fish](http://www.shlomifish.org) for helping me on my english.
