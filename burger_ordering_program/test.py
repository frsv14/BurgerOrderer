
import os.path

app_path = 'app.py'
add_user_path = 'add_user.py'
database_path = 'database.py'

db_path = '../burgers.db' 


try :
    import database
except ModuleNotFoundError:
    if os.path.isfile(db_path) == True:
        print('database has alreadey been deffined')
    else:
        print('The file database.py does not exist')
else :
    print("database was created and can now be used!")

try:
    import add_user
except ModuleNotFoundError:
    print("The file add_user.py does not exist")
else :
    print("Admin user was created and can now be used! ")

try :
    import app
except ModuleNotFoundError :
    print("The file app.py does not exist")
else:
    print("The host file has been checked and can now be ran! ")