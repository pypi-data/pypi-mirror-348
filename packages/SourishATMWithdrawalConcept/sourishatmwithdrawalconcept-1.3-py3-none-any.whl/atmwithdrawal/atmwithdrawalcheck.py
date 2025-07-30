def main():
    currentbalance = 55000
    atm_pin = 5690
    option = {1: 'withdrawal', 2: 'deposit', 3: 'Check balance'}
    print('please enter your atm and welcome to bank of America')
    gen_option = 0
    while True & gen_option == 0:

        given_pin = int(input('please enter your atm pin:   '))
        if given_pin == atm_pin:
            print(option)
            atm_option = int(input('Choose option'))

            if atm_option == 1:
                while True:
                    amount = int(input('Please enter your Amount:  '))
                    gen_option = atm_option
                    if amount > currentbalance:
                        print('Insufficient Balance')
                        break
                    elif amount <= currentbalance:
                        print(f'hold amount dispesing :{amount}')
                        currentbalance -= amount
                        print(f'Your current balance:{currentbalance}')
                        is_con = input('Do you want to withdraw again then type YES/Y or type anything else: :')
                        if is_con == 'YES' or is_con == 'yes' or is_con == 'Y' or is_con == 'y':
                            continue
                        else:
                            break
            elif atm_option == 2:
                amount = int(input('please enter your amount'))
                currentbalance += amount
                print(currentbalance)
            elif atm_option == 3:
                print(currentbalance)
                print('Thank you')
                break
            else:
                print('Not a valid option')
                break
        else:
            print('Not a valid option')
            break