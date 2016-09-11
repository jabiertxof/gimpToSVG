# gimp-export-to-svg
## Version: 0.4.1, License: GPL v3+, Author: Erdem Guven
# pango-to-svg
## Version: 0.1, License: GPL v3+, Author: Jabiertxo Arraiza
```
Copyright 2010 Erdem Guven
Copyright 2009 Chris Mohler
Copyright 2015 Jabiertxo Arraiza
Tested in Gimp 2.8

Install on GIMP: download the 2 .py files and put on plug-ins folder of Gimp. If linux, put the "gimp_..." file executable
The plugin is located in File->Export menu
Need python-lxml. Thanks https://github.com/Geyup!

Update to 0.4 code http://registry.gimp.org/node/25049
Based on  http://registry.gimp.org/node/18440
Dont upload in gimp registry because site in lockdown mode for spam
Put the .py file in Gimp plugin folder and if linux make it executable

"Only Visible" and filename formatting introduced by mh
"Retain visibility", "Layer Groups to nested Inkscape layers" "Crop layer" introduced by Jabiertxof
"Flattern" "Offset" introduced by Jabiertxof based on  http://registry.gimp.org/node/18440
In 0.4 allow option to export text as text to the result SVG.
Know issues in export as text:
*Text can be moved a bit
*Gimp fixed width box not fit perfect
*Gimp indentation dont work
```
