'''some tests'''

try :
    import BurgerOrderer.app
except ModuleNotFoundError:
    print('The file app.py does not exist')
else :
    print("The file app.py does exist")

try:
    import KitchenView.app
except ModuleNotFoundError:
    print("The file add_user.py does not exist")
else :
    print("The file app.py does exist")

try :
    import KitchenView.add_user
except ModuleNotFoundError :
    print("The file add_user.py does not exist")
else:
    print("The file add_user.py does exist")