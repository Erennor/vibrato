
"""used for debug
simply comment print line to desactivate debug traces
"""

def print_debug(txt):
	print("[DEBUG] : " + txt)


class AdvancedBooleanAnalyser:


	def __init__(self, boolean):
		self.value = boolean


	def isTrue(self):
		""" return True if boolean == True
			else return False if boolean is not True.
			else, raise and catch a Value Error

			I should go back to work
		"""
		try:
			print_debug("Appel de isTrue sur "+ str(boolean))
			if self.boolean == True:
				return True
			elif self.boolean == False:
				return False
			else:
				raise ValueError
		except ValueError:
			print_debug("[DEBUG] :" + " ValueError")
		finally:
			pass


