Manual
======

Introduction
~~~~~~~~~~~~
This section contains a manual for the Lise Analyzer app. You will find here all necessary information about how to navigate around the app and how to use available options. You'll get a general view of the applications layout and what it contains. The manual covers the topic of data preparation for analisis.

Layout
~~~~~~
When you first open the application in your web browser, you'll see a page which is divided into 3 diffrent parts:

1. **Graph picker** (left green panel) - this is the panel which contains options for choosing types of graphs you want to display,
2. **Filters** (right blue panel) - a panel in which you filter the data files you want to use in your data analisis,
3. **List of graphs** (bottom panel) - at the beginning, this panel has only an empty dropdown. After adding graphs using options from graph picker new graphs will be displayed below the dropdown.

Options
~~~~~~~
Each panel contains its own options.

1. **Graph picker** - on this panel you can find 5 different groups of data for graphs you can create. Each group of data is named depending on a type of variables the graph is about to present. The available groups are: *Conservation*, *Center of mass*, *Deformation*, *Pairing* and *Miscellaneous*. The last group of data is for the data types that doesn't belong to any of previous ones and the users can add their own data types to it. In each group of data there are 4 available options:

    * **Y axis scale (linear/log)** - radio buttons which set a scale of y axis to linear or logarithmic,
    * **Data type** - a dropdown, which sets a variable (data type) for y axis of the graph (data types for each groups of data can be found in section Data types),
    * **X axis domain (in time/in distance/as maps)** - radio buttons which set a domain of x axis. Two first groups of data have only time domain for a choice, while the rest have two available domains (*as maps* is a plan for future updates of the app and it's going to create a map graph which will contain an additional z axis),
    * **Add** - a button which adds a graph to the list of graphs. The graphs have settings that were chosen using previous options

2. **Filters** - this panel has options which allow the user to filter out data sets. There are 7 available options:

    * **System** - a dropdown which filters the data sets depending on the isotopes used in the experiment (you can select multiple systems),
    * **Method** - ???
    * **Functional** - idk XD
    * **Ecm** - a slider for filtering the data sets depending on the energy of center of mass, you can select a range of energies that you want to be taken into account,
    * **Phase** - a slider for filtering the data sets depending on the phase, you can select a range here as well,
    * **b** - a slider for filtering the data sets depending on the quadrupol moment, you can select range here too,
    * **Apply** - applies the filters to all graphs.

3. **List of graphs** - when you first launch the application, this panel has only one **option**, which is **a dropdown whith a list of added graphs**. When you add a graph using graph picker, a new tag representing this graph appears in this dropdown. This option, instead of just showing added graphs, allows to delete graphs from the list as well. You can delete a single graph by clicking a cross next to the tag of corresponding graph or you can delete all graphs by clicking a cross in the right side of the dropdown.
Another options appear when you add graphs. Each graph has its own options which can modify its settings. Every graph has 6 options:

    * **Y axis** - radiobuttons for setting a scale of y axis, linear or logarithmic,
    * **X axis** - radiobuttons for setting a domain of x axis, it can be time, distance or maps (not available, yet),
    * **Colorscale** - a dropdown, which can be used to set a colorscale of the data displayed on the graph, this option contains a wide variety of colorscales to choose,
    * **Data** - a checkbox for setting wheather the data have to be displayed relatively to the first value in the series of measurements (first value is set to position 0 on y axis),
    * **Show** - checkboxes for setting wheather the data have to dispalyed as lines or as points, or both,
    * **Hovermode** - radiobuttons, which can be used to set the hovermode when you hover a cursor over the graph. *Closest* means the label, which will appear next to the cursor, will show a value of the nearest data series, and *x unified* means the label will show values of all data series at the chosen x position.

These were all the options you will find while using Lise Analyzer app.

Data
~~~~
The data used in the application are stored in a `TestData` directory in `.dat` files. Each file is named following a convention which looks like this:

**Convention**: `<System>_<Functional>_<?>_<?>_<Quadrupol moment>_<Phase>_<Energy>_out.dat`
**Example**: `56Ni+208Pb_SkM-star_gp233_gn260_b0_0PIPhase_248MeV_out.dat`

Each parameter has to be written following the rules listed below. Otherwise, the program will not recognise them properly.

* **System** - contains the names of isotopes. The name of the isotope starts with mass number of the isotope followed by symbol of this element. If the system contains diffrent isotopes, their names must be seperated using `+`. For example: `56Ni+208Pb` is a system which contains isotopes of nickel-56 and lead-208.
* **Functional** - ???
* **?** - even more ???
* **?** - `while True: print("?")`
* **Quadrupol moment** - the name starts with a value of quadrupol moment followed by letter b. The value must be a float. Instead of using `.`` use `-`` i.e. replace `0.5` with `0-5`.
* **Phase** - the value of phase is written as a fraction of pi in decimal. The value needs to be written in the same way as in quadrupol moment using `-` instead of `.` and than is followed by `PIPhase`.
* **Energy** - the energy of the system. It contains a value which is an integer followed by `MeV` unit.

Save
~~~~
Coming soon.
