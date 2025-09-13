# Grapevine leaf tracing tutorial
a tutorial for tracing grapevine leaves and checking your results

# Leaf diagram
* Every grapevine leaf has five major veins: one midvein, two distal veins, two proximal veins
* Off each of the five major veins, there are three branches
* Ideally we want to trace all three branches for each of the five major veins. But there can be exceptions.
![alt](https://github.com/DanChitwood/grapevine_tracing_tutorial/blob/main/leaf_diagram.png)

# Tracing tutorial
* Watch the following tutorial about tracing blade and veins with FIJI/ImageJ: [https://youtu.be/MeLVKUxxUIE?feature=shared](https://youtu.be/MeLVKUxxUIE?feature=shared)
* Download FIJI/ImageJ here (FIJI is preferred): [https://imagej.net/downloads](https://imagej.net/downloads)

# Check your work with a python script
* Watch the following tutorial about how to check your work: [https://youtu.be/3EpTxi4g214?feature=shared](https://youtu.be/3EpTxi4g214?feature=shared)
* For each leaf you trace, you should have 1) the original image file, 2) a `*_blade.txt` file of blade coordinates, and 3) a `*_veins.txt` file of vein coordiantes.
* Place the above three files for each leaf in the `data` subfolder.
* Run the `test_leaf_data.py` script insides the subfolder `scripts`.
* An `outputs` subfolder should be created with example trace images to check your work.
* 
