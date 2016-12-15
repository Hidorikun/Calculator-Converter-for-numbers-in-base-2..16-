
class ProgramException(Exception):
    pass


class BaseNumException(ProgramException):
    pass


class BaseNum(object):
    
         
    def __init__(self, value, base):
        '''
        This method initialises the object:
        :args:
            value - string representing the value 
            base - base of the value 
        '''
        self.__value = value.lower()
        self.__base = base
        self.__signed = False
        if len(value) != 0 and value[0] == '-':
            self.__value = value[1:]
            self.__signed = True
        
        self.__trim_front_zeros()
        self.__validate()
        if self.__value =='0':
            self.__signed = False 
        
    def __trim_front_zeros(self):
        '''
        trims the front zeros of the object's value
        if value consists of only one 0, it is left intact
        '''
        while len(self.__value) > 1 and self.__value[0] == '0':
            self.__value = self.__value[1:]
            
    @staticmethod
    def digit(d):
        '''
        returns the digit d converted to base 10
        :args
            d - character representing the digit to be converted
        :returns
            int(d) - if d between ['0', '9']
            ord(d) - ord('a') + 10 if d between ['a', 'z']
        '''
        
        if d >=  '0' and d <='9':
            return int(d)
    
        if d >= 'a' and d <= 'z':
            return ord(d) - ord('a') + 10
        
    def __validate(self):
        '''
        method that validates the properties of  the object 
        :raises
            BaseNumException if :
                - base is not an integer number
                - the value is an empty string 
                - the base is not between [2, 16] 
                - the value has characters besides ['0' - '9'],['a' - 'f']
                - the characters in value are greater than base
        '''
        try:
            self.__base = int(self.__base)
        except ValueError:
            raise BaseNumException("Error -- base must be an integer number")
        
        if len(self.value) == 0:
            raise BaseNumException("Error -- value cannot be empty")
        
        if self.base < 2 or self.base > 16:
            raise BaseNumException("Error -- base must be between [2, 16]")
        
        for v in self.value:
            if v not in '0123456789abcdef':
                raise BaseNumException('Error -- value must only contain digits and letters from [a..f]')
            if BaseNum.digit(v) >= self.base:
                raise BaseNumException("Error -- values must be smaller than the base")
    
    @property
    def value(self):
        '''
        property that returns the object's value
        :returns
            self.__value 
        '''
        return self.__value 
    
    @property
    def base(self):
        '''
        property that returns the object's base
        :returns
            self.__base
        '''
        return self.__base 
    
    @property
    def signed(self):
        '''
        property that returns if the object is signed or not 
        '''
        return self.__signed
   
    def __getitem__(self, i):
        '''
        method that returns self.value[i] whenever object[i] is called
        '''
        return self.value[i]
        
    def __str__(self):
        '''
        method that overridees the default string representation of the object
        iw will be represented as 'sgn+value+(base)' for example -1a3(16)
        '''
        if self.signed:
            sign = '-'
        else:
            sign = ''
        return sign + self.value  + '({base})'.format(base  = self.base)
        
    def __add__(self, other):
        '''
        this method is called whenever we have a + b, there a and b are BaseNum objects
        this add override works more like a switch for the __addition_implementation method
        it chooses how to call the __addition_implementaton method depending on the sign of
        its arguments
        :args
            self - this object
            other - the other object in the expression
        :returns
            sum(self,  other) if they are both positive 
            sub(self, -other) if self is positive and other negative 
            sub(other, - self) if self is negative and b is positive
            -sum(-a, -b) if both are negative 
            
            where:
                sum = __addition_implementation
                sub = __subtraction_implementation
                
            and returns the BaseNum object that represents the sum of the self and other
        
        '''
        a = self
        b = other 
        
        a_positive = not a.signed 
        a_negative = a.signed 
        
        b_positive = not b.signed 
        b_negative = b.signed 
        
        sum = self.__addition_implementation
        sub = self.__subtraction_implementation
        
        if a_positive and b_positive:
            return sum(a, b)
        
        if a_positive and b_negative:
            return sub(a, -b)
        
        if a_negative and b_positive:
            return sub(b, -a)
        
        if a_negative and b_negative:
            return -sum(-a, -b)
        
    def __sub__(self, other):
        '''
        this method is called whenever we have a - b, where a and b are BaseNum objects
        this method works more like a switch for the __subtraction_implementation method
        it chooses how to call the __subtraction_implementation method depending on the sign
        of its arguments
        :args
            self -this object
            other - the other object in the expression
        :returns
            sub(self,other) if both are positive
            sum(self, -other) if a is positive and b ie negative
            -sum(-self, other) it a is negative and b is positive 
            sub(-other, -self) if both are negative
            
            where:
                sum = __addition_implementation
                sub = __subtraction_implementation
                
            and returns the BaseNum object that represents the sum of the self and other
    
        '''
        a = self
        b = other 
        
        a_positive = not a.signed 
        a_negative = a.signed 
        
        b_positive = not b.signed 
        b_negative = b.signed 
        
        sum = self.__addition_implementation
        sub = self.__subtraction_implementation
        
         
        if a_positive and b_positive:
            return sub(a, b)
        
        if a_positive and b_negative:
            return sum(a, -b)
        
        if a_negative and b_positive:
            return -sum(-a, b)
        
        if a_negative and b_negative:
            return sub(-b, -a)
    
    def __mul__(self, other):
        '''
        this method is called whenever we have a * b where a and b are BaseNum objects
        :returns
            BaseNum object that has the the multiplied value of self and other in their base 
        '''
        
        a = -self if self.signed else self
        b = -other if other.signed else other
        
        # a and b are the positive values of self, respectively other 
        
        result = self.__multiplication_implementation(a, b)
        
        #if don't have the same sign, the product will be negative
        if self.signed != other.signed:
            result = -result
        
        #else it will be positive
        return result
        
    def __truediv__(self, other):
        '''
        this method is called whenever we have a / b where a and b are BaseNum objects
        :returns
            BaseNum object that has the value of self divided by other  in their base
        '''
        
        a = -self if self.signed else self
        b = -other if other.signed else other
        # a and b are the positive value of self, respectively other 
        
        result = self.__division_implementation(a, b)
        
        #if they don't have the same sign, the division will be negatives
        if self.signed != other.signed:
            result = -result
        
        #else it will be positive
        return result
    
    def __mod__(self, other):
        '''
        this method is called whenever we have a % b where a and b are BaseNum objects
        :returns
            BaseNum object that has the modulus value between self and other
        
        '''
        
        a = -self if self.signed else self
        b = -other if other.signed else other
            
        # a and b have the positive values of self, respectively other 
        
        result = self.__modulus_implementation(a, b)
        
        #if they don't have the same sign, the modulus is negative
        if self.signed != other.signed:
            result = -result
        
        #else it it positive
        return result
    
    def __neg__(self):
        '''
        returns the negated BaseNum of self
        '''
        value = self.value 
        base = self.base 
        
        #if it is positive, make it negative
        if not self.signed:
            value = '-' + value
        
        # else make it positive
        neg = BaseNum(value, base)
        return (neg)

    def __pos__(self):
        '''
        retuns the same BaseNum object x, when +x is called
        '''
        return self

    def __eq__(self, other):
        '''
        tests if two BaseNum objects are equal
        :returns 
            True, if their base, value and sign are the same
            Fasle, otherwise 
        '''
        
        a = self
        b = other 
        if a.base != b.base:
            raise BaseNumException('Error -- the two operands must have the same base')
        
        if a.signed == b.signed and a.value == b.value:
            return True 
        return False 
      
    def __lt__(self, other):
        
        ''' 
        tests if a < b, where a and b are BaseNum objects
        :returns
            True, if self < other
            False, otherwise
        '''
        a = self 
        b = other 
        
        if a.base != b.base:
            raise BaseNumException('Error -- the two operands must have the same base')
        
        if a.signed and not b.signed:
            return True 
        if not a.signed and b.signed:
            return False
        
        sign = a.signed
        
        if a.value == b.value:
                return False
            
        if  len(a.value) == len(b.value):
            less_in_module = a.value < b.value
            return self.__xor(less_in_module, sign)
    
        less_length = len(a.value) < len(b.value)
        return self.__xor(less_length, sign)
    
    def __gt__(self, other):
        '''
        tests if a > b, where a,b are BaseNum objects 
        :returns 
            True, if a > b
            False otherwise
        '''
        a = self
        b = other 
        
        return not ((a < b) or (a == b))
    
    def __ge__(self, other):
        '''
        tests if a >= b, where a,b are BaseNum objects 
        :returns 
            True, if a >= b
            False otherwise
        '''
        a = self
        b = other 
         
        return not(a < b)
    
    def __le__(self, other):
        '''
        tests if a <= b, where a,b are BaseNum objects 
        :returns 
            True, if a <= b
            False otherwise
        '''
        a = self
        b = other 
        
        return not (a > b)

    def __xor(self, a, b):
        '''
        returns the xor value of 2 boolean values
        :returns
            True if a != b
            False if a == b
        
        where a, b are from [True, False]
        '''
        if a == b:
            return False
        return True

    def __addition_implementation(self, a, b):
        '''
        This implementation solves the addition between 2 positive BaseNum numbers
        :args
            a, b - positive BaseNum objects
            
        :returns:
            BaseObject that repersents the sum of a and b in their base
        '''
        
        if a.base != b.base:
            raise BaseNumException('Error -- the two operands must have the same base')
        
        s = []
        n, m = len(a.value), len(b.value)
        n-=1
        m-=1
        carry = 0
        while (m > -1) and (n > -1):
            x = a.digit(a[n])
            y = a.digit(b[m])
            s.insert(0, (x + y + carry) % a.base)
            carry = (x+ y + carry) // a.base
            n -= 1
            m -= 1
            
        while m > -1:
            y = a.digit(b[m])
            s.insert(0, (y + carry) % a.base)
            carry = (y + carry) // a.base
            m -= 1
            
        while n > -1:
            x = a.digit(a[n])
            s.insert(0, (x + carry) % a.base)
            carry = (x + carry) // a.base
            n -= 1
        
        if carry != 0:
            s.insert(0, carry)
            
        for i in range(len(s)):
            if (s[i] >= 10):
                s[i] = chr(s[i] - 10 + ord('a'))
            else:
                s[i] = str(s[i])
                
        result = BaseNum(''.join(s), a.base)
        return result
    
    def __subtraction_implementation(self, a, b):
        '''
        This implementation solves the subtraction between 2 positive BaseNum numbers
        :args
            a, b - positive BaseNum objects 
        :return
            BaseNum that represents the difference between a and b in their base
        '''
        
        if a.base != b.base:
            raise BaseNumException('Error -- the two operands must have the same base')
        
        invert_result = a < b
        if invert_result:
            a, b = b, a
            
        values1 = [BaseNum.digit(v) for v in a.value]
        values2 = [BaseNum.digit(v) for v in b.value]
        
        n = len(values1)
        while len(values2) != n:
            values2.insert(0, 0)
        
        n-=1
        
        result = [v for v in values1]
        
        
        while(n > -1):
            if (values1[n] < values2[n]):
                values1[n-1] -= 1
                values1[n] += self.base
        
            result[n] = values1[n] - values2[n]
            
            n-=1
        
        
        for i in range(len(result)):
            if (result[i] >= 10):
                result[i] = chr(result[i] - 10 + ord('a'))
            else:
                result[i] = str(result[i])
                
        result = BaseNum(''.join(result), self.base)
                
        if invert_result:
            return - result
        
        return result
            
    def __division_implementation(self, a, b):
        '''
        This implementation solves the division between a positive number and a digit
        :args
            a, b - positive BaseNum objects 
            obs! - b must have a single digit value 
        :return
            BaseNum that represents the division between a and b in their base
        '''
    
        if a.base != b.base:
            raise BaseNumException('Error -- the two operands must have the same base')
        
        if len(b.value) != 1:
            raise BaseNumException("Error -- you can only divide with single digit numbers")
        
        if b.value == '0':
            raise BaseNumException('Error -- division by 0')
        
        base = a.base
        
        reminder = BaseNum('0', base)
        quotent = BaseNum('0', base)
        
        b = int(BaseNum.convert_to_base_10(b).value)
        
        for v in a:
            reminder = BaseNum(reminder.value + v, base)
            aux = int(BaseNum.convert_to_base_10(reminder).value)
            reminder = BaseNum(str(aux % b), 10)
            reminder = BaseNum.convert_from_base_10_to(reminder, base)
            aux2 = BaseNum(str(aux // b), 10)
            aux2 = BaseNum.convert_from_base_10_to(aux2, 16)
            
            quotent = BaseNum(quotent.value + aux2.value, base)
            
        return quotent
            
    def __multiplication_implementation(self, a, b):
        '''
        this method solves the multiplication between 2 BaseNum objects a and b
        :args 
            a, b - BaseNum objects 
        :returns
            BaseNuum object that represents the objects a and b multiplied in their base 
        '''
        
        def multiplication_by_one_digit(a, b):
            '''
              this mehod solves the multiplication of a and b, BaseNum objects, b digit
              :args
                  a, b - BaseNum objects, b must have a single digit value
              :returns
                  BaseNum that represents a and b multiplied
             '''
            if len(b.value) != 1:
                raise BaseNumException("Error -- you can only m with single digit numbers")
            
            result = []
            values = [self.digit(v) for v in a]
            n = len(values) -1 
            b = int(BaseNum.convert_to_base_10(b).value)
            carry = 0
            base = a.base
            
            while( n >= 0 ):
                aux = carry + values[n]*b
                result.insert(0, aux % base)
                carry = aux // base 
                n-=1
            
            result.insert(0, carry)
            for i in range(len(result)):
                if (result[i] >= 10):
                    result[i] = chr(result[i] - 10 + ord('a'))
                else:
                    result[i] = str(result[i])
            
            result = BaseNum(''.join(result), self.base)
            return result
        
        if a.base != b.base:
            raise BaseNumException('Error -- the two operands must have the same base')
            
        base  = a.base        
        result = BaseNum('0', base)
        
        # multiplies every digit of b with a using the multiplication_by_one_digit method and 
        # add the results together, being careful to add the specific zeros 
        n = len(b.value)-1
        while n >=0:
            nr_of_zeros = len(b.value) -1 -n
            digit = BaseNum(b[n], base)
            aux = multiplication_by_one_digit(a, digit) 
            for _ in range(nr_of_zeros):
                aux = BaseNum(aux.value + '0', aux.base)
            result = result + aux
            n-=1
        return result
   
    def __modulus_implementation(self, a, b):
        '''
        This implementation solves the modulus between a positive number and a digit
        :args
            a, b - BaseNum objects
        :return 
            BaseNum object representing the value of a % b in their base
        '''
    
        if a.base != b.base:
            raise BaseNumException('Error -- the two operands must have the same base')
        
        if len(b.value) != 1:
            raise BaseNumException("Error -- you can only divide with single digit numbers")
        
        if b.value == '0':
            raise BaseNumException('Error -- division by 0')
        
        base = a.base
        
        reminder = BaseNum('0', base)
        quotent = BaseNum('0', base)
        
        b = int(BaseNum.convert_to_base_10(b).value)
        
        for v in a:
            reminder = BaseNum(reminder.value + v, base)
            aux = int(BaseNum.convert_to_base_10(reminder).value)
            reminder = BaseNum(str(aux % b), 10)
            reminder = BaseNum.convert_from_base_10_to(reminder, base)
            aux2 = BaseNum(str(aux // b), 10)
            aux2 = BaseNum.convert_from_base_10_to(aux2, 16)
            
            quotent = BaseNum(quotent.value + aux2.value, base)
        #the same implementation as division, the difference being that we return the reminder
        return  reminder
    
    @staticmethod
    def convert(baseNum, destination_base):
        '''
        convert method that chooses what conversion method to call based on source base and destination base
        :args
            baseNum - BaseNum object 
            destination_base - integer representing the base in which we want to convert
        :returns 
            BaseNum object representing the equivalent of baseNum in base destination_base
        '''
        
        if destination_base < 2 or destination_base > 16:
            raise BaseNumException('Error -- a number can only be converted to a base between [1, 16]')
        
        if destination_base == baseNum.base:
            return baseNum 
        
        if destination_base == 10:
            return BaseNum.convert_to_base_10(baseNum)
        
        if destination_base in [2, 4, 8, 16] and baseNum.base in [2, 4, 8, 16]:
            return BaseNum.convert_rapid_conversion(baseNum, destination_base)
        
        if destination_base > baseNum.base:
            return BaseNum.convert_substitution_method(baseNum, destination_base)
        
        if destination_base < baseNum.base:
            return BaseNum.convert_successive_divitions(baseNum, destination_base)
        

    @staticmethod
    def convert_rapid_conversion(baseNum, destination_base):
        '''
            conversion method that is used when converting between bases [2, 4, 8, 16]
            :args 
                baseNum - BaseNum object that we want to convert 
                destination_base - integer value representing the base in which we want the result
            :return
                BaseNum object that represents the equivalent of baseNum in base destination_base
            :raises
                BaseNumException - if source_base or destination_base are not from [2, 6, 8, 16]
        '''
        to_base2 = {'0':'0000','1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101', '6':'0110',
                    '7':'0111','8':'1000','9':'1001','a':'1010','b':'1011','c':'1100','d':'1101',
                    'e':'1110','f':'1111'}
        from_base2 ={'0001':'1','0101':'5','0000':'0','1101':'d','0111':'7','0100':'4','1001':'9',
                     '0110':'6','0010':'2','1100':'c','0011':'3','1110':'e','1000':'8','1111':'f',
                     '1011':'b','1010':'a'}
        
        source_base = baseNum.base
        if source_base not in [2, 4, 8, 16] or destination_base not in [2, 4, 8, 16]:
            raise BaseNumException('both bases must be from [2, 4, 8, 16]')
        
        p1 = 1
        while 2 ** p1 != source_base and 2 ** p1 <= 16:
            p1+=1
            
        p2 = 1
        while 2 ** p2 != destination_base and 2 ** p2 <=16:
            p2 += 1
            
        binary_rep = [to_base2[v][-p1:] for v in baseNum]
        binary_rep = ''.join(binary_rep)
        
        while len(binary_rep) % p2 != 0:
            binary_rep = '0' + binary_rep 
            
        result = ''
        i = 0
        while i < len(binary_rep):
            slice = binary_rep[i:i+p2]
            while len(slice) < 4:
                slice = '0' + slice 
            result += from_base2[slice]
            i+=p2
    
        result = BaseNum(result, destination_base)
        
        if baseNum.signed:
            return -result 
        
        return result
            

    @staticmethod
    def convert_substitution_method(baseNum, destination_base):
        '''
            conversion method that is used when source_base < destination_base
            :args 
                baseNum - BaseNum object that we want to convert 
                destination_base - integer value representing the base in which we want the result
            :return
                BaseNum object that represents the equivalent of baseNum in base destination_base
            :raises 
                BaseNumException - if source_base > destination_base
        '''
        
        result = BaseNum('0', destination_base)
        
        source_base = baseNum.base 
        
        if source_base > destination_base:
            raise BaseNumException('This method is used when source base < destination base')
        
        if source_base >= 10:
            converted_base = chr(source_base - 10 + ord('a'))
        else:
            converted_base = str(source_base)
            
        multiplier = BaseNum(converted_base, destination_base)
        k = BaseNum('1', destination_base)
        
        n = len(baseNum.value) - 1 
        
        while n>=0:
            aux = BaseNum(baseNum[n], destination_base)
            result = result + aux * k 
            k = k * multiplier
            n-=1
            
        if baseNum.signed:
            return - result 
        
        return result
         
    
    @staticmethod 
    def convert_using_10_as_intermediare_base(baseNum, destination_base):
        
        '''
            conversion method that is used for all bases
            :args 
                baseNum - BaseNum object that we want to convert 
                destination_base - integer value representing the base in which we want the result
            :return
                BaseNum object that represents the equivalent of baseNum in base destination_base
        '''
        
        intermediare = BaseNum.convert_to_base_10(baseNum)
        return BaseNum.convert_from_base_10_to(intermediare, destination_base)
    
    @staticmethod
    def convert_to_base_10(baseNum):
        
        '''
            conversion method that is used when converting to base 10 from any base
            :args 
                baseNum - BaseNum object that we want to convert to base 10
            :return
                BaseNum object that represents the equivalent of baseNum in base destination_base
        '''
        values = [BaseNum.digit(v) for v in baseNum]
        n = len(values) -1
        
        result = 0 
        k = 1
    
        while n >= 0:
            result += values[n] * k 
            k *= baseNum.base 
            n -= 1
            
        result = BaseNum(str(result), 10)
        if baseNum.signed:
            result = - result
        return result
            
    @staticmethod
    def convert_successive_divitions(baseNum, destination_base):
        '''
            conversion method that is used when source_base > destination_base
            :args 
                baseNum - BaseNum object that we want to convert 
                destination_base - integer value representing the base in which we want the result
            :return
                BaseNum object that represents the equivalent of baseNum in base destination_base
            :raises  
                BaseNumException if source_base < destination_base
        '''
        
        if baseNum.value == '0':
            return BaseNum('0', destination_base)
        
        signed = baseNum.signed 
        base = baseNum.base
        
        value = destination_base
             
        if base < destination_base: 
            raise BaseNumException('This method is used only if the source base > the destination base')
        
        if (value >= 10):
            value = chr(value - 10 + ord('a'))
        else:
            value = str(value)
        
        a = BaseNum(baseNum.value, baseNum.base)
        b = BaseNum(value, base)

        result = []
        remainder = 0
        while a.value != '0':
            remainder = BaseNum.digit((a % b).value)
            a = a / b 
            result.insert(0, remainder)
        
        for i in range(len(result)):
            if (result[i] >= 10):
                result[i] = chr(result[i] - 10 + ord('a'))
            else:
                result[i] = str(result[i])
        
        result = BaseNum(''.join(result), destination_base)
        
        if signed:
            result = - result 
        return result
            
    @staticmethod
    def convert_from_base_10_to(baseNum, destination_base):
        '''
            conversion method that is used when converting from base 10 to any base
            :args 
                baseNum - BaseNum object that we want to convert  in base 10
                destination_base - integer value representing the base in which we want the result
            :return
                BaseNum object that represents the equivalent of baseNum in base destination_base
        '''
        number = int(baseNum.value)
        base = destination_base
        
        if number == 0:
            return BaseNum('0', destination_base)
        
        result = []
        reminder = 0 
        quotent = 0
        
        while number != 0:
            reminder = number % base
            quotent = number // base
            result.insert(0, reminder)
            number = quotent
        
        for i in range(len(result)):
            if (result[i] >= 10):
                result[i] = chr(result[i] - 10 + ord('a'))
            else:
                result[i] = str(result[i])
                
        return BaseNum(''.join(result), destination_base)
    
        