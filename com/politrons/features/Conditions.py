#################
#    IF/ELSE    #
#################

newFloat = float(10)
'''If/else condition in Python it use [:] after the condition instead [{] like in Java or Scala'''
if (isinstance(newFloat, float)) and newFloat == 10.0:
    print("We have a float " + str(newFloat))
else:
    print("Another type")

strVar = "Politrons"

'''The if condition also can use [or] operator. I like more than logic operators, make the code more readable'''
if strVar.startswith("X") or len(strVar) > 5: print("The String %s is correct" % strVar)

listOfNames = ["John", "Paul", "Esther"]

'''To find an element into an array in a condition is so simple like use [element] in [collection]'''
if "Paul" in listOfNames:
    print("Paul is part of the names %s" % listOfNames)
else:
    print("User not found")

if "Jack" not in listOfNames:
    print("Jack is not part of the list")

#################
#   For loops   #
#################
'''For operator it's quite powerful in Python. It's able to detect the type that you're passing and iterate over each element.
   In case of a String it will iterate characters, and if you pass a range it will apply the specify rules'''

'''Iterate with For in Python is so simple enough like [ for [iterable_value] in [collection]]'''
newList = []
for word in ["Hello", "Python", "World"]:
    newList.append(word.upper())
print(newList)

'''To just get character and iterate over String char by char you can use the same syntax of [for loop]'''
charList = []
for character in "Politrons":
    charList.append(character)
print(charList)

'''Range for an iteration it's so simple like use [range] operator passing from/to'''
for i in range(0, 5):
    print(i)

'''With [range] operator you can also pass a third argument to specify the increase number in the range, in this case 
0,2,4,6 '''
for i in range(0, 10, 2):
    print(i)

'''You can also repeat a specific number of times an operation just saying how may times you want in range'''
for _ in range(4):
    print("Repeat this operation")

'''To iterate a [Map] with for we can specify the key, value variables per iteration before [in] and in the map
    we need to use items() function to obtain entry per iteration'''
myMap = {"A":1,"B":2,"C":3,"D":4}
for key, value in myMap.items():
    print("Key %s" %key)
    print("Value %s" %value)


#################
#      Print    #
#################
'''Format String output using %s for String %d for digit, and follow the String with % to pass arguments'''
varStr = "interpolation"
print("This is how %s works" % varStr)

'''You can use a Tuple in case you want to pass two arguments into the String'''
varInt = 100
varStr = "String value"
print("Print number %d and String %s" % (varInt, varStr))

'''It also works fine for List, you just need to use %s as with any String value'''
listOfStr = ["Hello", "Python", "World"]
print("The content of the list %s " % listOfStr)
