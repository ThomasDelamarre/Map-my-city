from graphviz import Digraph
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from labellines import labelLines, labelLine


def visualise_graph(edges, name):
    dot = Digraph(comment='Graph')
    for edge in edges.edges:
        dot.node(str(edge.node1.id), pos=str(edge.node1.lat) + "," + str(edge.node1.long) + "!")
        dot.node(str(edge.node2.id), pos=str(edge.node2.lat) + "," + str(edge.node2.long) + "!")
        if (edge.oneway):
            dot.edge(str(edge.node1.id), str(edge.node2.id), weight=str(edge.length), dir="forward", label=edge.name)
        else:
            dot.edge(str(edge.node1.id), str(edge.node2.id), weight=str(edge.length), dir="both", label=edge.name)

    dot.render('graphs_in_pdf/' + name + ".gv", view=True)


def visualise_circuit_with_plt(circuit, time_between_frames=0.5, legend=False):
    matplotlib.use('Tkagg')
    xmin, xmax, ymin, ymax = circuit.getExtremeLatLongs()
    xvals = []
    i = 0

    plt.xlim(left=xmin-0.0001, right=xmax+0.0001)
    plt.ylim(bottom=ymin-0.0001, top=ymax+0.0001)

    for edge in circuit.edges:
        i += 1
        plt.plot(np.array(edge.path.lats), np.array(edge.path.longs), label=str(i))

        if legend:
            s = 0
            for x in edge.path.lats:
                s += x
            xvals.append(s / edge.path.len)
            labelLine(plt.gca().get_lines()[-1], s / edge.path.len)

        plt.pause(time_between_frames)

    plt.show()





