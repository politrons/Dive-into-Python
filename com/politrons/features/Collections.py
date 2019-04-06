###################
#      LIST       #
###################
'''
Collections in Python are easy enough to create, with just [] and some values it would be enough.
Since in Python all types are object, the compiler it will allow you add different types in the 
same list.
'''
myList = ["Hello", "Python", "World", 0]
print(myList)

'''[Append] it will append a new element at the end of the list'''
myListAppend = []
myListAppend.append("Hello")
myListAppend.append("Python")
myListAppend.append("World")
print(myListAppend[1])

'''[Copy] operator it will create a copy of the list'''
copyOfTheList = myListAppend.copy()
print(copyOfTheList)

'''To concat two list, it's so simple like just use [+]'''
listA = ["hello", "python"]
listB = ["World", "!!!!"]
print(listA + listB)

'''To repeat a list section, you just need to multiply the list by the number of times to repeat'''
repeatList = ["fight", "die", "repeat"] * 5
print(repeatList)

#########################
#   LIST COMPREHENSION  #
#########################
'''List comprehension it's a great feature since it allow you to create a filter new list defined a predicate function 
   Here we filter the other collection and for each string we put in upper case'''
sentence = "hello Python Java World"
filterList = [word.upper() for word in sentence.split() if word != "Java"]
print("Filter list %s" % filterList)

###################
#       MAP       #
###################
'''To create a map just need to use [{}] and use [:] to separate key from value.
   The IDE will inference the type and it will show you the available functions of that type
'''
myMap = {"key": "MapValue", "key1": "MapValue1"}
print("Nornal map %s " % myMap)

'''Use get function to extract the value for a specify key'''
print("Get value from map %s " % myMap.get("key1"))

'''Return an collection of Keys'''
print("Get keys from map %s " % myMap.keys())

'''Return a collection of values'''
print("Get values from map %s " % myMap.values())

'''To merge two maps you just need to use the expresion {**NameOfMap, **NameOfOtherMap, ......}'''
mapA = {"A": "a"}
mapB = {"B": "b"}
mergeMaps = {**mapA, **mapB}
print("Two maps merged %s" % mergeMaps)

'''To delete an element in a map we need to use [del] operator and pass in the array [key] to the element to delete'''
mapToDelete = {1: "1", "2": 2}
del mapToDelete[1]
print("Map after delete element %s" % mapToDelete)

'''You can also use the Map as queue so you can pop an element from the map by pop(key) updating the map with one element less.'''
mapToPop = {1: "1", "2": 2}
mapToPop.pop(1)
print("Map after pop element %s" % mapToPop)

###################
#      NUMPY      #
###################
'''
   A library extension to give more support to use array with Matrix and other types for calculations. 
   To install new modules in Python you just need to use [pip] command together with install and the name of the library
   For instance: pip install numpy.
   Numpy
'''
'''Create 2 new lists height and weight'''
height = [1.87, 1.87, 1.82, 1.91, 1.90, 1.85]
weight = [81.65, 97.52, 95.25, 92.98, 86.18, 88.45]

# Import the numpy package as np
import numpy as np

'''Create 2 numpy arrays from height and weight'''
np_height = np.array(height)
np_weight = np.array(weight)

print(type(np_height))

'''Calculate bmi'''
bmi = np_weight / np_height ** 2
print(bmi)

###################
#       SET       #
###################
'''Set it's pretty much like list with the standard behaviour that cannot have two elements with same value'''
mySet = set(["muchJake", "John", "Eric"])
print(mySet)

mySetUnique = set([1,2,3,4,3,2,1,5,4])
print(mySetUnique)