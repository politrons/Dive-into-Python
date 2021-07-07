#################
#    STANDARD   #
#################
''''Those are examples of how you invoke methods/functions in Python'''
def myFirstFunction():
    print("Hello python function!")

myFirstFunction()

'''As a Dynamic type language you dont have to specify the types. Because you know what you're doing XD!
   Functions can return values just using [return] keyboard'''

def funcWithArguments(arg1, arg2):
    return arg1 + arg2

def printSum(arg1, arg2):
    print("I hope I can sum this two args %s" % (funcWithArguments(arg1, arg2)))

printSum(10, 5)

'''Just like in Java we can define one or many arguments in the last line. The only thing since Python
   cannot tell the type in case is one or more objects, we need to define as list'''

def multiElementsLastArg(first, *many):
    print("First element %s" % first)
    print("Rest of elements %s" % (list(many)))

multiElementsLastArg(1, 2, 3, 4, 5, 6)

########################
#  MAP TRANSFORMATION  #
########################
'''With the standard library of python you can use functor transformation using [map] operator.
   instead of apply the map over the monad allow you for instance apply a lambda function over a
   collection'''
sentence = ["Hello", "Functional", "Python", "world"]

newSentence = map(lambda word: word.upper(), sentence)
print(list(newSentence))

'''Just like with [for] iterator the map will get the second argument and it will transform into an iterator'''
charsIterator = map(lambda char: char.upper(), "politrons")
print(list(charsIterator))

'''Also it's possible pass more iterables in the map and combine them'''
numbersTotal = map(lambda x, x1: x + x1, [1, 2, 3, 4, 5], [6, 7, 8, 9, 10])
print(list(numbersTotal))

########################
#   PARTIAL FUNCTION   #
########################
'''Using [partial] function allow us use Currying where involking a function return another function until we reach all
   thr attributes that the function need to apply'''
from functools import partial

def composeSentence(word: str, word1: str, word2: str):
    return word + " " + word1 + " " + word2

function = partial(composeSentence, "hello")
function1 = partial(function, "world")

print(function1("python"))

###################
#    FN LIBRARY   #
###################
from fn import _
from fn.op import zipwith
from itertools import repeat

assert list(map(_ * 2, range(5))) == [0,2,4,6,8]
assert list(filter(_ < 10, [9,10,11])) == [9]
assert list(zipwith(_ + _)([0,1,2], repeat(10))) == [10,11,12]