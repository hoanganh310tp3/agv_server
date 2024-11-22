from django.utils import timezone
import datetime
import time

from agv_management.models import agv_data, agv_identify 

# Kiểm tra xem một AGV có đang hoạt động hay không
def is_agv_active(carID):
    AGVisActive = agv_identify.objects.filter(agv_id = carID, is_active = True, is_connected = True).exists()
    return AGVisActive

# Trả về danh sách các AGV đang hoạt động
# Mỗi phần tử trong danh sách chứa [ID của AGV]
# Sắp xếp theo ID của AGV
def list_active_AGV():
    listOfActiveAGV = []
    AGVisActive = agv_identify.objects.all().filter(is_active = True, is_connected = True).order_by('agv_id') 
    for eachQuery in AGVisActive:
        listOfActiveAGV.append([eachQuery.agv_id, eachQuery.parking_lot])
    return listOfActiveAGV

# Nếu AGV không gửi dữ liệu trong 300 giây (5 phút), đánh dấu là mất kết nối
def check_connect_AGV():
    now = time.mktime(datetime.datetime.now().timetuple)

    listOfActiveAGV = list_active_AGV()
    for eachCar in listOfActiveAGV:
        query = agv_data.objects.all().filter(agv_identify__car_id = eachCar[0]).last()
        dataTime = time.mktime(query.time_stamp.timetuple())
        if (now - dataTime) > 300:
            agv_identify.objects.filter(agv_id = eachCar[0]).update(is_connected = False)

# Nếu AGV có car_state = 11 (có thể là trạng thái lỗi), đánh dấu là mất kết nối
def check_connect_AGV():
    listOfActiveAGV = list_active_AGV()
    for eachCar in listOfActiveAGV:
        query = agv_data.objects.all().filter(agv_identify__car_id = eachCar[0], car_state = 11).last()
        if query:
            agv_identify.objects.filter(agv_id = eachCar[0]).update(is_connected = False)
    pass
# may be needed to fix

# Trả về danh sách tất cả các ID của AGV trong hệ thống
def list_AGV():
    listOfAGV = []
    AGVisActive = agv_identify.objects.all().order_by('agv_id')
    for eachQuery in AGVisActive:
        listOfAGV.append(eachQuery.agv_id)
    return listOfAGV


# Trả về danh sách các AGV đang sẵn sàng để sử dụng
# Chỉ lấy các AGV có trạng thái là 1 hoặc 7 (có thể là trạng thái sẵn sàng/rảnh)
# Mỗi phần tử chứa [ID của AGV, điểm waypoint trước đó, điểm waypoint tiếp theo]
def list_available_AGV():
    listOfAvailableAGV = []
    listOfActiveAGV = list_active_AGV()
    for eachCar in listOfActiveAGV:
        AGVisAvailable = agv_data.objects.all().filter(car_state__in = [1, 7], agv_id = eachCar).last()
        if AGVisAvailable:
            listOfAvailableAGV.append([AGVisAvailable.car_id.agv_id, AGVisAvailable.previous_waypoint, AGVisAvailable.next_waypoint])
    return listOfAvailableAGV

# Tự động vô hiệu hóa các AGV không hoạt động
# Nếu AGV không gửi dữ liệu trong 180 giây (3 phút), đánh dấu là không hoạt động
def deactivate_AGV():
    timeNow = timezone.now()
    listOfActiveAGV = list_active_AGV()
    for eachCar in listOfActiveAGV:
        query = agv_data.objects.all().filter(agv_identify__car_id = eachCar).last()
        if query and (timeNow - query.time_stamp).total_seconds() >= 180:
            agv_identify.objects.filter(agv_id = eachCar).update(is_busy = False)
