import sys
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import networkx as nx
import numpy as np
import matplotlib.collections as mc
from matplotlib.table import Table

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ABC_algorithm import map_execution, convert, agv_car, abc, constrains, control_signal, requirement, road

class AGVPathSimulatorWithCollision:
    def __init__(self):
        # Purpose: Initialize the AGV path simulator with collision detection
        self.road_list, self.direction_list = map_execution.Map.returnMap()
        self.G = self.create_graph_from_matrix(self.road_list)
        self.agv1_schedule = self.get_user_input_schedule("AGV1")
        self.agv2_schedule = self.get_user_input_schedule("AGV2")
        self.abc_algorithm = abc.ABC()
        self.agv1 = agv_car.AGVCar("AGV1")
        self.agv2 = agv_car.AGVCar("AGV2")
        self.agv1_visited_nodes = []
        self.agv2_visited_nodes = []
        self.agv1_current_velocity = 0
        self.agv2_current_velocity = 0
        self.agv1_path_history = []
        self.agv2_path_history = []

        # Log để kiểm tra road_list
        print("Sample distances from road_list:")
        for i in range(min(5, len(self.road_list))):
            for j in range(min(5, len(self.road_list[i]))):
                if self.road_list[i][j] != 100000:  # Assuming 100000 is used for non-connected nodes
                    print(f"Distance from node {i} to node {j}: {self.road_list[i][j]} meters")

    def create_graph_from_matrix(self, matrix):
        # Purpose: Create a graph representation from the given matrix
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
        # Purpose: Get user input for AGV schedule
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
        # Purpose: Animate the movements of AGVs on the graph
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
        
        agv1_start_time = convert.Convert.TimeToTimeStamp(self.agv1_schedule['TimeStart'])
        agv2_start_time = convert.Convert.TimeToTimeStamp(self.agv2_schedule['TimeStart'])

        self.agv1_path = self.find_new_path(self.agv1_schedule['Inbound'], self.agv1_schedule['Outbound'], 
                                       agv1_start_time, self.agv1_schedule['WeightLoad'])
        self.agv2_path = self.find_new_path(self.agv2_schedule['Inbound'], self.agv2_schedule['Outbound'], 
                                       agv2_start_time, self.agv2_schedule['WeightLoad'])

        end_time = max(agv1_start_time + convert.Convert.returnScheduleToTravellingTime(self.agv1_path.ListOfControlSignal),
                       agv2_start_time + convert.Convert.returnScheduleToTravellingTime(self.agv2_path.ListOfControlSignal))

        def update(frame):
            # Purpose: Update the animation frame
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
            
            agv1_pos, self.agv1_current_velocity = self.get_agv_position_and_velocity(self.agv1_path, current_time - agv1_start_time, self.agv1_current_velocity)
            agv2_pos, self.agv2_current_velocity = self.get_agv_position_and_velocity(self.agv2_path, current_time - agv2_start_time, self.agv2_current_velocity)
            
            # Cập nhật lịch sử đường đi
            if current_time >= agv1_start_time and agv1_pos[0] != self.agv1_path_history[-1] if self.agv1_path_history else True:
                self.agv1_path_history.append(agv1_pos[0])
            if current_time >= agv2_start_time and agv2_pos[0] != self.agv2_path_history[-1] if self.agv2_path_history else True:
                self.agv2_path_history.append(agv2_pos[0])
            
            # Vẽ đường đi của AGV1
            if current_time >= agv1_start_time:
                agv1_path_edges = self.get_travelled_path(self.agv1_path, current_time - agv1_start_time)
                nx.draw_networkx_edges(self.G, pos, edgelist=agv1_path_edges, edge_color='blue', width=2, ax=ax)
                ab1 = AnnotationBbox(imagebox1, pos[agv1_pos[0]], frameon=False)
                ax.add_artist(ab1)
                ax.text(pos[agv1_pos[0]][0], pos[agv1_pos[0]][1] + 0.1, f"AGV1: {self.agv1_current_velocity:.2f} m/s", ha='center', va='bottom')
            
            # Vẽ đường đi của AGV2
            if current_time >= agv2_start_time:
                agv2_path_edges = self.get_travelled_path(self.agv2_path, current_time - agv2_start_time)
                nx.draw_networkx_edges(self.G, pos, edgelist=agv2_path_edges, edge_color='green', width=2, ax=ax)
                ab2 = AnnotationBbox(imagebox2, pos[agv2_pos[0]], frameon=False)
                ax.add_artist(ab2)
                ax.text(pos[agv2_pos[0]][0], pos[agv2_pos[0]][1] - 0.1, f"AGV2: {self.agv2_current_velocity:.2f} m/s", ha='center', va='top')
            
            if current_time >= agv1_start_time and current_time >= agv2_start_time:
                if self.check_collision(agv1_pos, agv2_pos):
                    print(f"Collision detected at time {convert.Convert.returnTimeStampToTime(current_time)}")
                    self.handle_collision(current_time, agv1_pos, agv2_pos)
            
            ax.set_title(f"Time: {convert.Convert.returnTimeStampToTime(current_time)}")

            # Tạo bảng hiển thị vận tốc và lịch sử đường đi
            table_data = [
                ['AGV1 Velocity', 'AGV2 Velocity', 'AGV1 Path History', 'AGV2 Path History'],
                [f'{self.agv1_current_velocity:.2f} m/s' if current_time >= agv1_start_time else 'Not started',
                 f'{self.agv2_current_velocity:.2f} m/s' if current_time >= agv2_start_time else 'Not started',
                 ' -> '.join(map(str, self.agv1_path_history)),
                 ' -> '.join(map(str, self.agv2_path_history))]
            ]
            table = ax_table.table(cellText=table_data, loc='center', cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 1.5)
            for (row, col), cell in table.get_celld().items():
                if row == 0:
                    cell.set_text_props(fontweight='bold')
            ax_table.axis('off')
            ax_table.set_title('AGV Information')

        frames = int(end_time - start_time)
        ani = FuncAnimation(fig, update, frames=frames, repeat=False, interval=100)
        plt.tight_layout()
        plt.show()

    def handle_collision(self, current_time, agv1_pos, agv2_pos):
        # Purpose: Handle collision between AGVs more effectively
        road1 = self.get_current_road(agv1_pos)
        road2 = self.get_current_road(agv2_pos)
        
        # Apply collision constraints with more consideration
        control_signal1 = constrains.Constrains.CollisionConstrain(current_time, road1, ignore_scheduling=False)
        control_signal2 = constrains.Constrains.CollisionConstrain(current_time, road2, ignore_scheduling=False)
        
        # Adjust velocities based on the constraints
        self.adjust_agv_path(self.agv1_path, control_signal1, current_time)
        self.adjust_agv_path(self.agv2_path, control_signal2, current_time)

    def adjust_agv_path(self, agv_path, new_control_signal, current_time):
        # Purpose: Adjust AGV path considering new control signal
        insert_index = self.find_insert_index(agv_path, current_time)
        
        # If the new control signal suggests a different road, plan a new path
        if new_control_signal.Road.FirstNode == 0 and new_control_signal.Road.SecondNode == 0:
            new_path = self.find_new_path(agv_path.ListOfControlSignal[insert_index].Road.FirstNode,
                                          agv_path.ListOfControlSignal[-1].Road.SecondNode,
                                          current_time,
                                          agv_path.LoadWeight)
            agv_path.ListOfControlSignal = agv_path.ListOfControlSignal[:insert_index] + new_path.ListOfControlSignal
        else:
            # Adjust velocity of the current segment
            agv_path.ListOfControlSignal[insert_index].Velocity = new_control_signal.Velocity
        
        # Adjust remaining path
        self.adjust_remaining_path(agv_path, insert_index + 1, current_time)

    def find_insert_index(self, agv_path, current_time):
        # Purpose: Find the correct index to insert or modify the control signal
        total_time = 0
        for i, signal in enumerate(agv_path.ListOfControlSignal):
            travel_time = signal.Road.Distance / signal.Velocity
            if total_time + travel_time > current_time:
                return i
            total_time += travel_time
        return len(agv_path.ListOfControlSignal) - 1

    def adjust_remaining_path(self, agv_path, start_index, current_time):
        # Purpose: Adjust the remaining path after a collision or constraint application
        for i in range(start_index, len(agv_path.ListOfControlSignal)):
            signal = agv_path.ListOfControlSignal[i]
            new_signal = constrains.Constrains.CollisionConstrain(current_time, signal.Road, ignore_scheduling=False)
            agv_path.ListOfControlSignal[i] = new_signal
            current_time += signal.Road.Distance / new_signal.Velocity

    def get_current_road(self, agv_pos):
        # Purpose: Get the current road for an AGV position
        return road.Road(agv_pos[0], agv_pos[1], self.calculate_real_distance(agv_pos[0], agv_pos[1]))

    def get_agv_position_and_velocity(self, path, elapsed_time, current_velocity):
        # Purpose: Calculate the current position and velocity of an AGV
        if elapsed_time < 0:
            return (path.ListOfControlSignal[0].Road.FirstNode, path.ListOfControlSignal[0].Road.FirstNode, 0), 0
        
        total_time = 0
        distance_travelled = 0
        for signal in path.ListOfControlSignal:
            acceleration = min(agv_car.AGVCar.MaxAccelaration, 
                               max(0, (agv_car.AGVCar.MaxVelocity - current_velocity) / agv_car.AGVCar.delayTime))
            
            if acceleration == 0 or current_velocity >= agv_car.AGVCar.MaxVelocity:
                # AGV is already at max speed
                time_at_max_speed = signal.Road.Distance / agv_car.AGVCar.MaxVelocity
                if total_time + time_at_max_speed > elapsed_time:
                    t = elapsed_time - total_time
                    distance = agv_car.AGVCar.MaxVelocity * t
                    progress = (distance_travelled + distance) / signal.Road.Distance
                    return (signal.Road.FirstNode, signal.Road.SecondNode, progress), agv_car.AGVCar.MaxVelocity
                total_time += time_at_max_speed
                distance_travelled += signal.Road.Distance
                current_velocity = agv_car.AGVCar.MaxVelocity
                continue

            time_to_max_speed = (agv_car.AGVCar.MaxVelocity - current_velocity) / acceleration
            
            if total_time + time_to_max_speed > elapsed_time:
                # AGV is still accelerating
                t = elapsed_time - total_time
                new_velocity = min(agv_car.AGVCar.MaxVelocity, current_velocity + acceleration * t)
                distance = current_velocity * t + 0.5 * acceleration * t * t
                progress = (distance_travelled + distance) / signal.Road.Distance
                return (signal.Road.FirstNode, signal.Road.SecondNode, progress), new_velocity
            
            distance_at_max_speed = signal.Road.Distance - (current_velocity * time_to_max_speed + 0.5 * acceleration * time_to_max_speed * time_to_max_speed)
            time_at_max_speed = distance_at_max_speed / agv_car.AGVCar.MaxVelocity
            
            if total_time + time_to_max_speed + time_at_max_speed > elapsed_time:
                # AGV reaches max speed during this segment
                t = elapsed_time - (total_time + time_to_max_speed)
                distance = (current_velocity * time_to_max_speed + 0.5 * acceleration * time_to_max_speed * time_to_max_speed) + agv_car.AGVCar.MaxVelocity * t
                progress = (distance_travelled + distance) / signal.Road.Distance
                return (signal.Road.FirstNode, signal.Road.SecondNode, progress), agv_car.AGVCar.MaxVelocity
            
            total_time += time_to_max_speed + time_at_max_speed
            distance_travelled += signal.Road.Distance
            current_velocity = agv_car.AGVCar.MaxVelocity
        
        return (path.ListOfControlSignal[-1].Road.SecondNode, path.ListOfControlSignal[-1].Road.SecondNode, 1), agv_car.AGVCar.MaxVelocity

    def check_collision(self, pos1, pos2):
        # Purpose: Check if there's a collision between two AGV positions
        if pos1[0] == pos2[0] and pos1[1] == pos2[1]:
            return True
        if pos1[0] == pos2[1] and pos1[1] == pos2[0]:
            return True
        return False

    def find_new_path(self, start_node, end_node, current_time, load_weight):
        # Purpose: Find a new path for an AGV
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
        # Purpose: Calculate the real distance between two nodes. đoạn code này có thể bỏ qua vì nó chỉ là check đơn vị đường đi
        distance = self.road_list[node1][node2]
        print(f"Calculated distance from node {node1} to node {node2}: {distance} meters")
        return distance

    def get_travelled_path(self, path, elapsed_time):
        # Purpose: Get the travelled path of an AGV
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