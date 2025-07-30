'''
Below is the module with method app this is the starting point guys.
Call this method for all the fun begins
'''
from atmwithdrawal import atmwithdrawalcheck as m
def app():
        atm = m.Atmfunctionality()
        print('please enter your atm and welcome to bank of America')
        balance=int(input('enter balance'))
        atm.main(balance)

if __name__ == '__main__':
    app()