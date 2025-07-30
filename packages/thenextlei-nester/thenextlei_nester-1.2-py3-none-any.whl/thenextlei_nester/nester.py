"""
this is a recursive module
"""
def print_lol(the_list,level=0):
	"""
	given the list, we can iterate each item (including list)
	"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for i in range(level):
				print("\t",end="")
				print(each_item)
