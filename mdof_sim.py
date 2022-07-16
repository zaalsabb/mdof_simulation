import openseespy.opensees as ops
import pandas as pd
import matplotlib.pyplot as plt

class SimulationModel():
    def __init__(self, materials_f, sections_f, nodes_f, elements_f, constraints_f):
        self.materials_csv = pd.read_csv(materials_f)
        self.sections_csv = pd.read_csv(sections_f)
        self.nodes_csv = pd.read_csv(nodes_f)
        self.constraints_csv = pd.read_csv(constraints_f)
        self.elements_csv = pd.read_csv(elements_f)        

        self.materials_E = dict()
        self.materials_G = dict()
        self.sections = dict()
        self.nodes = dict()
        self.elements = dict()
        self.disps = dict()
        self.load_pattern = 0

        self.initialize_model()
        self.create_materials()
        self.create_sections()
        self.create_nodes()
        self.create_constraints()
        self.create_elements()        
        
    def initialize_model(self):
        ops.wipe()
        ops.model('Basic', '-ndm', 3,'-ndf',6)

    def set_analysis_parameters(self):
        ops.system('SparseSYM')
        ops.numberer('RCM')
        ops.timeSeries('Linear', 1)
        ops.constraints('Plain')
        ops.integrator('LoadControl', 1.0)
        ops.test('NormDispIncr', 1e-5, 100)
        ops.algorithm('Newton')
        ops.analysis('Static')        

    def create_materials(self):
        for i,row in self.materials_csv.iterrows():
            E = row['E']
            G = row['G']
            name = row['materials']
            self.materials_E[name] = E
            self.materials_G[name] = G

    def create_sections(self):
       for i,row in self.sections_csv.iterrows():
            name = row['sections']
            A = row['Area']
            Iz = row['Iz']
            Iy = row['Iy']
            J = row['J']
            mat = row['material']
            E = self.materials_E[mat]
            G = self.materials_G[mat]
            self.sections[name] = [A,Iz,Iy,J,E,G]

    def create_nodes(self):
       for i,row in self.nodes_csv.iterrows():
            node_id = int(row['node'])
            x = float(row['x'])
            y = float(row['y'])
            z = float(row['z'])
            self.nodes[node_id] = [x,y,z]
            ops.node(node_id, x, y, z)

    def create_constraints(self):
       for i,row in self.constraints_csv.iterrows():
            node_id = int(row['node'])
            x = int(row['x'])
            y = int(row['y'])
            z = int(row['z'])
            rot_x = int(row['rot_x'])
            rot_y = int(row['rot_y'])
            rot_z = int(row['rot_z'])
            ops.fix(node_id, *[x, y, z, rot_x, rot_y, rot_z])

    def create_elements(self):
       for i,row in self.elements_csv.iterrows():
            elem_id = int(row['element'])
            n1 = int(row['node1'])
            n2 = int(row['node2'])
            section = row['section']
            l_x = float(row['localxz_x'])
            l_y = float(row['localxz_y'])
            l_z = float(row['localxz_z'])
            self.elements[elem_id] = [n1,n2]
            A,Iz,Iy,J,E,G = self.sections[section]

            ops.geomTransf('Linear', i, l_x, l_y, l_z)
            ops.element('elasticBeamColumn', elem_id, n1, n2, A, E, G, J, Iy, Iz, i)

    def apply_nodal_loads(self, nodal_loads_f):  
        if self.load_pattern > 0:
            ops.remove('loadPattern',self.load_pattern)   
            ops.reset()   
        self.load_pattern +=1
        nodal_loads_csv = pd.read_csv(nodal_loads_f)      
        ops.pattern('Plain', self.load_pattern, 1)
        for i,row in nodal_loads_csv.iterrows():
            node_id = int(row['node'])
            fx = float(row['fx'])
            fy = float(row['fy'])
            fz = float(row['fz'])
            ops.load(node_id, fx, fy, fz, 0., 0., 0.)
         
    def start_analysis(self):
        ok = ops.analyze(1)
        return ok

    def write_disps(self, output_disp_f):
        with open(output_disp_f, 'w') as f:
            f.write("node, dx, dy, dz, rot_x, rot_y, rot_z \n")
            for node_id in self.nodes.keys():
                self.disps[node_id] = ops.nodeDisp(node_id,0)
                f.write("%i, %f, %f, %f, %f, %f, %f \n" % (node_id, *self.disps[node_id]))

    def visualize(self, scale=1):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        for elem_id in self.elements.keys():
            n1 = self.nodes[self.elements[elem_id][0]]
            n2 = self.nodes[self.elements[elem_id][1]]
            d1 = self.disps[self.elements[elem_id][0]]
            d2 = self.disps[self.elements[elem_id][1]]

            xline1 = [n1[0], n2[0]]
            yline1 = [n1[1], n2[1]]
            zline1 = [n1[2], n2[2]]

            ax.plot3D(xline1, yline1, zline1, 'gray')

            xline2 = [n1[0]+scale*d1[0], n2[0]+scale*d2[0]]
            yline2 = [n1[1]+scale*d1[1], n2[1]+scale*d2[1]]
            zline2 = [n1[2]+scale*d1[2], n2[2]+scale*d2[2]]

            ax.plot3D(xline2, yline2, zline2, 'red')  

        plt.show()
            
if __name__ == '__main__':
    
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