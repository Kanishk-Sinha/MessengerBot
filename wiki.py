import wikipedia
import collections
# Named tuple for storing content
li = collections.namedtuple('list', ['title', 'url', 'content'])
elist = ''

def summ(str) :
	try :
		ny = wikipedia.page(str)
		nysum = wikipedia.summary(str, sentences = 5)
		title = ny.title.encode('utf-8')
		url = ny.url.encode('utf-8')
		content = nysum.encode('utf-8')
		p = li(title, url, content)
		return [p.title, p.url, p.content]

	except wikipedia.exceptions.DisambiguationError as err :
		return ['Error', 'Please enter a specific search string.']

	except wikipedia.exceptions.PageError as err :
		return ['Error', 'Uh, 404 not found! Please try searching something else.']

	except wikipedia.exceptions.WikipediaException as err :
		return ['Error', 'Please enter a search string to proceed.']


def full(str):
	ny = wikipedia.page(str)
	title = ny.title
	content = ny.content
	url = ny.url
	p = li(title, url, content)
	return [p.title, p.url, p.content]


