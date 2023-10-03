desc = """

we studied entire functools.
except single-dispatch, (that defines function  by arg types)

@cache(dangerous)

@lru_cache(maxsize=128)
-requires hash-able args

patial
2line->1line for def with argschange

patialmethod
..in a class.


from functools import wraps
is not learned.
seems more convenient decorator..

"""


#least- recent- kinds.
#when making shader.. cache..
#py had cache LHU kinds thing. with size.

#https://docs.python.org/3/library/functools.html

from functools import cache

@cache
def factorial(n):
    return n* factorial(n-1) if n else 1

factorial(10)
factorial(5)
factorial(12)


from functools import cached_property
from math import sqrt

class Shape:
	def __init__(self, points):
		self._data = points
	
	@cached_property
	def center(self):
		"of mass"
		dx,dy = 0,0
		for x,y in self._data:
			#dist = sqrt( x**2+y**2 )
			dx,dy = dx+x,dy+y
		return dx,dy

s = Shape( [[0,0],[1,1],[2,2],[-3,0] ] )
print(s.center)
#...how it works?
s._data = [ [0,0],[1,1] ]
print(s.center)
#as imagined. not changed.


from functools import lru_cache

@lru_cache(maxsize=128)
def center(points):
	dx,dy = 0,0
	for x,y in points:
		dx,dy = dx+x,dy+y
	return dx,dy

#hash-able!
#c = center( [[0,0],[1,1],[2,2],[-3,0] ] )
c = center( ((0,0),(1,1),(2,2),(-3,0)) )
print(c)
c = center( ((0,0),(1,1)) )
print(c)
c = center( ((0,0),(1,1)) )
print(c)

print( center.cache_info() )

#acceptable.
#close cased




#====================and functools


#================== use partial for avoid too many def func.
#since massive defs are overwhelming.

from functools import partial
import numpy as np

#int('10',base=2)
#partial(int,base=2)

f32arr = partial(np.array, dtype='float32')

a = np.array( [1,2,3],dtype = 'float32')
print(a)
a = f32arr([1,2,3])
print(a)

#but can't trace a function, by def statement.


#partial shortens def , more read-able. specially for functions array like N=20..
def order(x):
	return lambda x: print(x,end='!\n')
def ask(x):
	return lambda x: print(x,end='?\n')
# 4 lines=>
order = partial(print,end='!\n')
ask = partial(print,end='?\n')
# 2 line!
order('clean the room')
ask('clean the room')



class Window:
	def lock(self):
		"not directly used. nor attr. accesable.  the interface!"
		self._mouselock = True
		print(state,'!')
	def unlock(self):
		"not directly used. nor attr. accesable.  the interface!"
		self._mouselock = False
		print(state,'!')
	#this dirty, shares same logic.

	def _setlock(self, state):
		"not directly used. nor attr. accesable.  the interface!"
		self._mouselock = state
		print(state,'!')
	def lock(self):
		self._setlock(True)
	def unlock(self):
		self._setlock(False)
	#this better, but 4 lines for 2 methods! harmful for read-ablity. human works for machine.


#below shows minimum code, machine works for human.
from functools import partialmethod
class Window:
	def _set_mouselock(self,state):
		"not directly used. nor attr. accesable.  the interface!"
		self._mouselock = state
		print(state,'!')
	lock = partialmethod(_set_mouselock,True)
	unlock = partialmethod(_set_mouselock,False)

#wonderful, function in class' namespace.
w= Window()
w.lock()
w.unlock()
print(dir(w))

#but too many methods..
#extreamly shortens the code. acceptable!




from functools import reduce
def func(x,y):
	print(x,y)
	return x+y
mass = reduce(func, [1, 2, 3, 4, 5])
print(mass)
#inputs 1->2->3->4->

#not found way.












def func(x):
	if type(x) == int:
		print(i,'isint')
	elif type(x) == type(lambda:1):
		print(i,'isfunc')

#===========single dispatch  , def once, bremove if blocks.
#but hard to understand,/ use now.
#and -method, too.
from functools import singledispatch

@singledispatch
def func(arg):
	print(arg)

@func.register
def _(arg:int):
	print(arg,'int')
@func.register
def _(arg:float):
	print(arg,'int')


#stacking
@func.register(int)
@func.register(float)
def _(arg):
	print(arg,'int')



#with same line
from typing import Union
Union[int,float] #note []!

#below errors why??
# @func.register
# def _(arg: list|tuple):
# 	print(arg,'int')


def _(arg:Union[list,tuple] ):
	print(arg)
_('33')

Union[int]
Union[int,float]
Union[int,float,str]
