## Multi Degree Of Freedom (MDOF) Simulation 
Create MDOF structural frame models and analyze them using OpenSees.

## OpenSees Installation
Install [tcl](http://www.tcl.tk/software/tcltk/) on your machine to use OpenSees (>3.2.2).

The Windows executable files for OpenSees are contained in the `OpenSees` folder in this repo. If you are Linux then consider building OpenSees from source using this [guide](https://www.researchgate.net/post/How-to-install-opensees-in-UBUNTU).

### Inputs
The `Inputs.tcl` file contains the basic input parameters to run the model, including frame geometry and ground motion parameters. The ground motion input file is contained in the `GMfiles` folder.

### Units
The model by default uses imperial units. However, this can be easily be changed through the `LibUnits.tcl` by defining metric variables for conversions.

### Running the Program

To run the program, run the following commands:
```
cd tcl
..\OpenSees\bin\OpenSees.exe runSteelAnalysis.tcl
```

You have the option of running the files `runSteelAnalysis.tcl` or `runRCAnalysis.tcl`. Each one runs the steel or reinforced concrete examples from `Ex8.genericFrame3D` examples, which use inelastic sections to simulate permanent earthquake damage.

Other parameters can be changed in the files inside the `tcl` folder.

### Outputs
The outputs produced by the program include `nodes.txt`, `elements.txt`, and `disp.out` (can be read as a text file).

`nodes.txt`: defines node geometry, `node_id position_x position_y position_z`.
`elements.txt`: defines element connectivity, `element_id node_1 node_2`.
`disp.out`: defines node displacements at each timestep: 
```
time node1_disp_x node1_disp_y node1_disp_z node2_disp_x node2_disp_y node2_disp_z ....
```

The node displacements in `disp.out` don't have the node ids, but they are ordered in ascending order in terms of node ids. Every three columns contain the `x`, `y`, and `z` displacements for each node.