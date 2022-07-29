import numpy as np
import sys
import matplotlib.pyplot as plt

def process_disp(*args):
    
    disp_path = args[0]
    nodes_path = args[1]
    elements_path = args[2]
    out_path = args[3]

    disp_out = np.loadtxt(disp_path)
    nodes = np.loadtxt(nodes_path)
    elements = np.loadtxt(elements_path)
    
    disp_last = disp_out[-1,1:]
    disp_last = disp_last.reshape(-1,6)

    nodes_id = nodes[:,0].reshape(-1,1)
    nodes_id = np.array(nodes_id,dtype=np.int64)

    out = np.hstack([nodes_id,disp_last])
    np.savetxt(out_path,out,fmt='%.18f')

    visualize(nodes,elements,disp_last)    

def visualize(nodes,elements,disps,scale=100):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    nodes_dict = {}
    disps_dict = {}
    for i,n in enumerate(nodes):
        id = int(n[0])
        disps_dict[id] = disps[i,1:]
        nodes_dict[id] = nodes[i,1:]

    for elem in elements:
        n1 = nodes_dict[int(elem[1])]
        n2 = nodes_dict[int(elem[2])]
        d1 = disps_dict[int(elem[1])]
        d2 = disps_dict[int(elem[2])]

        xline1 = [n1[0], n2[0]]
        zline1 = [n1[1], n2[1]]
        yline1 = [n1[2], n2[2]]

        ax.plot3D(xline1, yline1, zline1, 'gray')

        xline2 = [n1[0]+scale*d1[0], n2[0]+scale*d2[0]]
        zline2 = [n1[1]+scale*d1[1], n2[1]+scale*d2[1]]
        yline2 = [n1[2]+scale*d1[2], n2[2]+scale*d2[2]]

        ax.plot3D(xline2, yline2, zline2, 'red')  

    plt.show()    


if __name__ == '__main__':
    process_disp(*sys.argv[1:])