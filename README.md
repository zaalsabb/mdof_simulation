## Multi Degree Of Freedom (MDOF) Simulation 
Create MDOF structural frame models and analyze them using opensees in Python.
## Installation
Clone this package:
```
git clone https://github.com/zaalsabb/mdof_simulation.git
```
Install python requirements (Tested using Python `3.9`):
```
cd mdof_simulation
pip install -r requirements.txt
```

## Define Model
To create a 3d model, you must define your nodes, elements, materials, sections, and constraints as csv files. See the `test` folder for an example.

### Units
The model is agnostic to which units to use. However, you must stay consistent when you define your materials, section properties, element dimensions, and loads. The example in the `test` folder uses `N` & `m`. The modulus uses `N/m2`.

### Define Material
Define your materials, including young modulus and shear modulus.
|materials | E | G |
| --- | --- |--- |
|steel | 2.00E+11 | 7.69E+10|

### Define Sections
Define your sections, including area, section properties, and material name.
| sections | Area | Iz       | Iy       | J        | material |
|----------|------|----------|----------|----------|----------|
| I_beam   | 0.1  | 1.00E-04 | 1.00E-04 | 1.00E-06 | steel    |

### Define Nodes
Define node ids and 3d coordinates.
| node | x | y | z |
|------|---|---|---|
| 1    | 0 | 0 | 0 |
| 2    | 1 | 0 | 0 |
| 3    | 1 | 1 | 0 |
| 4    | 0 | 1 | 0 |
| 5    | 0 | 0 | 1 |
| 6    | 1 | 0 | 1 |
| 7    | 1 | 1 | 1 |
| 8    | 0 | 1 | 1 |

### Define Elements
Define element ids, the 2 nodes that form the element, section name, and the orientation of the element (defined by a vector parallel to the element's [local xz plane](https://opensees.berkeley.edu/wiki/index.php/Linear_Transformation).
| element | node1 | node2 | section | localxz_x | localxz_y | localxz_z |
|---------|-------|-------|---------|-----------|-----------|-----------|
| 1       | 1     | 5     | I_beam  | 0         | 1         | 0         |
| 2       | 2     | 6     | I_beam  | 0         | 1         | 0         |
| 3       | 3     | 7     | I_beam  | 0         | 1         | 0         |
| 4       | 4     | 8     | I_beam  | 0         | 1         | 0         |
| 5       | 5     | 6     | I_beam  | 0         | 1         | 0         |
| 6       | 6     | 7     | I_beam  | 1         | 0         | 0         |
| 7       | 7     | 8     | I_beam  | 0         | 1         | 0         |
| 8       | 8     | 5     | I_beam  | 1         | 0         | 0         |

### Define Constraints
Define your 6DOF constraints for some nodes. set it to `1` for fixed dof, and `0` for a free dof. The following example shows pinned constraints.
| node | x | y | z | rot_x | rot_y | rot_z |
|------|---|---|---|-------|-------|-------|
| 1    | 1 | 1 | 1 | 0     | 0     | 0     |
| 2    | 1 | 1 | 1 | 0     | 0     | 0     |
| 3    | 1 | 1 | 1 | 0     | 0     | 0     |
| 4    | 1 | 1 | 1 | 0     | 0     | 0     |

### Define a Load Case
Define your nodal loads.
| node | fx       | fy | fz |
|------|----------|----|----|
| 5    | 1.00E+03 | 0  | 0  |
| 6    | 1.00E+03 | 0  | 0  |
| 7    | 1.00E+03 | 0  | 0  |
| 8    | 1.00E+03 | 0  | 0  |

## Usage
You can either use this program from command line, or by importing this package and defining a `SimulationModel` class.

### Command line
```
python mdof_sim.py -m MATERIALS.csv -s SECTIONS.csv -n NODES.csv -e ELEMENTS.csv -c CONSTRAINTS.csv -l LOADS.csv [-o OUTPUT.csv]
```

### Importing `SimulationModel`
```python
from mdof_sim import SimulationModel

materials = 'materials.csv'
sections = 'sections.csv'
nodes = 'nodes.csv'
elements = 'elements.csv'
constraints = 'constraints.csv'
loads = 'loads.csv'
output = 'output.csv'

# create opensees model
model = SimulationModel(materials, sections, nodes, elements, constraints)

# initialize analysis paremeters
model.set_analysis_parameters()

# apply load and perform analysis
model.apply_nodal_loads(loads)
ok = model.start_analysis()    
model.write_disps(output)
model.visualize(scale=100) 
```

### Test
```
python test.py
```
