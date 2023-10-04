import math

#velocity = tafter
#scale is not vel but pos. inv.x**2 is acceptable.. which is log.
#https://www.mathportal.org/math-tests/tests-in-exponents-and-logarithms/logarithms.php?testNo=5
#math.log(0)=-inf / math.log(1)=0 / math.log(2.7) = 1
#y=5*log(x+1)
#f = lambda x:5*math.log(x+1)

E = math.e
log = math.log
E_1 = E-1

def explode_drag(t):
	"0->value , decreasing velocity. t=1,1."
	#t+1 is offset for t=0, f(0) = 0.
	#return log( (t+1)/2*E )
	return log( (E_1+t))
#but we need , t=1, t=9999 's value.
#ah, it's graph, now. like wave ..etc.

def main():
	for i in range(20):
		print( explode_drag(i/10))

if __name__ == '__main__':
	main()