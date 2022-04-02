from OsomeDB import OsomeDB

# Create/Get DB
DB = OsomeDB("School")
# Get/Create the PassBin
student_passwords = DB.PassBin("School","Student_Passwords")
# changing the settings
DB.Settings("School").change("ENC","Hi-lol") # Turning on encryption
# make collection
DB.make_collection("Students")
# getting the collection
school_db = DB.get_collection("Students")

print("Testing The DB")
while True:
    cmd = input("""
    1) Find by id
    2) New Student
    3) Reset Password
    >
    """)
    if cmd == "1":
        Id = input("ID : ")
        print(school_db.search_by_key_val("ID",Id),student_passwords.search_by_Id(Id))
    elif cmd == "2":
        name = input("Name : ")
        Id = input("ID : ")
        Password  = input("Password : ")
        student_passwords.append_new_pass(Id,Password)
        school_db+={"Name":name,"ID":Id}
    elif cmd == "3":
        Id = input("ID : ")
        New_Password = input("New Password : ")
        student_passwords.reset_pass(Id,New_Password)
