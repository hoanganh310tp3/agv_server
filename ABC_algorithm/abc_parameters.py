class ABCSetting:
    # Number of Decision Path. Đây là số lượng các "Decision Path", có thể hiểu là số lượng các giải pháp quyết định ban đầu mà thuật toán sẽ thử nghiệm hoặc xử lý. Nó có thể tương ứng với số con ong hoặc số lượng giải pháp trong quần thể ban đầu.
    nCount = 20
    # nCount = 60
    # Number of Decision Variables. Đây là số lượng biến quyết định (Decision Variables) cho mỗi giải pháp. Mỗi giải pháp trong quần thể sẽ có 10 biến quyết định cần được tối ưu hóa. Ví dụ, nếu đang giải bài toán tối ưu hóa với nhiều biến, số lượng biến là 10.
    nVar = 10
    # nVar = 20
    # Maximum Number of Iterations. Đây là số lần lặp tối đa mà thuật toán ABC sẽ thực hiện trước khi dừng lại. Sau khi đạt đến số lần lặp này, thuật toán sẽ dừng ngay cả khi chưa tìm được giải pháp tối ưu.
    MaxIt = 50
    # MaxIt = 100
    #Population Size (Colony Size). Đây là kích thước quần thể (hay kích thước bầy ong) trong thuật toán ABC. Nó thể hiện tổng số con ong (giải pháp) trong quần thể mà thuật toán sẽ làm việc cùng một lúc.
    nPop = 50
    # nPop = 200
    # Number of Onlooker Bees. Đây là số lượng con ong định hướng (Onlooker Bees) trong thuật toán ABC. Con ong định hướng là một loại con ong đặc biệt, chịu trách nhiệm định hướng và lựa chọn các giải pháp tốt hơn trong quần thể.
    nOnlooker = nPop
    # Abandonment Limit Parameter (Trial Limit). Đây là giới hạn số lần thử không thành công cho mỗi giải pháp. Nếu một giải pháp không được cải thiện sau 10 lần thử, giải pháp đó sẽ bị "bỏ rơi", và một giải pháp mới (ong trinh sát) sẽ được tạo ra để thay thế.
    L = 10
    # Acceleration Coefficient Upper Bound. Đây là giới hạn trên của hệ số gia tốc (Acceleration Coefficient). Hệ số này có thể được dùng để điều chỉnh mức độ khám phá của ong trong không gian tìm kiếm. Giá trị lớn hơn của a có thể khiến ong di chuyển xa hơn khỏi các giải pháp hiện tại, tăng cường khám phá giải pháp mới.
    a = 1
    
#Định nghĩa các tham số cho thuật toán ABC.