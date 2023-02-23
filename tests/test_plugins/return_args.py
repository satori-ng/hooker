import hooker


@hooker.hook("return_args")
def return_args_1(a, b):
	print("'return_args_1' function - args '%s, %s'" %(a,b))
	return a, b, 'test'
