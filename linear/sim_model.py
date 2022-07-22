import argparse
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

        self.materials = dict()
        self.sections = dict()
        self.nodes = dict()
        self.elements = dict()
        self.disps = dict()
        self.load_pattern = 0
        self.g = 9.807

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
            density = row['density']
            name = row['materials']
            self.materials[name] = [E, G, density]

    def create_sections(self):
       for i,row in self.sections_csv.iterrows():
            name = row['sections']
            A = row['Area']
            Iz = row['Iz']
            Iy = row['Iy']
            J = row['J']
            mat = row['material']
            E, G, density = self.materials[mat]
            mass = density * A
            self.sections[name] = [A,Iz,Iy,J,E,G,mass]

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
            A,Iz,Iy,J,E,G,mass = self.sections[section]

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
    
    parser = argparse.ArgumentParser(description='Create MDOF structural frame models and analyze them using opensees in Python.')
    parser.add_argument('-m','--materials', help='filepath to materials csv file', required=True)
    parser.add_argument('-s','--sections', help='filepath to materials csv file', required=True)
    parser.add_argument('-n','--nodes', help='filepath to nodes csv file', required=True)
    parser.add_argument('-e','--elements', help='filepath to elements csv file', required=True)
    parser.add_argument('-c','--constraints', help='filepath to constraints csv file', required=True)
    parser.add_argument('-l','--loads', help='filepath to loads csv file', required=True)
    parser.add_argument('-o','--output', help='filepath to output displacements csv file', required=False, default='output_displacements.csv')

    args = vars(parser.parse_args())

    materials = args['materials']
    sections = args['sections']
    nodes = args['nodes']
    elements = args['elements']
    constraints = args['constraints']
    loads = args['loads']
    output = args['output']    

    # create opensees model
    model = SimulationModel(materials, sections, nodes, elements, constraints)
    
    # initialize analysis paremeters
    model.set_analysis_parameters()

    # apply load and perform analysis
    model.apply_nodal_loads(loads)
    ok = model.start_analysis()    
    model.write_disps(output)
    model.visualize(scale=100)             