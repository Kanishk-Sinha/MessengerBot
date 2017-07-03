import math

def calc(func, a, b) :
	if func == 'add' :
		return a + b
	if func == 'sub' :
		return a - b
	if func == 'mul' :
		return a * b
	if func == 'div' :
		return a / b
	if func == 'pow' :
		return math.pow(a, b)
