from oslash import Left, Right, Just, Nothing

'''
One great library to play with Monads is [oslash] to install it just use [pip] command [pip install oslash]
'''
###################
#      MAYBE      #
###################
'''Maybe Monad is based in Haskell Monad, it contains the monad type Just which contains the value, and the Monad
   Nothing which it does not contain any value'''
just = Just("I think therefor I am")
print(just)
nothing = Nothing()
print(nothing)

'''Transformation with Maybe as Functor it's pretty much the same as in Scala, you just use [map] operator.'''
justResult = Just("Hello") \
    .map(lambda word: word + " maybe") \
    .map(lambda word: word + " python") \
    .map(lambda word: word + " world") \
    .map(lambda word: word.upper())

print(justResult)

'''In case of type Nothing none function will be apply in the pipeline.'''
nothingResult = Nothing() \
    .map(lambda word: word + " maybe") \
    .map(lambda word: word + " python") \
    .map(lambda word: word + " world") \
    .map(lambda word: word.upper())

print(nothingResult)

###################
#      EITHER     #
###################
'''Using the oslash library we just need to create the Right or Left monad passing the value'''
right = Right(1)
print(right)
left = Left("Error")
print(left)

'''In case you want to do composition, we need to use [\] [bind] operator and return a Right in the transformation.
   In case of Left it will not evaluate the lambda and it will pass just the monad'''

newValue = right \
    .bind(lambda x: Right(x + 1980)) \
    .bind(lambda x: x * 10)

print(newValue)

'''Another way to use composition instead of [bind] it's using [|] operator, less  verbose right?'''
rightResult = Right("Hello") | \
              (lambda word: Right(word + " Functional")) | \
              (lambda word: Right(word + " Python")) | \
              (lambda word: Right(word + " world")) | \
              (lambda word: Right(word.upper()))
print(rightResult)

newError = left.bind(lambda x: x + 1981)
print(newError)
