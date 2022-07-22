import argparse
import openseespy.opensees as ops
import pandas as pd
import matplotlib.pyplot as plt

class SimulationModel():
    def __init__(self, materials_f, sections_f, nodes_f, elements_f, constraints_f):

        self.nodes_csv = pd.read_csv(nodes_f)
        self.constraints_csv = pd.read_csv(constraints_f)
        self.elements_csv = pd.read_csv(elements_f)        

        self.nodes = dict()
        self.elements = dict()
        self.disps = dict()

        self.create_nodes()
        self.create_constraints()
        self.create_elements()                

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
            ops.element('elasticBeamColumn', elem_id, n1, n2, A, E, G, J, Iy, Iz, i, '-mass', mass)

    def write_disps(self, output_disp_f):
        with open(output_disp_f, 'w') as f:
            f.write("node, dx, dy, dz, rot_x, rot_y, rot_z \n")
            for node_id in self.nodes.keys():
                self.disps[node_id] = ops.nodeDisp(node_id,0)
                f.write("%i, %f, %f, %f, %f, %f, %f \n" % (node_id, *self.disps[node_id]))

            
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Create MDOF structural frame models and analyze them using opensees in Python.')
    parser.add_argument('-n','--nodes', help='filepath to nodes csv file', required=True)
    parser.add_argument('-e','--elements', help='filepath to elements csv file', required=True)
    parser.add_argument('-c','--constraints', help='filepath to constraints csv file', required=True)
    parser.add_argument('-o','--output', help='filepath to output displacements csv file', required=False, default='output_displacements.csv')

    args = vars(parser.parse_args())

    NStory = args['NStory']
    NBayX = args['NBayX']
    NBayZ = args['NBayZ']

    LCol = args['LCol']
    LBeam = args['LBeam']
    LGird = args['LGird']
    GJ = args['GJ']

    output = args['output']    

    # create opensees model
    model = SimulationModel(nodes, elements, constraints)
    
           