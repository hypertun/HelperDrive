
from datetime import date


class Helper:
    def __init__(self, name, code, status, nationality, medical, staff_Id):
        self.name = name
        self.id = -1
        self.dob = date.today()
        self.arrivalDate = date.today()
        self.status = status
        self.nationality = nationality
        self.code = code
        self.flightNo = ""
        self.fin = ""
        self.medical = medical
        self.staffId = staff_Id
        self.createdAt = date.today()
        self.updatedAt = date.today()

    def add(self, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO helpers (name,code,status,nationality,medical,staff_id) VALUES(%s,%s,%s,%s,%s,%s)",
                       (self.name, self.code, self.status, self.nationality, self.medical, self.staffId))
        conn.commit()
        cursor.close()

    def delete(self, conn):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM helpers WHERE id=%s",self.id)
        conn.commit()
        cursor.close()
