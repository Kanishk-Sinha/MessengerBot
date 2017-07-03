import sys
from PyDictionary import PyDictionary
import collections
dictionary = PyDictionary()
li = collections.namedtuple('retlist', ['pos', 'mean'])
def meaning(word) :
	try:
		pos = dictionary.meaning(word).keys()[0]
		m = dictionary.meaning(word).get(pos)
		p = li(pos, mean = m)
		return [p.pos, p.mean]
	except AttributeError :
		return ['Error', 'No meaning in the dictionary. Try another word!']
	except :
		return ['Error' ,'Unexpected error!']
		
# test data
# wr = 'SyBowl'
# print meaning(wr)