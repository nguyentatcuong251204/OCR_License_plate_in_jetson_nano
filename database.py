import sqlite3
from datetime import datetime
import time

class Database:
    def __init__(self, db_name='Detect_lisence_plate.db'):
        # Khởi tạo đối tượng, mở kết nối đến cơ sở dữ liệu
        self.db_name = db_name
        self.cn = sqlite3.connect(db_name)
        self.c = self.cn.cursor()
        self.create_database()

    def create_database(self):
        # Tạo bảng trong cơ sở dữ liệu nếu chưa tồn tại
        sql_create_table1 = """
            CREATE TABLE IF NOT EXISTS Observe (
                carID INT,
                Lisence_plate TEXT,
                Status BIT,
                Time DATETIME,
                PRIMARY KEY (carID),  
                FOREIGN KEY (Time) REFERENCES number_Car(Time)
            )
        """

        sql_create_table2 = """
            CREATE TABLE IF NOT EXISTS number_Car (
                Time DATETIME PRIMARY KEY,
                number_Car INT
            )
        """

        self.c.execute(sql_create_table2)
        self.c.execute(sql_create_table1)
        self.cn.commit()

    def insert_data(self, carID, Lisence_plate, Status, number_Car):
        # Chèn dữ liệu vào cơ sở dữ liệu
        current_time = datetime.now()
        
        #carID = self.count_db() + 1
    
        # Status mặc định là 1
        #Status = 1

        sql_insert_table1 = """
            INSERT INTO Observe (carID, Lisence_plate, Status, Time) VALUES (?, ?, ?, ?)
        """
        sql_insert_table2 = """
            INSERT INTO number_Car (Time, number_Car) VALUES (?, ?)
        """
        self.c.execute(sql_insert_table1, (carID, Lisence_plate, Status, current_time))
        self.c.execute(sql_insert_table2, (current_time, number_Car))
        print("Insert successfully")
        self.cn.commit()

    def is_license_plate_in_database(self, Lisence_plate):
        # Kiểm tra xem biển số xe có trong cơ sở dữ liệu không
        sql_check_license_plate = """
            SELECT * FROM Observe WHERE Lisence_plate = ?
        """
        self.c.execute(sql_check_license_plate, (Lisence_plate,))
        result = self.c.fetchone()
        return result is not None

    def count_db(self):
        # Đếm số lượng dòng trong bảng Observe
        query = """
            SELECT COUNT(*) FROM Observe
        """
        self.c.execute(query)
        result = self.c.fetchone()
        return result[0] if result else 0

    def close_connection(self):
        # Đóng kết nối đến cơ sở dữ liệu
        self.c.close()
        self.cn.close()

# Sử dụng class LicensePlateDatabase
# db = Database()

# # Chèn dữ liệu vào cơ sở dữ liệu
# db.insert_data(carID=5, Lisence_plate="dBCs123", Status=1, number_Car=5)


# # Đóng kết nối đến cơ sở dữ liệu
# db.close_connection()
