import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import networkx as nx
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ABC_algorithm import abc, map_execution

class ABCPathFinder:
    def __init__(self):
        self.road_list, _ = map_execution.Map.returnMap()
        self.G = self.create_graph_from_matrix(self.road_list)
    
    def read_map_from_csv(self, file_path):
        data = pd.read_csv(file_path, header=None)
        return data.values

    def create_graph_from_matrix(self, matrix):
        G = nx.DiGraph()
        num_nodes = len(matrix)
        for i in range(num_nodes):
            G.add_node(i)
        for i in range(num_nodes):
            for j in range(num_nodes):
                if matrix[i][j] != 100000:  # 100000 represents infinity (no edge)
                    G.add_edge(i, j, weight=matrix[i][j])
        return G

    def find_path(self, start_node, end_node): # đã bỏ qua ràng buộc lập lịch 
        abc_instance = abc.ABC()
        dummy_time_start = 0
        best_solution = abc_instance.ABCAlgorithm(abc_instance, start_node, end_node, 0, dummy_time_start, ignore_scheduling=True)
        return best_solution.TravelledNode

    def animate_path(self, path):
        pos = nx.spring_layout(self.G)
        fig, ax = plt.subplots(figsize=(12, 8))
        
        car_img = plt.imread("car1.png")
        imagebox = OffsetImage(car_img, zoom=0.1)
        
        def update(num):
            ax.clear()
            nx.draw(self.G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold', ax=ax)
            edge_labels = nx.get_edge_attributes(self.G, 'weight')
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
            
            path_edges = list(zip(path[:num+1], path[1:num+2]))
            nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color='blue', width=2, ax=ax)
            
            if num < len(path):
                car_pos = pos[path[num]]
                ab = AnnotationBbox(imagebox, car_pos, frameon=False)
                ax.add_artist(ab)
            
            plt.title("AGV Moving Along the Path Found by ABC Algorithm")
        
        ani = FuncAnimation(fig, update, frames=len(path), repeat=False, interval=1000)
        plt.show()

if __name__ == "__main__":
    path_finder = ABCPathFinder()

    start_node = int(input("Enter the start node: "))
    end_node = int(input("Enter the end node: "))

    path = path_finder.find_path(start_node, end_node)

    if path:
        print("Path found by ABC algorithm:", path)
        print("Path cost:", sum(path_finder.G[u][v]['weight'] for u, v in zip(path[:-1], path[1:])))
        path_finder.animate_path(path)
    else:
        print("No path found.")