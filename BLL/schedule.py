import DTO.schedule
import DTO.agv_car
import BLL.convert
import DTO.agv_car
import BLL.abc
import BLL.requirement
import BLL.car_selection
import BLL.schedule
import logging

# Fixed parking spots for each AGV
PARKING_SPOTS = {
    1: 0,  # AGV 1 parks at spot 0
    2: 1,  # AGV 2 parks at spot 1
    3: 2   # AGV 3 parks at spot 2
}

class Schedule:
    @staticmethod
    def returnSchedule(Requirement, SelectedCarTrip, SelectedTransportingTrip):
        """
        Creates a schedule for a specific requirement using the selected car and route.
        Also includes the return path to parking spot.
        
        Args:
            Requirement: The delivery requirement to be scheduled
            SelectedCarTrip: The selected car and its trip to the pickup point
            SelectedTransportingTrip: The transport trip from pickup to delivery
            
        Returns:
            Schedule: The created schedule object, or None if an error occurred
        """
        logger = logging.getLogger(__name__)
        
        try:
            # Validate input parameters
            if Requirement is None:
                logger.error("Cannot create schedule: Requirement is None")
                return None
            
            if SelectedCarTrip is None:
                logger.error(f"Cannot create schedule for Order #{Requirement.Order}: SelectedCarTrip is None")
                return None
            
            if SelectedTransportingTrip is None:
                logger.error(f"Cannot create schedule for Order #{Requirement.Order}: SelectedTransportingTrip is None")
                return None
            
            if not hasattr(SelectedCarTrip, 'Car') or SelectedCarTrip.Car is None:
                logger.error(f"Cannot create schedule for Order #{Requirement.Order}: No car assigned")
                return None
            
            # Create a new schedule object
            Schedule = DTO.schedule.Schedule()
            
            # Set basic properties from the requirement
            Schedule.Name = Requirement.Name
            Schedule.Order = Requirement.Order
            Schedule.Date = Requirement.Date
            Schedule.Car = SelectedCarTrip.Car
            Schedule.Car.Location = Requirement.Outbound
            Schedule.Inbound = Requirement.Inbound
            Schedule.Outbound = Requirement.Outbound
            Schedule.TimeStart = Requirement.TimeStart
            Schedule.LoadWeight = Requirement.LoadWeight
            Schedule.LoadAmount = Requirement.LoadAmount
            
            # Get the AGV's assigned parking spot
            agv_id = int(Schedule.Car.CarId)
            parking_spot = PARKING_SPOTS.get(agv_id)
            
            if parking_spot is None:
                logger.error(f"No parking spot assigned for AGV {agv_id}")
                return None

            # Find path to parking spot using ABC algorithm
            NewABC = BLL.abc.ABC()
            parking_return_trip = NewABC.ABCAlgorithm(
                NewABC,
                Requirement.Outbound,  # From delivery point
                parking_spot,          # To parking spot
                0,                     # No load when returning
                0                      # Time doesn't matter for parking return
            )

            if not parking_return_trip:
                logger.error(f"Could not find path to parking spot {parking_spot} for AGV {agv_id}")
                return None

            # Combine all control signals: car trip + transport trip + parking return trip
            Schedule.ListOfControlSignal = (
                SelectedCarTrip.Cost.ListOfControlSignal + 
                SelectedTransportingTrip.ListOfControlSignal +
                parking_return_trip.ListOfControlSignal
            )
            
            # Generate control signal format for MQTT
            try:
                Schedule.ControlSignal = Schedule.list_control_signal()
            except Exception as cs_error:
                logger.error(f"Error generating control signals for Order #{Requirement.Order}: {cs_error}")
                return None
            
            # Calculate end time including return to parking
            try:
                TimeStamp = BLL.convert.Convert.TimeToTimeStamp(Schedule.TimeStart)
                TravelTime = BLL.convert.Convert.returnScheduleToTravellingTime(Schedule.ListOfControlSignal)
                Schedule.TimeEnd = BLL.convert.Convert.returnTimeStampToTime(TimeStamp + TravelTime + DTO.agv_car.AGVCar.delayTime)
            except Exception as time_error:
                logger.error(f"Error calculating end time for Order #{Requirement.Order}: {time_error}")
                return None
            
            # Calculate total energy and distance including return to parking
            try:
                Schedule.TotalEnergy = round(
                    SelectedCarTrip.Cost.CostValue + 
                    SelectedTransportingTrip.CostValue + 
                    parking_return_trip.CostValue, 
                    3
                )
                Schedule.TotalDistance = Schedule.get_total_distance()
            except Exception as calc_error:
                logger.error(f"Error calculating energy/distance for Order #{Requirement.Order}: {calc_error}")
                return None
            
            # Update battery capacity
            try:
                MaxBatteryCapacity = DTO.agv_car.AGVCar.MaxBatteryCapacity
                CurrentBattery = float(Schedule.Car.BatteryCapacity)
                EnergyUsed = float(Schedule.TotalEnergy)
                Schedule.Car.BatteryCapacity = round((CurrentBattery * MaxBatteryCapacity/100 - EnergyUsed) * 100/MaxBatteryCapacity, 2)
                Schedule.BatteryCapacity = Schedule.Car.BatteryCapacity
            except Exception as battery_error:
                logger.error(f"Error calculating battery for Order #{Requirement.Order}: {battery_error}")
                # Continue anyway since battery calculation is not critical
            
            # Add this schedule to the car's schedule list
            if hasattr(Schedule.Car, 'ScheduleList'):
                Schedule.Car.ScheduleList.append(Schedule)
            
            logger.info(f"Successfully created schedule for Order #{Requirement.Order} with return to parking spot {parking_spot}")
            return Schedule
        
        except Exception as e:
            logger.error(f"Error creating schedule for {getattr(Requirement, 'Order', 'unknown')}: {e}")
            return None

    @staticmethod
    def returnListOfSchedule():
        """
        Generates and returns a list of schedules for all requirements.
        Each requirement represents a delivery order that needs to be scheduled.
        
        Returns:
            list: The list of generated schedules
        """
        logger = logging.getLogger(__name__)
        
        try:
            # Get the list of requirements (orders to be scheduled)
            ListOfRequirement = BLL.requirement.Requirement.ReadTimeTable()
            if not ListOfRequirement:
                logger.warning("No requirements found to schedule")
                return []
            
            logger.info(f"Found {len(ListOfRequirement)} requirements to schedule")
            
            # Initialize ABC algorithm and cars
            NewABC = BLL.abc.ABC()
            BLL.car_selection.CarSelection.InitialCar()
            
            # Process each requirement
            for EachRequirement in ListOfRequirement:
                try:
                    logger.info(f"Processing requirement for Order #{EachRequirement.Order}")
                    
                    # Select car for this requirement
                    SelectedCarTrip = BLL.car_selection.CarSelection.returnSelectedCar(EachRequirement)
                    if not SelectedCarTrip:
                        logger.warning(f"No suitable car found for Order #{EachRequirement.Order}")
                        continue
                    
                    # Calculate start time with any needed adjustments
                    TimeStart = BLL.convert.Convert.TimeToTimeStamp(EachRequirement.TimeStart)
                    if len(SelectedCarTrip.Cost.ListOfControlSignal) > 1:
                        TimeStart = BLL.convert.Convert.returnScheduleToTravellingTime(SelectedCarTrip.Cost.ListOfControlSignal) + TimeStart
                    
                    # Find the optimal route for this requirement
                    NewABC = BLL.abc.ABC()  # Create a fresh ABC algorithm instance
                    SelectedTransportingTrip = NewABC.ABCAlgorithm(
                        NewABC,
                        EachRequirement.Inbound,
                        EachRequirement.Outbound,
                        EachRequirement.LoadWeight,
                        TimeStart
                    )
                    
                    if not SelectedTransportingTrip:
                        logger.warning(f"Could not find a valid route for Order #{EachRequirement.Order}")
                        continue
                    
                    # Create the schedule
                    Schedule = BLL.schedule.Schedule.returnSchedule(
                        EachRequirement,
                        SelectedCarTrip,
                        SelectedTransportingTrip
                    )
                    
                    # Only add valid schedules to the list
                    if Schedule is not None:
                        DTO.schedule.Schedule.ListOfSchedule.append(Schedule)
                        logger.info(f"Successfully created schedule for Order #{EachRequirement.Order}")
                    else:
                        logger.warning(f"Failed to create schedule for Order #{EachRequirement.Order}")
                    
                except Exception as req_error:
                    # Log the error but continue processing other requirements
                    logger.error(f"Error processing requirement {getattr(EachRequirement, 'Order', 'unknown')}: {req_error}")
                    continue
                
            logger.info(f"Successfully created {len(DTO.schedule.Schedule.ListOfSchedule)} schedules")
            return DTO.schedule.Schedule.ListOfSchedule
        
        except Exception as e:
            logger.error(f"Error in returnListOfSchedule: {e}")
            return []

    @staticmethod
    def return_to_lot(startNode, stopNode, loadWeight, timeStart):
        NewABC = BLL.abc.ABC()
        Route=list()
        Route = NewABC.ABCAlgorithm(NewABC, startNode, stopNode, loadWeight, timeStart)
        return Route
