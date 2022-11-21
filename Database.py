"""
    @author Dimos Retsidis

    class SudentDatabase used by main
"""


#import the module to use database
import sqlite3


class StudentsDatabase:

    """
    __init__ method creates the database we need for the app
    also creates table "students" to store data that represent:
        id : (int) unique id for every student
        name : (string) name of the student
        phone_num : (string) student's phone number
        price_per_hour : (int) amount that professor be paid per hour
        paid : (int) total amount professor have recieved
        lessons : (string) all lessons that have be done written in spesific format
                           DAY DATE START_TIME-END_TIME
        comments : (string) any comment that professor want to write for student
    """
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS students(
            id Integer Primary Key,
            name text,
            phone_num text,
            price_per_hour Int,
            paid Int,
            lessons text,
            comments text
        )
        """
        #lessons Integer,
        self.cur.execute(sql)
        self.con.commit()

        
    # add -> method to add a student in the database
    def add(self , name , phone_num , price_per_hour , paid , lessons , comments ):
        self.cur.execute("insert into students values (Null,?,?,?,?,?,?)",
                         (name, phone_num,price_per_hour , paid , lessons ,comments))
        self.con.commit()

    # all_students -> method to return all database's records
    def all_students(self):
        self.cur.execute("SELECT * from students")
        rows = self.cur.fetchall()
        # print(rows)
        return rows

    # remove -> method to delete a student based in the id
    def remove(self, id):
        self.cur.execute("delete from students where id=?", (id,))
        self.con.commit()

    # update -> method to update a student's record based in the id
    def update(self, id , name , phone_num , price_per_hour , paid ,  lessons , comments):
        self.cur.execute(
            "update students set name=?, phone_num=?,price_per_hour=?, paid=?, lessons=? , comments =? where id=?",
            ( name, phone_num,price_per_hour , paid , lessons, comments, id))
        self.con.commit()

