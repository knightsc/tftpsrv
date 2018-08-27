import networkx as nx
import pydot

graph = nx.DiGraph()


def main():
    global graph
    
    with open('tftpsrv.text.fixed.txt') as f:
        lines = f.readlines()
        
    graph_function(lines, 'strcpy')
    #graph_function(lines, 'FillScreen')
    #graph_function(lines, 'sprintf')

    pydot_graph = nx.to_pydot(graph)
    pydot_graph.write_png('unsafe.png')

    
def graph_function(lines, function):
    global graph
    
    for i in range(len(lines)):
        if function in lines[i] and not lines[i].startswith('00') and 'lui	gp,' not in lines[i]:
            # Back up to the function prolog
            j = i - 1
            while 'lui	gp,' not in lines[j] and j > 0:
                j -= 1
                
            if j != 0:
                caller = lines[j][0:8].strip()
	        if lines[j-1].startswith('00'):
                    caller = lines[j-1].strip()[10:-2]

                if caller != function:
    	            graph.add_edge(caller, function)
    	            print(caller + '->' + function)
    	        
    	            if caller != 'main':
                        graph_function(lines, caller)


if __name__ == "__main__":
    main()
