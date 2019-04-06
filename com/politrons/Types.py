# Types
'''
Python since it´s not static type language but Dynamic, you dont have to specify types when you define variables.
The IDE will still inference the type and it will let you know the type pressing Ctrl + click
'''

###########
#   Int   #
###########
'''Python by default create numeric type as Int, so if you need to use just two bytes as Short, you cannot by default'''
intVar = 1
print(intVar)

#############
#   Float   #
#############
'''In order to create float types, you just need to create the number just with a dot or wrap the number with [float] function'''
standarFloat = 9.0
newFloat = float(10)
print(standarFloat)
print(newFloat)

##############
#   String   #
##############
'''In Python String declarations are not far different from another language. We can use quote or double quote to define the 
variable. '''
stringVar = "Hello Python world"
print(stringVar)
singleStr = 'Another way to do it'
print(singleStr)

'''If you want to put a String in upper or lower you just need to use [upper] [lower] operator'''
print(stringVar.upper())

'''You can repeat a String just multiplying for a number'''
repeatString = "Hello python world " * 5
print(repeatString)

'''Using index operator, you can extract the index of one character in your String. It will get the first index that found'''
strWithIndex = "POLITRONS".index("T")
print("Index value %s" % strWithIndex)

'''Using [count] function passing the character we can extract from the String the number of character of that type'''
numberOfCharacter = "POLITRONS".count("O")
print("Number of character of O its %s" % numberOfCharacter)

'''To subString a String you just need to add [from:to] after the String and it will create a new String from and to of the original'''
subStr = "POLITRONS"[4:9]
print("The new sub string is %s" % subStr)

'''Using this trick you can reverse a String, just wondering why reverse() it's not yet part of the API'''
reverseString = "HELLO WORLD"[::-1]
print("Str reverse %s" % reverseString)

'''Jus like in Java [split] function works getting the separator match and applying into the String '''
splitStr = "hello python world in array".split(" ")
print("The Str split into array %s" % splitStr)
