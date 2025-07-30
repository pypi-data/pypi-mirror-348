"""
this is a recursive module
"""
def print_lol(the_list,level):
	"""
	given the list, we can iterate each item (including list)
	"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			tl = level
			while tl > 0:
				print("\t",end="")
				tl = tl -1
			print(each_item)
