import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ABC_algorithm import abc, map_execution, constrains, road, schedule

class ABCPathFinder:
    def __init__(self):
        self.road_list, _ = map_execution.Map.returnMap()
        self.G = self.create_graph_from_matrix(self.road_list)
    
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
    
    def find_paths_for_two_agvs(self, start_node1, end_node1, start_node2, end_node2):
        abc_instance1 = abc.ABC()
        abc_instance2 = abc.ABC()
        dummy_time_start = 0
        dummy_load_weight = 0

        try:
            path1 = abc_instance1.ABCAlgorithm(start_node1, end_node1, dummy_load_weight, dummy_time_start)
            path2 = abc_instance2.ABCAlgorithm(start_node2, end_node2, dummy_load_weight, dummy_time_start)

            collision, collision_index = self.check_collision(path1, path2)
            if collision:
                print("Collision detected! Finding alternative paths...")
                # Find alternative path for AGV 2
                path2 = self.find_alternative_path(start_node2, end_node2, path1)

            return path1, path2
        except Exception as e:
            print(f"Error finding paths: {e}")
            return None, None

    def find_alternative_path(self, start_node, end_node, other_path):
        abc_instance = abc.ABC()
        dummy_time_start = 0
        dummy_load_weight = 0

        # Add the other path to the schedule to avoid it
        schedule.Schedule.ListOfSchedule.append(schedule.Schedule(0, other_path, 0, dummy_time_start))

        alternative_path = abc_instance.ABCAlgorithm(start_node, end_node, dummy_load_weight, dummy_time_start)

        # Remove the temporary schedule
        schedule.Schedule.ListOfSchedule.pop()

        return alternative_path

   

    def apply_collision_constraint(self, path1, path2, collision_index):
        new_path1 = path1[:collision_index]
        new_path2 = path2[:collision_index]
        
        current_time = collision_index  # Assuming each step takes 1 time unit
        
        new_path1, _ = self.apply_constraint_to_path(path1, new_path1, collision_index, current_time)
        new_path2, _ = self.apply_constraint_to_path(path2, new_path2, collision_index, current_time)

        return new_path1, new_path2

    def apply_constraint_to_path(self, original_path, new_path, start_index, current_time):
        for i in range(start_index, len(original_path)):
            current_road = road.Road(original_path[i-1], original_path[i], self.G[original_path[i-1]][original_path[i]]['weight'])
            control_signal = constrains.Constrains.CollisionConstrain(current_time, current_road)
            
            if control_signal.Road.SecondNode != original_path[i]:
                alternative_path = nx.dijkstra_path(self.G, original_path[i-1], original_path[-1], weight='weight')
                new_path.extend(alternative_path[1:])
                break
            else:
                new_path.append(original_path[i])
                current_time += control_signal.Road.Distance / control_signal.Velocity
        
        return new_path, current_time

    def animate_two_paths(self, path1, path2):
        pos = nx.spring_layout(self.G)
        fig, ax = plt.subplots(figsize=(12, 8))
        
        car_img1 = plt.imread("car1.png")
        car_img2 = plt.imread("car2.png")
        imagebox1 = OffsetImage(car_img1, zoom=0.1)
        imagebox2 = OffsetImage(car_img2, zoom=0.1)
        
        def update(num):
            ax.clear()
            nx.draw(self.G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold', ax=ax)
            edge_labels = nx.get_edge_attributes(self.G, 'weight')
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
            
            path1_edges = list(zip(path1[:num+1], path1[1:num+2]))
            path2_edges = list(zip(path2[:num+1], path2[1:num+2]))
            nx.draw_networkx_edges(self.G, pos, edgelist=path1_edges, edge_color='blue', width=2, ax=ax)
            nx.draw_networkx_edges(self.G, pos, edgelist=path2_edges, edge_color='green', width=2, ax=ax)
            
            if num < len(path1):
                car1_pos = pos[path1[num]]
                ab1 = AnnotationBbox(imagebox1, car1_pos, frameon=False)
                ax.add_artist(ab1)
            
            if num < len(path2):
                car2_pos = pos[path2[num]]
                ab2 = AnnotationBbox(imagebox2, car2_pos, frameon=False)
                ax.add_artist(ab2)
            
            plt.title("Two AGVs Moving Along Their Paths")
        
        max_path_length = max(len(path1), len(path2))
        ani = FuncAnimation(fig, update, frames=max_path_length, repeat=False, interval=1000)
        plt.show()

if __name__ == "__main__":
    path_finder = ABCPathFinder()

    start_node1 = int(input("Enter the start node for AGV 1: "))
    end_node1 = int(input("Enter the end node for AGV 1: "))
    start_node2 = int(input("Enter the start node for AGV 2: "))
    end_node2 = int(input("Enter the end node for AGV 2: "))

    path1, path2 = path_finder.find_paths_for_two_agvs(start_node1, end_node1, start_node2, end_node2)

    if path1 is None or path2 is None:
        print("Unable to find valid paths for both AGVs. Exiting.")
    else:
        print("Path for AGV 1:", path1)
        print("Path for AGV 2:", path2)
        
        path_finder.animate_two_paths(path1, path2)