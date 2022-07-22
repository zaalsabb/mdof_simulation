from sim_model import SimulationModel

materials = 'test/model/materials.csv'
sections = 'test/model/sections.csv'
nodes = 'test/model/nodes.csv'
elements = 'test/model/elements.csv'
constraints = 'test/model/constraints.csv'

# create opensees model
model = SimulationModel(materials, sections, nodes, elements, constraints)

# initialize analysis paremeters
model.set_analysis_parameters()

# test 4 load cases
# fx load case
load_case1 = 'test/load_cases/load_case1.csv'
output_disp1 = 'test/output_disp/output_disp1.csv'
model.apply_nodal_loads(load_case1)
ok = model.start_analysis()    
model.write_disps(output_disp1)
model.visualize(scale=100)    

# fy load case
load_case1 = 'test/load_cases/load_case2.csv'
output_disp1 = 'test/output_disp/output_disp2.csv'
model.apply_nodal_loads(load_case1)
ok = model.start_analysis()    
model.write_disps(output_disp1)
model.visualize(scale=100)    

# fz load case
load_case1 = 'test/load_cases/load_case3.csv'
output_disp1 = 'test/output_disp/output_disp3.csv'
model.apply_nodal_loads(load_case1)
ok = model.start_analysis()    
model.write_disps(output_disp1)
model.visualize(scale=100)    

# torsion load case
load_case1 = 'test/load_cases/load_case4.csv'
output_disp1 = 'test/output_disp/output_disp4.csv'
model.apply_nodal_loads(load_case1)
ok = model.start_analysis()    
model.write_disps(output_disp1)
model.visualize(scale=100)   