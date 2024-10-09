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
            
            # Vẽ đồ thị mà không có các cạnh có trọng số 0
            edges = [(u, v) for (u, v, d) in self.G.edges(data=True) if d['weight'] != 0]
            nx.draw_networkx_nodes(self.G, pos, node_color='lightblue', node_size=500, ax=ax)
            nx.draw_networkx_edges(self.G, pos, edgelist=edges, ax=ax, edge_color='gray', alpha=0.5)
            nx.draw_networkx_labels(self.G, pos, font_size=10, font_weight='bold', ax=ax)
            
            # Vẽ nhãn cạnh chỉ cho các cạnh có trọng số khác 0
            edge_labels = {(u, v): d['weight'] for (u, v, d) in self.G.edges(data=True) if d['weight'] != 0}
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
            # Vẽ đường đi hiện tại
            current_path = path[:num+1]
            current_edges = list(zip(current_path, current_path[1:]))
            nx.draw_networkx_edges(self.G, pos, edgelist=current_edges, edge_color='blue', width=2, ax=ax)
            
            # Vẽ xe
            if num < len(path):
                car_pos = pos[path[num]]
                ab = AnnotationBbox(imagebox, car_pos, frameon=False)
                ax.add_artist(ab)
            
            plt.title("AGV Moving Along the Path Found by ABC Algorithm")
            ax.set_axis_off()
        
        ani = FuncAnimation(fig, update, frames=len(path), repeat=False, interval=1000)
        plt.show()

if __name__ == "__main__":
    path_finder = ABCPathFinder()

    start_node = int(input("Enter the start node: "))
    end_node = int(input("Enter the end node: "))

    path = path_finder.find_path(start_node, end_node)

    if path:
        print("Path found by ABC algorithm:", path)
        # Thêm các dòng debug này trước đoạn mã gây ra lỗi
        print("Debug: Path =", path)
        for u, v in zip(path[:-1], path[1:]):
            print(f"Debug: Edge ({u}, {v}) weight =", path_finder.G[u][v]['weight'], type(path_finder.G[u][v]['weight']))

        # Sau đó, tính toán và in chi phí đường đi
        path_cost = sum(float(path_finder.G[u][v]['weight']) for u, v in zip(path[:-1], path[1:]))
        print("Path cost:", path_cost)
        path_finder.animate_path(path)
    else:
        print("No path found.")