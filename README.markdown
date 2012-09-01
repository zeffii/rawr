This repository contains my favourite homebrew scripts. Any future blender scripting that I do will be available from here. 

##### blender/scripts/addons_contrib/text_editor_extras/
[text editor eval selection](https://github.com/zeffii/rawr/tree/master/blender/scripts/addons_contrib/text_editor_extras): Will eval the current selection and replace it with the result.  

[text editor chroma key](https://github.com/zeffii/rawr/tree/master/blender/scripts/addons_contrib/text_editor_extras): A one click method to enable syntax highlighting and ruler etc.  

##### blender/scripts/addons_contrib/io_material_loader/
[this addon](https://github.com/zeffii/rawr/tree/master/blender/scripts/addons_contrib/io_material_loader): An example of how to link_append from other blender files, to turn them into a library.  

##### blender/scripts/addons_contrib/io_import_mesh_afm_ascii/
[this addon](https://github.com/zeffii/rawr/tree/master/blender/scripts/addons_contrib/io_import_mesh_afm_ascii): Reads ascii format Atomic Force Microscope data files and generates a mesh from the z data grid.  

##### blender/scripts/addons_contrib/
[monster tile v3 005.py](https://github.com/zeffii/rawr/blob/master/blender/scripts/addons_contrib/monster_tile_v3_005.py): A region/border/tile renderer for cycles and blender internal, useful for when you don't have enough ram to render a scene. I also wrote a couple of different scripts to automatically stitch these tiles together. [More info here](https://github.com/zeffii/Monster_Tile_Renderer/wiki/Monster-Tile-Renderer---Info-sheet.)  

[txt editor gist import addon.py](https://github.com/zeffii/rawr/blob/master/blender/scripts/addons_contrib/txt_editor_gist_import_addon.py): Feed it a gist reference and it will download the file into the text editor.  

[mesh edge intersection tools.py](https://github.com/zeffii/rawr/blob/master/blender/scripts/addons_contrib/mesh_edge_intersection_tools.py): edge projection(V), edge extention(T) and edge intersection(X) tool. (ugly but battle hardened). Included in [Blenders SVN for addons_contrib](http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Modeling/Edge_Slice)  

[Empty placing addon.py](https://github.com/zeffii/rawr/blob/master/blender/scripts/addons_contrib/Empty_placing_addon.py): Places empties at selected vertex locations.  

##### blender/scripts/image_manipulation/
[firefly removal extended.py](https://github.com/zeffii/rawr/blob/master/blender/scripts/image_manipulation/firefly_removal_extended.py): This is a tentative and primative approach to dealing with obvious fireflies automatically without imploying bidirectional smoothing. discontinued due to better cycles algorithms and special composite nodes. It's a very interesting field!  

##### blender/scripts/tests
[blender version igs import.py](https://github.com/zeffii/rawr/blob/master/blender/scripts/tests/blender_version_igs_import.py): An importer for a limited set of IGS spline types.   

##### blender/scripts/templates/
[operator and button 3dview.py](https://github.com/zeffii/rawr/blob/master/blender/scripts/templates/operator_and_button_3dview.py): I use this to quickly load a boilerplate for random projects, includes references to often used views.  

##### /svg_tests/
[bpy to svg.py](https://github.com/zeffii/rawr/blob/master/svg_tests/bvp_to_svg.py): can render the currently selected object from 3dview as an svg and writes it out onto the filesystem.  

