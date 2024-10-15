
try :
    import database
except ModuleNotFoundError:
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