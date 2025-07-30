"""
this is a recursive module
"""
def print_lol(the_list,indent=False,level=0):
	"""
	given the list, we can iterate each item (including list)
	"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1)
		else:
			if indent == True:
				for i in range(level):
					print("\t",end="")
			print(each_item)
