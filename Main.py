from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import SlideTransition
# from database import Database
import sqlite3
store_id = "" #declear global vairable
# Window.size=(350,600)

class Database():
    def __init__(self):
        # self.con.sqlite3.connect("db.db")
        self.con = sqlite3.connect('Student_record.db')
        self.cursor = self.con.cursor()
        self.create_student_table()
        self.create_sign_up_table()
    # ********************************* for register ************************************
    # create  register_table to signup people
    def create_sign_up_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS register_table(
                id integer PRIMARY KEY AUTOINCREMENT, 
                first_name varchar(50),
                last_name varchar(50),
                mobile_no  varchar(50),
                cnic varchar(15),
                email varchar(50),
                passward
            )
            """
        )
        self.con.commit()


    # "to isert values in register_table table "
    def create_sign_record(self, first_name,last_name, mobile_no, cnic, email, passward):
        # Ensure the values match the table structure
        self.cursor.execute(
            """
            INSERT INTO register_table(first_name, last_name, mobile_no, cnic, email, passward)
            VALUES(?,?,?,?,?,?)
            """,
            (first_name, last_name, mobile_no, cnic, email, passward)
        )
        self.con.commit()
        

    def get_register_record(self):
        first_row = (self.cursor.execute("SELECT* FROM register_table WHERE id = 1 ").fetchall())
        return first_row

    def forget_password(self, first_name, last_name, mobile_no, cnic, email, passward):
        self.cursor.execute(
            """
            UPDATE register_table
            SET 
                first_name = ?,
                last_name = ?,
                mobile_no = ?,
                cnic = ?,
                email = ?,
                passward = ?
            WHERE id = 1
            """,
            (first_name, last_name, mobile_no, cnic, email, passward)
        )
        self.con.commit()
        print("First row updated successfully.")
    

    # ****************************************** en of te register record  ************************************


    
    # ****************************************** code for student data table ************************************
    # create student table
    def create_student_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS student_table(id integer PRIMARY KEY AUTOINCREMENT, first_name varchar(50), last_name varchar(50), f_name varchar(50), cnic integer, mobile_no integer, class_name varchar(10) )")
        self.con.commit()

    

    
    # for inset data in studnet table
    '''CREATE A Task'''
    def create_record(self,first_name, last_name, f_name, cnic, mobile_no, class_name):
        self.cursor.execute("INSERT INTO student_table(first_name, last_name, f_name, cnic, mobile_no, class_name) VALUES(?, ?, ?,?,?,?)", (first_name,last_name,f_name,cnic,mobile_no,class_name))
        self.con.commit()

    # load record from database in page 
    def get_record(self):
        # self.load_record = self.cursor.execute("SELECT id, first_name, last_name, f_name, cnic, mobile_no, class_name FROM student_table ").fetchall()
        self.cursor.execute("SELECT * FROM student_table")
        self.rows = self.cursor.fetchall()
        self.con.commit()


        self.data_list = [] #to store all rows in list 

        for row in self.rows: # looping for all rows in appent in data list 
            self.data_list.append(row)

        return self.data_list

    """ It code define to search one row in DB but it and get search_record page """
    def search_record(self,id):
        row = (self.cursor.execute("SELECT* FROM student_table WHERE id = ? ",(id,)).fetchall())
        
        searching_row = []
        if row == []:
            pass
        else:
            row = row[0]
            for i in row:
                searching_row.append(str(i))

        return searching_row

    # To delete record from student_table
    def delete_record(self, id):
        # self.cursor.execute("DELETE FROM student_table WHERE id = ?",str(id))
        self.cursor.execute("DELETE FROM student_table WHERE id = ?",(id,))

    

    # update student Record
    def update_student_record(self, first_name, last_name, f_name, cnic, mobile_no, class_name, id):
        self.cursor.execute(
            """
            UPDATE student_table
            SET 
                first_name = ?,
                last_name = ?,
                f_name = ?,
                cnic = ?,
                mobile_no = ?,
                class_name = ?
            WHERE id = ?
            """,
            (first_name, last_name,f_name, cnic, mobile_no, class_name, id)
        )
        self.con.commit()
        print("First row updated successfully.")
        

   
   
    # ****************************************** End of the student data table ************************************
        

db = Database()




class Manager(MDScreenManager):
    pass    


class UpdatePage(MDScreen):
    def get_record(self): # 
        id = self.ids.id.text # get id from Updated page MDTextField
        # print(id)
        row = db.search_record(id) # class search_record function to get single row or record
        
        if row == []: # if we get empty list, than print message
            print("no record found")

            self.ids.first_name.text = ""
            self.ids.last_name.text = ""
            self.ids.f_name.text = ""
            self.ids.cnic.text  = ""
            self.ids.mobile_no.text = ""
            self.ids.class_name.text = ""
        
        else: # if list not empty the do prosess
        
            id, first_name, last_name, f_name, cnic, mobile_no, class_name = row # unpack list

            # set data on MDTextField from Database
            self.ids.first_name.text = first_name
            self.ids.last_name.text = last_name
            self.ids.f_name.text = f_name
            self.ids.cnic.text  = cnic
            self.ids.mobile_no.text = mobile_no
            self.ids.class_name.text = class_name
            # print(self.class_name)

            

    # here we are try to update record in our Database
    def update_record(self):
        # print("i call successfuly your prosess next")
        
        #  Get text or vlaues from UpdatePage where user change in Database
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        f_name = self.ids.f_name.text
        cnic = self.ids.cnic.text
        mobile_no = self.ids.mobile_no.text
        class_name = self.ids.class_name.text
        id = self.ids.id.text

        # just for checking values 
        # print(id)
        # print(first_name)
        # print(last_name)
        # print(f_name)
        # print(cnic)
        # print(mobile_no)
        # print(class_name)

        # send variables in update_student_record  (it functin define in Database file code)
        db.update_student_record(first_name, last_name, f_name, cnic, mobile_no, class_name, id)
        
        # After changeing recored clear MDTextFields 
        self.ids.id.text = ""
        self.ids.first_name.text = ""
        self.ids.last_name.text = ""
        self.ids.f_name.text = ""
        self.ids.cnic.text  = ""
        self.ids.mobile_no.text = ""
        self.ids.class_name.text = ""


class ForgetPage(MDScreen):
    # get values from forget page MDTextFields
    def get_forget_page(self):
        self.cnic = self.ids.cnic.text
        self.mobile_no = self.ids.mobile_no.text
        self.new_passward = self.ids.new_passward.text
        self.confirm_passward = self.ids.confirm_passward.text
        # print(cnic) # jsut for chacking variables
        # print(mobile_no)
        # print(new_passward)
        # print(confirm_passward)

        # condition To require all fields to Fill
        if self.cnic =="" and self.mobile_no == "" and self.new_passward == "" and self.confirm_passward == "":
            self.ids.indicater.text = "   Fill all fields"
        else:     
            if self.new_passward == self.confirm_passward: # Conditon if new passwar match with confirm passward, otherwise else
                self.get_signup_table() # call if function
            else:
                self.ids.indicater.text = "   password not match"

    # get signup table row
    def get_signup_table(self):
        row = db.get_register_record()
        if row !=[]:
            row = row[0] # unpack tuples to list 
            # print(row)
            id, first_name, last_name, mobile_no,cnic, email, passward = row # unpack tuples

            # conditon if MDTextField cnic and mobile no check with Database record
            if self.cnic == cnic and self.mobile_no == mobile_no:
                print("passward match")
                db.forget_password(first_name, last_name,mobile_no, cnic, email, self.confirm_passward)
                self.manager.current = "login_page"
            else: 
                self.ids.indicater.text = "   Nic or mobile no not match with database"
        else: 
            self.ids.indicater.text = "   User not found"




class SignUp(MDScreen):
    def sign_up_page_values(self):

        # get values from SignUp page 
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        mobile_no = self.ids.mobile_no.text
        cnic = self.ids.cnic.text
        email = self.ids.email.text
        passward = self.ids.passward.text
        confirm_passward = self.ids.confirm_passward.text

        # get first row of a register table
        self.first_row_db = db.get_register_record()

        # condition on the MDTextFields in your SignUp page
        # print(self.first_row_db)
        if first_name != "" and last_name != "" and mobile_no != "" and email != "" and passward != "" and confirm_passward != "":
            if passward == confirm_passward:
                # print("passward make successfuly")
                pass
                if self.first_row_db == []: # condition if one user exist or not (create one user or not)
                    db.create_sign_record(first_name, last_name, mobile_no, cnic, email, passward)
                    self.manager.current  = "login_page" # if all condition ture, change screen
                else:
                    # print("one user alrady exist")
                    self.ids.indicate_in_signup_page.text = "Only allowed one user, one user already exist"
            else:
                # print("passward not match")
                self.ids.indicate_in_signup_page.text = "passward not match"

        else:
            self.ids.indicate_in_signup_page.text = "Please fill all fields"
            
        
        
        
        
    

class LoginPage(MDScreen):
    def get_login_values(self):
        
        # get username and passward from LoginPage
        self.email = self.ids.email.text
        self.passward = self.ids.passward.text

        # get user data from db
        user_data = db.get_register_record()
        # print(user_data)
        if user_data == []:
            # print("no record of user")
            self.ids.incorrect.text = "create account"
        else:
            user_data = user_data[0] # for uppack list becuse we have tuples in list
            id, first_name, last_name, mobile_no, cnic, email, passward = user_data  # for unpack tuples
            # print(f"id:{id}")
            # print(f"first name:{first_name}")
            # print(f"last_name:{last_name}")
            # print(f"mobile_no:{mobile_no}")
            # print(f"cnic:{cnic}")
            # print(f"email:{email}")
            # print(f"passward:{passward}")

            #  show indicate if codition true or false also elif
            if self.email == email and self.passward == passward:
                self.manager.current = "home_page"
                self.manager.transition = SlideTransition(direction="right")  # Slide animation
            elif self.email == "" or self.passward == "":
                self.ids.incorrect.text = "Fill all fields"
            else: 
                self.ids.incorrect.text = "username or\npassword incorrect"
            

class HomePage(MDScreen):
    pass


class ViewStudent(MDScreen):
    def on_enter(self, *args):
        # Clear existing list items to avoid duplication
        self.ids.mylist.clear_widgets()

        # Fetch records from the database
        all_record_in_list = db.get_record()
        
        for row in all_record_in_list:
            id, first_name, last_name, f_name, cnic, mobile_no, class_name = row

            # Add to the list
            self.ids.mylist.add_widget(
                ThreeLineListItem(text=(f"[size=28][b][u]ID[/b]: {id}[/u][/size]    [size=28][b]Name[/b]: {first_name}_{last_name}[/size]    [size=28][b]F/Name[/b]: {f_name}[/size]"),
                secondary_text=(f"[size=28][b]NIC[/b]: {str(cnic)}[/size]    [size=28][b]Phone[/b] : {mobile_no}[/size] "),
                tertiary_text= (f"[u][b][size=28]Class[/b]: {class_name}[/size]                                                                                                                                                                                   ")
                
                )
            )
        

class AddStudent(MDScreen):
    def get_text_from_add_record(self):
        # id = self.ids.id.text
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        f_name = self.ids.f_name.text
        cnic = self.ids.cnic.text
        mobile_no = self.ids.mobile_no.text
        class_name = self.ids.class_name.text


        #  Only for terminal print 
        # print(type(first_name))
        # print(type(last_name))
        # print(type(f_name))
        # print(type(cnic))
        # print(type(mobile_no))
        # print(type(class_name))
        
        if first_name and last_name !="" and f_name != "" and mobile_no != "" and cnic != "" and class_name != "":
            # To inset record in database  (student table)
            db.create_record(first_name, last_name, f_name, cnic, mobile_no, class_name)

            # when record inset in Database, clear text from MDTextField in Add_record page
            # self.ids.id.text = ""
            self.ids.first_name.text = ""
            self.ids.last_name.text = ""
            self.ids.f_name.text = ""
            self.ids.cnic.text =""
            self.ids.mobile_no.text = ""
            self.ids.class_name.text = ""
            self.ids.error_indicate.text = ""
        else:
            self.ids.error_indicate.text = "Require all field"

class SearchStudent(MDScreen):

    def searching_row(self):
        global store_id # it is global variable
        self.search = self.ids.search_student.text # get values from search box

        record = db.search_record(self.search) # get single row record in List(tuples)  for the help of search_record fuction in your database.py file
        # print(record)
        if  record == []: # if record not found
            print("recod not found")
            self.ids.record_not_found_indicate.text = "Recorde not found" # if record not show set on lable it masssage  
            self.clear_labels() # clear label from text
            store_id = "" # if record not found then assign "" to globle var

        else: # when record found
            self.id, first_name, last_name, f_name, cnic, phone, class_name = record # unpack tuples store in Variables
            store_id = ""
            # print("i am form esle:", id)
            # Just for chacking Variables
            # Variables کوچیک کریں
            # print("ID:", type(id))
            # print("First Name:", type(first_name))
            # print("Middle Name:", type(last_name))
            # print("Last Name:", type(f_name))
            # print("CNIC:", type(cnic))
            # print("Phone:", type(phone))
            # print("class_name", type(class_name))

            # set data on labels in SearchStudent page
            self.ids.id_id.text = (f"  ID:   {str(self.id)}")
            self.ids.full_name.text = (f"  Name:   {first_name}_{last_name}")
            self.ids.f_name.text = (f"  F.Name:   {f_name}")
            self.ids.cnic.text = (f"  Naitonal ID:   {str(cnic)}")
            self.ids.mobile_no.text = (f"  Mobile:   {str(phone)}")
            self.ids.class_name.text = (f"  Class:   {class_name}")
            self.ids.record_not_found_indicate.text = ""
            
            store_id = self.search # assign search value

            self.ids.search_student.text = "" # after all search text filed clear form text





    # student record already load in searching_row function here is just make some logic and open a dialog box
    def logic_for_delete_student(self):

        global store_id

        if store_id == "":   # your id not avalable in your Database
            # print("recot not fout")
            self.ids.record_not_found_indicate.text = "You have empty page"

        else:   # Condition
            # # here is deleting recored(row)  when clikc (yess butoon) on dailog then call it fuction and delete it row
            db.delete_record(store_id) # Your id avalable in your database. then delete record(row) for the help of delete_record fuction in your database.py
            self.clear_labels() # clear lables when delete recor
     


    def clear_labels(self):
        self.ids.id_id.text = ""
        self.ids.full_name.text = ""
        self.ids.f_name.text = ""
        self.ids.cnic.text = ""
        self.ids.mobile_no.text = ""
        self.ids.class_name.text = ""  
        # print("After clear variables")



    

class DialogContent(MDBoxLayout):
    # the init function for the class constructor
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    


class MainApp(MDApp):
    def build(self):
        return

    def show_dailog(self):
        # Create and show the dialog
        self.dailog = MDDialog(
            title="Warning Message",
            type="custom",
            content_cls=DialogContent(),
        )
        self.dailog.open()
    

    # close dialog box 
    def close_dialog(self):
        self.dailog.dismiss()
        print("close dailog (it message for close_dialog function)")

    # # if click on dailog button (yes) it call
    def yes_delete_record(self):
        ob = SearchStudent() # create object of SearchStudent class
        ob.logic_for_delete_student() # call function of SearchStudent class




if __name__ == "__main__":
    MainApp().run()