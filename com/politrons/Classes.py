"""In Python To create Class is just like any other OOP language, we use [class]
   Just like the rest of the language we use : instead of {}.
   Inside the class you can create variables and methods that can be accessed from
   once the instance it's created. For method we need to use self(The Java this) in method attributes in case we dont receive
   any argument, and to access global variable of the class we need to use instead [this.] of Java but [self.]
   also in Python the way to make a method private it's using double underscore before method __foo
"""


class MyFirstPythonClass:
    variable = "Custom value"

    def getCustomValue(self): return self.variable

    def secondMethod(self, arg): return self.__privateMethod(arg)

    def __privateMethod(self, arg): return arg + 100

    @staticmethod
    def staticMethod(arg): return arg * 100


'''In Python you dont have to use [new] like in Java to create a class. you just need use () like if a case of Scala was. '''
myClass = MyFirstPythonClass()
print(myClass)
print(myClass.getCustomValue())

'''Not fan at all about mutability, but Python allow you mutate global variables in classes.'''
myClass.variable = "New value"
print(myClass.variable)

'''To create and use Static method in Python, you need to add annotation [@staticmethod]'''
number = MyFirstPythonClass.staticMethod(10)
print(number)

'''In this example we invoke a public method passing an argument and this one invoke a private method'''
sumValues = MyFirstPythonClass().secondMethod(100)
print("Invoke private method %s" % sumValues)
