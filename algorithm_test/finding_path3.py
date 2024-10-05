import sys
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import networkx as nx
from datetime import datetime, timedelta
import numpy as np


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ABC_algorithm.abc_parameters import ABCSetting
from ABC_algorithm import map_execution, convert, agv_car, abc, constrains, requirement, control_signal, road
class AGVPathSimulator:
    def __init__(self):
        self.road_list, self.direction_list = map_execution.Map.returnMap()
        self.G = self.create_graph_from_matrix(self.road_list)
        self.agv1_schedule = self.get_user_input_schedule("AGV1")
        self.agv2_schedule = self.get_user_input_schedule("AGV2")
        self.max_velocity = agv_car.AGVCar.MaxVelocity
        self.abc_algorithm = abc.ABC()
        self.max_iterations = ABCSetting.MaxIt 

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
        # schedule_data['Name'] = input("Name of goods: ")
        schedule_data['CarId'] = int(input("CarId: "))
        schedule_data['WeightLoad'] = float(input("Weight Load: "))
        schedule_data['TimeStart'] = input("TimeStart (HH:MM:SS): ")
        schedule_data['Inbound'] = int(input("Inbound (starting node): "))
        schedule_data['Outbound'] = int(input("Outbound (destination node): "))
        return schedule_data
    
    
    def create_default_schedule(self):
        return pd.DataFrame({
            'TimeStart': ['00:00:00'],
            'TimeEnd': ['00:01:00'],
            'Inbound': [0],
            'Outbound': [1],
            'WeightLoad': [0.0],
            'ControlSignal': ['01(1.0 m)(0.2 m/s)']
        })
    
    def calculate_end_time(self, start_time, control_signal):
        start_timestamp = convert.Convert.TimeToTimeStamp(start_time)
        total_time = sum(float(segment.split('(')[1].split(' ')[0]) / float(segment.split('(')[2].split(' ')[0])
                         for segment in control_signal.split(','))
        end_timestamp = start_timestamp + total_time
        return convert.Convert.returnTimeStampToTime(end_timestamp)
    
    
    def get_agv_position(self, path, elapsed_time):
        total_time = 0
        for signal in path.ListOfControlSignal:
            travel_time = signal.Road.Distance / signal.Velocity
            if total_time + travel_time > elapsed_time:
                progress = (elapsed_time - total_time) / travel_time
                return signal.Road.FirstNode, signal.Road.SecondNode, progress
            total_time += travel_time
        return path.ListOfControlSignal[-1].Road.SecondNode, path.ListOfControlSignal[-1].Road.SecondNode, 1
    
    def find_new_path(self, start_node, end_node, current_time, load_weight):
        req = requirement.Requirement(TimeStart=current_time, Inbound=start_node, Outbound=end_node, Weight=load_weight)
        
        for _ in range(self.max_iterations):
            new_path = self.abc_algorithm.CreateInitialPopulation(self.abc_algorithm, req.Inbound, req.Outbound, req.LoadWeight, convert.Convert.TimeToTimeStamp(req.TimeStart), ignore_scheduling=True)

            if new_path is not None and new_path.ListOfControlSignal:
                # Sử dụng control_signal để tạo và kiểm tra các tín hiệu điều khiển
                control_signals = control_signal.ControlSignal.returnListOfControlSignal(current_time, new_path.ListOfNode)
                
                # Kiểm tra xem có tín hiệu điều khiển hợp lệ không
                if all(cs.Velocity > 0 for cs in control_signals):
                    new_path.ListOfControlSignal = control_signals
                    return new_path

        print(f"No valid path found from {start_node} to {end_node} after {self.max_iterations} attempts")
        return None

    def parse_control_signal(self, control_signal):
        parsed_signals = []
        signals = control_signal.split(',')
        for signal in signals:
            parts = signal.split('(')
            nodes = parts[0]
            distance = float(parts[1].split(')')[0])
            velocity = float(parts[2].split(')')[0])
            parsed_signals.append((nodes, distance, velocity))
        return parsed_signals
    
    def animate_agv_movements(self):
        pos = nx.spring_layout(self.G)
        fig, ax = plt.subplots(figsize=(12, 8))

        car_img1 = plt.imread("car1.png")
        car_img2 = plt.imread("car2.png")
        imagebox1 = OffsetImage(car_img1, zoom=0.1)
        imagebox2 = OffsetImage(car_img2, zoom=0.1)

        start_time = min(convert.Convert.TimeToTimeStamp(self.agv1_schedule['TimeStart']),
                         convert.Convert.TimeToTimeStamp(self.agv2_schedule['TimeStart']))

        self.agv1_path = self.find_new_path(self.agv1_schedule['Inbound'], self.agv1_schedule['Outbound'], start_time, self.agv1_schedule['WeightLoad'])
        self.agv2_path = self.find_new_path(self.agv2_schedule['Inbound'], self.agv2_schedule['Outbound'], start_time, self.agv2_schedule['WeightLoad'])

        if self.agv1_path is None or self.agv2_path is None:
            print("Unable to find valid paths for both AGVs. Exiting.")
            return

        # Kiểm tra xem ListOfControlSignal có hợp lệ không
        if not self.agv1_path.ListOfControlSignal or not self.agv2_path.ListOfControlSignal:
            print("One or both AGV paths have empty or invalid control signal lists. Exiting.")
            return

        end_time = max(start_time + convert.Convert.returnScheduleToTravellingTime(self.agv1_path.ListOfControlSignal),
                       start_time + convert.Convert.returnScheduleToTravellingTime(self.agv2_path.ListOfControlSignal))


        def update(frame):
        
            current_time = start_time + frame
            ax.clear()
            nx.draw(self.G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold', ax=ax)
            edge_labels = nx.get_edge_attributes(self.G, 'weight')
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
            
            agv1_pos = self.get_agv_position(self.agv1_path, current_time - start_time)
            agv2_pos = self.get_agv_position(self.agv2_path, current_time - start_time)
            
            if self.check_collision_risk(agv1_pos, agv2_pos, current_time):
                print(f"Collision risk detected at time {convert.Convert.returnTimeStampToTime(current_time)}")
            self.agv1_path = self.find_new_path(agv1_pos[0], self.agv1_schedule['Outbound'], current_time, self.agv1_schedule['WeightLoad'])
            self.agv2_path = self.find_new_path(agv2_pos[0], self.agv2_schedule['Outbound'], current_time, self.agv2_schedule['WeightLoad'])
            
            ab1 = AnnotationBbox(imagebox1, pos[agv1_pos[0]], frameon=False)
            ax.add_artist(ab1)
            
            ab2 = AnnotationBbox(imagebox2, pos[agv2_pos[0]], frameon=False)
            ax.add_artist(ab2)
            
            plt.title(f"Two AGVs Moving Along Their Paths - Time: {convert.Convert.returnTimeStampToTime(current_time)}")

        frames = int(end_time - start_time)
        ani = FuncAnimation(fig, update, frames=frames, repeat=False, interval=100)
        plt.show()
    def check_collision_risk(self, pos1, pos2, current_time):
        road1 = road.Road(pos1[0], pos1[1], self.road_list[pos1[0]][pos1[1]])
        road2 = road.Road(pos2[0], pos2[1], self.road_list[pos2[0]][pos2[1]])
        
        control_signal1 = constrains.Constrains.CollisionConstrain(current_time, road1)
        control_signal2 = constrains.Constrains.CollisionConstrain(current_time, road2)
        
        return control_signal1.Road.Distance == 100000 or control_signal2.Road.Distance == 100000 or \
               control_signal1.Velocity < self.max_velocity or control_signal2.Velocity < self.max_velocity
    
    
    

    def update_schedule(self, old_schedule, new_path, current_time):
        new_schedule = old_schedule.copy()
        new_schedule['ControlSignal'] = self.path_to_control_signal(new_path)
        new_schedule['TimeStart'] = convert.Convert.returnTimeStampToTime(current_time)
        new_schedule['TimeEnd'] = convert.Convert.returnTimeStampToTime(current_time + convert.Convert.returnScheduleToTravellingTime(new_path.ListOfControlSignal))
        return new_schedule

    

if __name__ == "__main__":
    simulator = AGVPathSimulator()
    simulator.animate_agv_movements()