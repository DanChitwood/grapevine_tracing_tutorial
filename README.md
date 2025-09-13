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
* Choose which side of the petiolar junction to start and stop the blade and veins tracing.
* Be mindful about blade overlaps that hide parts of the blade outline or veins and have a plan about how to trace these.
* To save an outline, go to `File/Save As/XY Coordinates...`
* Save with the exact file name but add `*_blade.txt` or `*_veins.txt` as appropriate.
* Try an example leaf tracing before committing to real data. You don't want to have to redo a trace!
* It takes 30-40 minutes to trace both the blade and veins.

# Check your work with a python script
* Watch the following tutorial about how to check your work: [https://youtu.be/3EpTxi4g214?feature=shared](https://youtu.be/3EpTxi4g214?feature=shared)
* For each leaf you trace, you should have 1) the original image file, 2) a `*_blade.txt` file of blade coordinates, and 3) a `*_veins.txt` file of vein coordiantes.
* Place the above three files for each leaf in the `data` subfolder.
* Run the `test_leaf_data.py` script insides the subfolder `scripts`.
* An `outputs` subfolder should be created with example trace images to check your work.
* If you have not installed the following python modules, you should run the following command in your terminal before running the script: `pip install opencv-python numpy`
