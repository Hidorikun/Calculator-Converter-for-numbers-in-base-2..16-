from domain.entities import BaseNum, ProgramException
class ExitException(Exception):
    pass

class Console(object):
    '''
    class respoisabile for user interface
    '''
    def run(self):
        '''
        main menu loop
        '''
        
        while True:
            print('Author: Vele Radu George - group 917')
            print('You can:')
            menu = {1: 'ADD - add two numbers in base b',
                    2: 'SUBTRACT - subtract two numbers in base b',
                    3: 'MULTIPLY - multiply two numbers in base b',
                    4: 'DIVIDE - divide a number with a digit in base b',
                    5: 'CONVERT - enter the conversion menu',
                    6: 'Interactive Console',
                    7: 'EXIT - exit the program'

                    }
            for key in menu:
                print('{0}. {1}'.format(key, menu[key]))
            print('--------------------------------------------------------')
            print('IMPORTANT NOTE!')
            print('All results will be printed under the form value(b)')
            print('where value represents the value of the number in base b')
            print('--------------------------------------------------------')
            print('Input your command number:')
            
            cmds= {1: self.addition,
                   2: self.subtraction,
                   3: self.multiplication,
                   4: self.division,
                   5: self.conversion_menu,
                   6: self.interactive_console,
                   7: self.exit
                   }
            
            try:
                cmd = int(input())
                cmds[cmd]()
                self.press_enter_to_continue()
            except ValueError:
                print('Error -- command must be integer')
                self.press_enter_to_continue()
            except KeyError:
                print('Error -- there is no such command')
                self.press_enter_to_continue()
            except ProgramException as ex:
                print(ex)
                self.press_enter_to_continue()
            except ExitException:
                return 
            finally:
                print('')
                
    
    def __read_two_base_numbers(self):
        '''
        method that reads from the user two BaseNum objects
        :returns
            a tuple consisting of 2 BaseNum objects
        '''
        base = input('Base: ')
        BaseNum('0', base)
        
        a = input('a = ')
        a = BaseNum(a, base)
        
        b = input('b = ')
        b = BaseNum(b, base)
        return a, b
    
    def addition(self):
        '''
        method that prints the sum of two BaseNum objects given by the user
        '''
        a, b = self.__read_two_base_numbers()
        print(a + b)
    
    def subtraction(self):
        '''
        method that prints the difference between two BaseNum objects given by the user
        '''
        a, b = self.__read_two_base_numbers()
        print(a - b)
    
    
    def multiplication(self):
        '''
        method that prints the product of two BaseNum objects given by the user
        '''
        a, b = self.__read_two_base_numbers()
        print(a * b)
     
    
    def division(self):
        '''
        method that prints the division of two BaseNum objects given by the user
        '''
        a, b = self.__read_two_base_numbers()
        print(a / b)
     
    
    def conversion_menu(self):
        '''
        the conversiom menu loop
        '''
        while True:
            
            print('Author: Vele Radu George - group 917')
            print('You can:')
            menu = {1: 'SMART CONVERT - chooses the best method for conversion',
                    2: 'SUBSTITUTION METHOD - for source base < destination base',
                    3: 'SUCCESIVE DIVISIONS METHOD - for source base > destination base',
                    4: 'RAPID CONVERSIONS - for bases [2, 4, 8, 16]',
                    5: 'RETURN TO MENU'
                    }
            
            cmds= {1: self.smart_conversion,
                   2: self.substitution_method,
                   3: self.successive_divisions_method,
                   4: self.rapid_conversions,
                   5: self.exit,
                   }
            
            for key in menu:
                print('{0}. {1}'.format(key, menu[key]))
                
            try:
                cmd = int(input())
                cmds[cmd]()
            except ValueError:
                print('Error -- command must be integer')
                self.press_enter_to_continue()
            except KeyError:
                print('Error -- there is no such command')
                self.press_enter_to_continue()
            except ProgramException as ex:
                print(ex)
                self.press_enter_to_continue()
            except ExitException:
                return 
            finally:
                print('')
                
        
    def read_number_and_base(self):
        '''
        method that reads a BaseNum object, and base from the user
        :returns
            a tuple with a BaseNum object and the base
        '''
        a = input('number = ')
        source_base = input('source_base = ')
        a = BaseNum(a, source_base)
        destination_base = input('destination_base = ')
        BaseNum('0', destination_base)
        
        return a, int(destination_base)
        
    def smart_conversion(self):
        '''
        method that applies smart conversion on a BaseNum object and a destination_basea given by the user
        '''
        a, destination_base = self.read_number_and_base()
        print(BaseNum.convert(a, destination_base))
        
        
    def substitution_method(self):
        '''
        method that applies substitution method conversion on a BaseNum object and a destination_basea given by the user
        '''
        a, destination_base = self.read_number_and_base()
        
        print(BaseNum.convert_substitution_method(a, destination_base))
        
    def successive_divisions_method(self):
        '''
        method that applies successive division conversion on a BaseNum object and a destination_basea given by the user
        '''
        a, destination_base = self.read_number_and_base()
        print(BaseNum.convert_successive_divitions(a, destination_base))
        
    def rapid_conversions(self):
        '''
        method that applies rapid conversion on a BaseNum object and a destination_basea given by the user
        '''
        a, destination_base = self.read_number_and_base()
        print(BaseNum.convert_rapid_conversion(a, destination_base))
    
    def exit(self):
        '''
        method that raises the exception necessary to exit a menu loop 
        :effect 
            -exiets the a menu loop
            -if that menu loop is the main loop, it exits the program
        '''
        raise ExitException
    
    def __greet_to_interactive_console(self):
        '''
        displays the greetings to the interactive console loop
        '''
        print('--------------------INTERACTIVE_CONSOLE---------------------')
        print('This is the interactive console.')
        print('Here you can play with the functionalities of the program in')
        print('an interactive way, here are some instructions:')
        print('')
        print('You can declare new variables like this:')
        print('       var_name = BaseNum(value, base)'     ) 
        print("  ex:         a = BaseNum('abf3', 16)   ")
        print('')
        print('Then you can compute any expression using the operators +,-,*,/, <, >, <=, >=')
        print('IMPORTANT NOTE! Be careful when dividing, you can only divide by one digit!')
        print('')
        print('You can also convert base numbers like this:')
        print('       var_name = BaseNum.convert(var_name, base)')
        print('  ex:         a = BaseNum.convert(a, 10)')
        print('You can exit this console by typing "exit"')
        print('HAVE FUN!')
        print('------------------------------------------------------------')
        
        
        
    def interactive_console(self):
        '''
        the interactive console loop
        '''
        print('Author: Vele Radu George - group 917')
        self.__greet_to_interactive_console()
        while True:
            try:
                expression = input('expression:')
                if expression.strip() in ['exit','exit()']:
                    return 
                if expression.count('=') == 1 and expression.count('<') == 0 and expression.count('>') == 0:
                    exec(expression)
                else:
                    print(eval(expression))
            except ProgramException as ex:
                print(ex)
            except Exception as ex:
                print(ex)
                
    def press_enter_to_continue(self):
        input("Prss ENTER to continue...") 
        