"""
this is a recursive module
"""
def print_lol(the_list):
	"""
	given the list, we can iterate each item (including list)
	"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
