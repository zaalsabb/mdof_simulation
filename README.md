## Multi Degree Of Freedom (MDOF) Simulation 
Create MDOF structural frame models and analyze them using opensees in Python.
## Installation
Clone this package:
```
git clone https://github.com/zaalsabb/mdof_simulation.git
```
Install python requirements:
```
cd mdof_simulation
pip install -r requirements.txt
```
## Define Model
To create a 3d model, you must define your nodes, elements, materials, sections, and constraints as csv files. See the `test` folder for an example.

### Define Nodes
Define node ids and 3d coordinates.
| node  | x | y |z |
| --- | --- |--- |--- |
| 1	| 0	| 0	| 0 |
| 2	| 1	| 0	| 0 |
| 3	| 1	| 1	| 0 |

### Define Elements
Define element ids, the 2 nodes that form the element, section name, and the orientation of the element (defined by a vector parallel to the element's ![local xz plane](https://opensees.berkeley.edu/wiki/index.php/Linear_Transformation)).
| element  | node1 | node2 | section | localxz_x | localxz_y | localxz_z |
| --- | --- |--- |--- |--- |--- |--- |
| 1	| 1	| 5	| I_beam | 0 | 1 | 0 |
| 2	| 2	| 6	| I_beam | 0 | 1 | 0 |
| 3	| 3	| 7	| I_beam | 0 | 1 | 0 |

### Define Material
