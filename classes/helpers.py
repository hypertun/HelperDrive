
from datetime import date


def getAllHelpers(conn):
    helperList = []
    cursor = conn.cursor()
    cursor.execute("SELECT * from helpers")
    data = cursor.fetchall()
    for eachHelper in data:
        id, name, code, dob, arrival_Date, flight_No, status, nationality, fin, medical, staff_id, created_at, updated_at = eachHelper
        newHelper = Helper(name,
                           code,
                           status,
                           nationality,
                           medical,
                           staff_id,
                           )
        newHelper.id = id
        newHelper.date_of_birth = dob
        newHelper.arrival_date = arrival_Date
        newHelper.flight_no = flight_No
        newHelper.fin = fin
        newHelper.created_at = created_at
        newHelper.updated_at = updated_at
        helperList.append(newHelper)

    cursor.close()
    return helperList


class Helper:
    def __init__(self, name, code, status, nationality, medical, staff_Id):
        self.name = name
        self.id = -1
        self.date_of_birth = date.today().strftime("%Y-%m-%d")
        self.arrival_date = date.today().strftime("%Y-%m-%dT%H:%M")
        self.status = status
        self.nationality = nationality
        self.code = code
        self.flight_no = ""
        self.fin = ""
        self.medical = medical
        self.staff_id = staff_Id
        self.created_at = date.today().strftime("%Y-%m-%dT%H:%M")
        self.updated_at = date.today().strftime("%Y-%m-%dT%H:%M")

    def add(self, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO helpers (name,code,status,nationality,medical,staff_id) VALUES(%s,%s,%s,%s,%s,%s)",
                       (self.name, self.code, self.status, self.nationality, self.medical, self.staff_id))
        conn.commit()
        cursor.close()

    def delete(self, conn):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM helpers WHERE id=%s", self.id)
        conn.commit()
        cursor.close()

    def edit(self, conn):
        cursor = conn.cursor()
        update = "UPDATE helpers SET "
        arguments = ()
        for key, value in self.__dict__.items():
            if key == "id":
                continue
            if value != "":
                update = update + key + "=%s,"
                arguments = arguments + (value,)
        # remove comma
        update = update[:-1] + " WHERE id=%s"
        arguments = arguments + (self.id,)
        cursor.execute(update, arguments)
        conn.commit()
        cursor.close()

    def get(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * from helpers WHERE id=%s", self.id)
        row = cursor.fetchone()
        if row is None:
            return None

        id, name, code, dob, arrival_Date, flight_No, status, nationality, fin, medical, staff_id, created_at, updated_at = row
        newHelper = Helper(name,
                           code,
                           status,
                           nationality,
                           medical,
                           staff_id,
                           )
        newHelper.id = id
        newHelper.date_of_birth = dob
        newHelper.arrival_date = arrival_Date
        newHelper.flight_no = flight_No
        newHelper.fin = fin
        newHelper.created_at = created_at
        newHelper.updated_at = updated_at

        cursor.close()
        return newHelper
