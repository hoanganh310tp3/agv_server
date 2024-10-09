import sys
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import networkx as nx
import numpy as np
import matplotlib.collections as mc
from matplotlib.table import Table
# hoạt động tốt nhưng chưa mô phỏng được thời gian 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ABC_algorithm import map_execution, convert, agv_car, abc, constrains, control_signal, requirement, road

class AGVPathSimulatorWithCollision:
    def __init__(self):
        self.road_list, self.direction_list = map_execution.Map.returnMap()
        self.G = self.create_graph_from_matrix(self.road_list)
        self.agv1_schedule = self.get_user_input_schedule("AGV1")
        self.agv2_schedule = self.get_user_input_schedule("AGV2")
        self.abc_algorithm = abc.ABC()
        self.agv1 = agv_car.AGVCar("AGV1")
        self.agv2 = agv_car.AGVCar("AGV2")

        # Log để kiểm tra road_list
        print("Sample distances from road_list:")
        for i in range(min(5, len(self.road_list))):
            for j in range(min(5, len(self.road_list[i]))):
                if self.road_list[i][j] != 100000:  # Assuming 100000 is used for non-connected nodes
                    print(f"Distance from node {i} to node {j}: {self.road_list[i][j]} meters")

    def create_graph_from_matrix(self, matrix):
        G = nx.DiGraph()
        num_nodes = len(matrix)
        for i in range(num_nodes):
            G.add_node(i)
        for i in range(num_nodes):
            for j in range(num_nodes):
                if matrix[i][j] != 100000:
                    G.add_edge(i, j, weight=matrix[i][j])
        return G

    def get_user_input_schedule(self, agv_name):
        print(f"Enter schedule data for {agv_name}:")
        schedule_data = {}
        schedule_data['Order'] = input("Order: ")
        schedule_data['CarId'] = int(input("CarId: "))
        schedule_data['WeightLoad'] = float(input("Weight Load: "))
        schedule_data['TimeStart'] = input("TimeStart (HH:MM:SS): ")
        schedule_data['Inbound'] = int(input("Inbound (starting node): "))
        schedule_data['Outbound'] = int(input("Outbound (destination node): "))
        return schedule_data

    def animate_agv_movements(self):
        pos = nx.spring_layout(self.G)
        fig = plt.figure(figsize=(12, 10))
        gs = fig.add_gridspec(3, 1, height_ratios=[0.1, 4, 1])
        ax_title = fig.add_subplot(gs[0])
        ax = fig.add_subplot(gs[1])
        ax_table = fig.add_subplot(gs[2])

        ax_title.axis('off')
        ax_title.set_title("Two AGVs Moving Along Their Paths", fontsize=16, fontweight='bold')

        car_img1 = plt.imread("car1.png")
        car_img2 = plt.imread("car2.png")
        imagebox1 = OffsetImage(car_img1, zoom=0.1)
        imagebox2 = OffsetImage(car_img2, zoom=0.06)

        start_time = min(convert.Convert.TimeToTimeStamp(self.agv1_schedule['TimeStart']),
                         convert.Convert.TimeToTimeStamp(self.agv2_schedule['TimeStart']))

        self.agv1_path = self.find_new_path(self.agv1_schedule['Inbound'], self.agv1_schedule['Outbound'], 
                                       start_time, self.agv1_schedule['WeightLoad'])
        self.agv2_path = self.find_new_path(self.agv2_schedule['Inbound'], self.agv2_schedule['Outbound'], 
                                       start_time, self.agv2_schedule['WeightLoad'])

        end_time = max(start_time + convert.Convert.returnScheduleToTravellingTime(self.agv1_path.ListOfControlSignal),
                       start_time + convert.Convert.returnScheduleToTravellingTime(self.agv2_path.ListOfControlSignal))

        def update(frame):
            current_time = start_time + frame
            ax.clear()
            ax_table.clear()
            
            # Vẽ đồ thị mà không có các cạnh có trọng số 0
            edges = [(u, v) for (u, v, d) in self.G.edges(data=True) if d['weight'] != 0]
            nx.draw_networkx_nodes(self.G, pos, node_color='lightblue', node_size=500, ax=ax)
            nx.draw_networkx_edges(self.G, pos, edgelist=edges, ax=ax, edge_color='gray', alpha=0.5)
            nx.draw_networkx_labels(self.G, pos, font_size=10, font_weight='bold', ax=ax)
            
            # Vẽ nhãn cạnh chỉ cho các cạnh có trọng số khác 0
            edge_labels = {(u, v): d['weight'] for (u, v, d) in self.G.edges(data=True) if d['weight'] != 0}
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
            
            agv1_pos, agv1_velocity = self.get_agv_position_and_velocity(self.agv1_path, current_time - start_time)
            agv2_pos, agv2_velocity = self.get_agv_position_and_velocity(self.agv2_path, current_time - start_time)
            
            # Vẽ đường đi của AGV1
            agv1_path_edges = self.get_travelled_path(self.agv1_path, current_time - start_time)
            nx.draw_networkx_edges(self.G, pos, edgelist=agv1_path_edges, edge_color='blue', width=2, ax=ax)
            
            # Vẽ đường đi của AGV2
            agv2_path_edges = self.get_travelled_path(self.agv2_path, current_time - start_time)
            nx.draw_networkx_edges(self.G, pos, edgelist=agv2_path_edges, edge_color='green', width=2, ax=ax)
            
            if self.check_collision(agv1_pos, agv2_pos):
                print(f"Collision detected at time {convert.Convert.returnTimeStampToTime(current_time)}")
                self.handle_collision(current_time, agv1_pos, agv2_pos)
            
            ab1 = AnnotationBbox(imagebox1, pos[agv1_pos[0]], frameon=False)
            ax.add_artist(ab1)
            ax.text(pos[agv1_pos[0]][0], pos[agv1_pos[0]][1] + 0.1, f"AGV1: {agv1_velocity:.2f} m/s", ha='center', va='bottom')
            
            ab2 = AnnotationBbox(imagebox2, pos[agv2_pos[0]], frameon=False)
            ax.add_artist(ab2)
            ax.text(pos[agv2_pos[0]][0], pos[agv2_pos[0]][1] - 0.1, f"AGV2: {agv2_velocity:.2f} m/s", ha='center', va='top')
            
            ax.set_title(f"Time: {convert.Convert.returnTimeStampToTime(current_time)}")

            # Tạo bảng hiển thị vận tốc
            table_data = [
                ['AGV1', 'AGV2'],
                [f'{agv1_velocity:.2f} m/s', f'{agv2_velocity:.2f} m/s']
            ]
            table = ax_table.table(cellText=table_data, loc='center', cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(12)
            table.scale(1, 1.5)
            ax_table.axis('off')
            ax_table.set_title('AGV Velocities')

        frames = int(end_time - start_time)
        ani = FuncAnimation(fig, update, frames=frames, repeat=False, interval=100)
        plt.tight_layout()
        plt.show()

    def handle_collision(self, current_time, agv1_pos, agv2_pos):
        # Apply collision constraints
        road1 = self.get_current_road(agv1_pos)
        road2 = self.get_current_road(agv2_pos)
        
        control_signal1 = constrains.Constrains.CollisionConstrain(current_time, road1)
        control_signal2 = constrains.Constrains.CollisionConstrain(current_time, road2)
        
        # Update paths with new control signals
        self.update_agv_path(self.agv1_path, control_signal1, current_time)
        self.update_agv_path(self.agv2_path, control_signal2, current_time)

    def get_current_road(self, agv_pos):
        return road.Road(agv_pos[0], agv_pos[1], self.calculate_real_distance(agv_pos[0], agv_pos[1]))

    def update_agv_path(self, agv_path, new_control_signal, current_time):
        # Find the index where the new control signal should be inserted
        insert_index = 0
        for i, signal in enumerate(agv_path.ListOfControlSignal):
            if current_time < self.get_signal_end_time(signal, current_time):
                insert_index = i
                break
        
        # Insert the new control signal and adjust the rest of the path
        agv_path.ListOfControlSignal.insert(insert_index, new_control_signal)
        self.adjust_remaining_path(agv_path, insert_index + 1, current_time)

    def get_signal_end_time(self, signal, start_time):
        return start_time + signal.Road.Distance / signal.Velocity

    def adjust_remaining_path(self, agv_path, start_index, current_time):
        for i in range(start_index, len(agv_path.ListOfControlSignal)):
            signal = agv_path.ListOfControlSignal[i]
            new_signal = control_signal.ControlSignal(signal.Road)
            new_signal.Velocity = min(new_signal.Velocity, agv_car.AGVCar.MaxVelocity)
            new_signal.Velocity = max(new_signal.Velocity, agv_car.AGVCar.MinAccelaration)
            agv_path.ListOfControlSignal[i] = new_signal

    def get_agv_position_and_velocity(self, path, elapsed_time):
        total_time = 0
        for signal in path.ListOfControlSignal:
            travel_time = signal.Road.Distance / signal.Velocity
            if total_time + travel_time > elapsed_time:
                progress = (elapsed_time - total_time) / travel_time
                return (signal.Road.FirstNode, signal.Road.SecondNode, progress), signal.Velocity
            total_time += travel_time
        return (path.ListOfControlSignal[-1].Road.SecondNode, path.ListOfControlSignal[-1].Road.SecondNode, 1), path.ListOfControlSignal[-1].Velocity

    def check_collision(self, pos1, pos2):
        if pos1[0] == pos2[0] and pos1[1] == pos2[1]:
            return True
        if pos1[0] == pos2[1] and pos1[1] == pos2[0]:
            return True
        return False

    def find_new_path(self, start_node, end_node, current_time, load_weight):
        req = requirement.Requirement(TimeStart=current_time, Inbound=start_node, Outbound=end_node, Weight=load_weight)
        new_path = self.abc_algorithm.ABCAlgorithm(self.abc_algorithm, req.Inbound, req.Outbound, req.LoadWeight, convert.Convert.TimeToTimeStamp(req.TimeStart))
        
        # Apply collision constraints and adjust velocities
        adjusted_control_signals = []
        for signal in new_path.ListOfControlSignal:
            adjusted_signal = constrains.Constrains.CollisionConstrain(current_time, signal.Road)
            adjusted_control_signals.append(adjusted_signal)
        
        new_path.ListOfControlSignal = adjusted_control_signals
        return new_path

    def calculate_real_distance(self, node1, node2):
        distance = self.road_list[node1][node2]
        print(f"Calculated distance from node {node1} to node {node2}: {distance} meters")
        return distance

    def get_travelled_path(self, path, elapsed_time):
        travelled_edges = []
        total_time = 0
        for signal in path.ListOfControlSignal:
            travel_time = signal.Road.Distance / signal.Velocity
            if total_time + travel_time <= elapsed_time:
                travelled_edges.append((signal.Road.FirstNode, signal.Road.SecondNode))
            elif total_time < elapsed_time:
                travelled_edges.append((signal.Road.FirstNode, signal.Road.SecondNode))
                break
            else:
                break
            total_time += travel_time
        return travelled_edges

if __name__ == "__main__":
    simulator = AGVPathSimulatorWithCollision()
    simulator.animate_agv_movements()