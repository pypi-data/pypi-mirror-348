import atmwithdrawalcheck as m
if __name__=='__main__':
    atm = m.Atmfunctionality()
    print('please enter your atm and welcome to bank of America')
    balance=int(input('enter balance'))
    atm.main(balance)
