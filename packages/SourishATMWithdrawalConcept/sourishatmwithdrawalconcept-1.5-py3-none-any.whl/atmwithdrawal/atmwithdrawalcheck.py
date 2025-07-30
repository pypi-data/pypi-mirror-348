'''
Below is the module with method

'''
class Atmfunctionality:
    def main(self, balance):
        ''' below has the hardcoded sample amount 55000 and when you provide option 1 2 3 it will start processing
         please play around with method
         '''
        self.currentbalance = balance
        self.atm_pin = 5690
        option = {1: 'withdrawal', 2: 'deposit', 3: 'Check balance'}
        print('please enter your atm and welcome to bank of America')
        gen_option = 0
        while True & gen_option == 0:

            given_pin = int(input('please enter your atm pin:   '))
            if given_pin == self.atm_pin:
                print(option)
                atm_option = int(input('Choose option'))

                if atm_option == 1:
                    while True:
                        amount = int(input('Please enter your Amount:  '))
                        gen_option = atm_option
                        if amount > self.currentbalance:
                            print('Insufficient Balance')
                            break
                        elif amount <= self.currentbalance:
                            print(f'hold amount dispesing :{amount}')
                            self.currentbalance -= amount
                            print(f'Your current balance:{self.currentbalance}')
                            is_con = input('Do you want to withdraw again then type YES/Y or type anything else: :')
                            if is_con == 'YES' or is_con == 'yes' or is_con == 'Y' or is_con == 'y':
                                continue
                            else:
                                break
                elif atm_option == 2:
                    amount = int(input('please enter your amount'))
                    self.currentbalance += amount
                    print(self.currentbalance)
                elif atm_option == 3:
                    print(self.currentbalance)
                    print('Thank you')
                    break
                else:
                    print('Not a valid option')
                    break
            else:
                print('Not a valid option')
                break