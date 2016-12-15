'''
Created on Dec 1, 2016

@author: Ok!
'''
import unittest

from domain.entities import BaseNum, BaseNumException


class Test(unittest.TestCase):


    def testDigit(self):
        a = BaseNum('1234', 8)
        self.assertEqual(a.digit('1'), 1, '1 is equal to 1')
        self.assertEqual(a.digit('a'), 10, 'a is equal to 10')
        self.assertEqual(a.digit('f'), 15, 'f must be equal to 15')
    
    def testValidate(self):
        
        try:
            BaseNum('', 10)
            assert False
        except BaseNumException:
            pass 
        
        try:
            BaseNum('af', 3)
            assert False
        except BaseNumException:
            pass 
        
        try:
            BaseNum('123', 39)
            assert False 
        except BaseNumException:
            pass 
        
    def testNegation(self):
        
        a = BaseNum('-123', 10)
        self.assertEqual(a.signed, True, 'wrong initialization of number')
        
        a = -a 
        self.assertEqual(a.signed, False, 'the negation did not work')
    
        a = BaseNum('123', 10)
        self.assertEqual(a.signed, False, 'wrong initialization of number')
        
        a = -a 
        self.assertEqual(a.signed, True , 'the negation did not work')
          
    def testLess(self):
        
        for i in range(-10, 10):
            for j in range(-10, 10):
                a = BaseNum(str(i), 10)
                b = BaseNum(str(j), 10)
                self.assertEqual(i < j , a < b)
            
        a = BaseNum('ab89', 16)
        b = BaseNum('123', 16)
            
        self.assertLess(b, a)
        
        b = BaseNum('aa89', 16)
        
        self.assertLess(b, a)
                
        self.assertFalse(a < a)
        
    def testEqual(self):
        
        a = BaseNum('123', 5)
        b = BaseNum('123', 5)
        c = BaseNum('12', 5)
        
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(a, a)
        
    def testGreater(self):
        
        for i in range(-10, 10):
            for j in range(-10, 10):
                a = BaseNum(str(i), 10)
                b = BaseNum(str(j), 10)
                self.assertEqual(i > j , a > b)
            
        a = BaseNum('ab89', 16)
        b = BaseNum('123', 16)
            
        self.assertGreater(a, b)
        
        a = BaseNum('aa89', 16)
        
        self.assertGreater(a, b)        
        self.assertFalse(a > a)
        
    def testGreaterEqual(self):
        
        for i in range(-10, 10):
            for j in range(-10, 10):
                a = BaseNum(str(i), 10)
                b = BaseNum(str(j), 10)
                self.assertEqual(i >= j , a >= b)
                
    def testLessEqual(self):
        
        for i in range(-10, 10):
            for j in range(-10, 10):
                a = BaseNum(str(i), 10)
                b = BaseNum(str(j), 10)
                self.assertEqual(i <= j , a <= b)
              
    def testAdd(self):
        
        a = BaseNum('123', 10)
        b = BaseNum('321', 10)
        result = str(a+b)[:-4]
        self.assertEqual(result, '444')
        
        a = BaseNum('5abcd', 16)
        b = BaseNum('d9ef', 16)
        result = str(a+b)[:-4]
        self.assertEqual(result, '685bc')
        
        a = BaseNum('1', 10)
        b = BaseNum('5', 10)
        
        result = str( a + -b )[:-4]
        self.assertEqual(result, '-4')
        
        result = str( -a + b)[:-4]
        self.assertEqual(result, '4')
        
        result = str( -a + (-b))[:-4]
        self.assertEqual(result, '-6')
            
    def testSub(self):
          
        a = BaseNum('123', 10)
        b = BaseNum('321', 10)
        result = str(a-b)[:-4]
        self.assertEqual(result, '-198')
           
        a = BaseNum('5abcd', 16)
        b = BaseNum('d9ef', 16)
        result = str(a-b)[:-4]
        self.assertEqual(result, '4d1de')
            
        a = BaseNum('507002', 10)
        b = BaseNum('48679', 10)
        result = str(a-b)[:-4]
        self.assertEqual(result, '458323')
       
        a = BaseNum('101001', 2)
        b = BaseNum('11111', 2)
        result = str(a-b)[:-3]
        self.assertEqual(result, '1010')
       
        a = BaseNum('206005', 7)
        b = BaseNum('46346',7)
        result = str(a-b)[:-3]
        self.assertEqual(result, '126326')
        
        a = BaseNum('1', 10)
        b = BaseNum('2', 10)
        
        result = str( a - -b)[:-4]
        self.assertEqual(result, '3')
        
        result = str( -a - b)[:-4]
        self.assertEqual(result, '-3')
        
        result = str( -a - -b)[:-4]
        self.assertEqual(result, '1')
        
    def testTrueDiv(self):
        
        a = BaseNum('40231', 6)
        b = BaseNum('5', 6)
        result = str(a/b)[:-3]
        self.assertEqual(result, '4515')
        
        a = BaseNum('baca5', 16)
        b = BaseNum('f', 16)
        result = str(a/b)[:-4]
        self.assertEqual(result, 'c73e')
        
        a = BaseNum('caca', 16)
        b = BaseNum('a', 16)
        result = str(a/b)[:-4]
        self.assertEqual(result, '1447')
        
        result = str(-a/b)[:-4]
        self.assertEqual(result, '-1447')
        
        result = str(a/-b)[:-4]
        self.assertEqual(result, '-1447')
        
        result = str(-a/-b)[:-4]
        self.assertEqual(result, '1447')    
        
        a = BaseNum('7',10)
        b = BaseNum('8',10)
        
        result = str( a/b )[:-4]
        self.assertEqual(result, '0')
        
    def testMul(self):
        
        a = BaseNum('2febd',16)
        b = BaseNum('a', 16)
        result = str(a*b)[:-4]
        self.assertEqual(result, '1df362')
        
        a = BaseNum('9', 10)
        b = BaseNum('0', 10)
        result = str(a*b)[:-4]
        self.assertEqual(result, '0')
        
        a = BaseNum('0101', 2)
        b = BaseNum('1', 2)
        result = str(a*b)[:-3]
        self.assertEqual(result, '101')
        
    def testMod(self):
        
        a = BaseNum('10', 10)
        b = BaseNum('3', 10)
        result = str(a % b)[:-4]
        self.assertEqual(result, '1')
          
        a = BaseNum('af', 16)
        b = BaseNum('a', 16)
        result = str(a % b)[:-4]
        self.assertEqual(result, '5')
        
    def testConvertToBase10(self):

        
        a = BaseNum('0101', 2)
        b = BaseNum('5', 10)
        a = BaseNum.convert_to_base_10(a)
        
        self.assertEqual(a, b)
          
        a = BaseNum('a', 16)
        b = BaseNum('10', 10)
        a = BaseNum.convert_to_base_10(a)
        
        self.assertEqual(a, b)
        
    def testConvertFromBase10ToBase(self):
        
        a = BaseNum('af1', 16)
        b = a 
        a = BaseNum.convert_to_base_10(a)
        a = BaseNum.convert_from_base_10_to(a, 16)
        
        self.assertEqual(a, b)
        
        a = BaseNum('1314', 5)
        b = a 
        a = BaseNum.convert_to_base_10(a)
        a = BaseNum.convert_from_base_10_to(a, 5)
        self.assertEqual(a, b)
        
    def testConvertSuccessiveMethod(self):
        
        a = BaseNum('dafac', 16)
        
        b = BaseNum('896940', 10)
        c = BaseNum.convert_successive_divitions(a, b.base)
        self.assertEqual(c, b)
        
        b = BaseNum('3327654', 8)
        c = BaseNum.convert_successive_divitions(a, b.base)
        self.assertEqual(c, b)
        
        b = BaseNum('11011010111110101100', 2)
        c = BaseNum.convert_successive_divitions(a, b.base)
        self.assertEqual(c, b)
        
        a = BaseNum('2016', 10)
        
        b = BaseNum('3740', 8)
        c = BaseNum.convert_successive_divitions(a, b.base)
        self.assertEqual(c, b)
        
        b = BaseNum('11111100000', 2)
        c = BaseNum.convert_successive_divitions(a, b.base)
        self.assertEqual(c, b)
        
        a = BaseNum('a', 16)
        
        b = BaseNum('14', 6) 
        c = BaseNum.convert(a, b.base) 
        self.assertEqual(c, b)

    def testRapidConversionMethod(self):
        
        a = BaseNum('0101', 2)
        
        b = BaseNum('5', 8)
        c = BaseNum.convert_rapid_conversion(a, b.base)
        self.assertEqual(c, b)
        
        b = BaseNum('11', 4)
        c = BaseNum.convert_rapid_conversion(a, b.base)
        self.assertEqual(c, b)
        
        a = BaseNum('dafac', 16)
        
        b = BaseNum('3327654', 8)
        c = BaseNum.convert_rapid_conversion(a, b.base)
        self.assertEqual(c, b)
        
        b = BaseNum('11011010111110101100', 2)
        c = BaseNum.convert_rapid_conversion(a, b.base)
        self.assertEqual(c, b)
        
    def testConvertSubstitutionMethod(self):
        
        a = BaseNum('0101', 2)
         
        b = BaseNum('5', 10)
        c = BaseNum.convert_substitution_method(a, b.base)
        self.assertEqual(c, b)
          
        b = BaseNum('5', 8)
        c = BaseNum.convert_substitution_method(a, b.base)
        self.assertEqual(c, b)
          
        b = BaseNum('11', 4)
        c = BaseNum.convert_substitution_method(a, b.base)
        self.assertEqual(c, b)
          
        a = BaseNum('2016', 10)
          
        b = BaseNum('7E0', 16)
        c = BaseNum.convert_substitution_method(a, b.base)
        self.assertEqual(c, b)
        
        
        
    def testConvertBase10Intermediare(self):
        
        a = BaseNum('0101', 2)
        
        b = BaseNum('5', 10)
        a = BaseNum.convert_using_10_as_intermediare_base(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('5', 8)
        a = BaseNum.convert_using_10_as_intermediare_base(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('11', 4)
        a = BaseNum.convert_using_10_as_intermediare_base(a, b.base)
        self.assertEqual(a, b)
        
        a = BaseNum('dafac', 16)
        
        b = BaseNum('896940', 10)
        a = BaseNum.convert_using_10_as_intermediare_base(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('3327654', 8)
        a = BaseNum.convert_using_10_as_intermediare_base(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('11011010111110101100', 2)
        a = BaseNum.convert_using_10_as_intermediare_base(a, b.base)
        self.assertEqual(a, b)
        
        a = BaseNum('2016', 10)
        
        b = BaseNum('7E0', 16)
        a = BaseNum.convert_using_10_as_intermediare_base(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('3740', 8)
        a = BaseNum.convert_using_10_as_intermediare_base(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('11111100000', 2)
        a = BaseNum.convert_using_10_as_intermediare_base(a, b.base)
        self.assertEqual(a, b)
        
    def testConveret(self):
        
        a = BaseNum('0101', 2)
        
        b = BaseNum('5', 10)
        a = BaseNum.convert(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('5', 8)
        a = BaseNum.convert(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('11', 4)
        a = BaseNum.convert(a, b.base)
        self.assertEqual(a, b)
        
        a = BaseNum('dafac', 16)
        
        b = BaseNum('896940', 10)
        a = BaseNum.convert(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('3327654', 8)
        a = BaseNum.convert(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('11011010111110101100', 2)
        a = BaseNum.convert(a, b.base)
        self.assertEqual(a, b)
        
        a = BaseNum('2016', 10)
        
        b = BaseNum('7E0', 16)
        a = BaseNum.convert(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('3740', 8)
        a = BaseNum.convert(a, b.base)
        self.assertEqual(a, b)
        
        b = BaseNum('11111100000', 2)
        a = BaseNum.convert(a, b.base)
        self.assertEqual(a, b)
        
    
if __name__ == "__main__":
    unittest.main()