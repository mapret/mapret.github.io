import os
import re
import sys
import urllib.request


project = sys.argv[1]
githublink = 'https://raw.githubusercontent.com/mapret/{}/master/README.md'
githublink = githublink.format(project)
print('Fetching ' + githublink)
text = urllib.request.urlopen(githublink).read().decode()
#text = open('scripts/README.md', 'r').read()
#print(text)

#text = text.replace('>', '&gt;')

#text = re.sub('^# (.*)', '<h1>\\1</h1>', text, 0, re.M)
#text = re.sub('^## (.*)', '<h2>\\1</h2>', text, 0, re.M)
#text = re.sub('^>(.*)', '<pre>\\1</pre>', text, 0, re.M)
#text = re.sub('```(.*?)```', '<pre>\\1</pre>', text, 0, re.S)

def getline():
	global text
	index = text.find('\n')
	line = text[:index]
	text = text[index+1:]
	return line

def peekline():
	global text
	index = text.find('\n')
	return text[:index]

def getlinesuntil(*string2):
	lines = []
	while True:
		if peekline() in string2:
			return '\n'.join(lines)
		lines.append(getline())

def getblockquote():
	lines = getlinesuntil('')
	lines = re.sub('^>', '', lines, 0, re.M)
	lines = re.sub('\n', '<br/>\n', lines)
	return lines

def gettext():
	return getlinesuntil('', '```')

text = text.replace('<', '&lt;')
text = re.sub('\\[(.*?)\\]\\((.*?)\\)', '<a href="\\2" target="_blank" rel="noopener">\\1</a>', text)

formattext = ''
while text != '':
	if text.startswith('\n'):
		getline()
	if text.startswith('# '):
		formattext += '<h1>' + getline()[2:] + '</h1>\n'
	elif text.startswith('## '):
		formattext += '<h2>' + getline()[3:] + '</h2>\n'
	elif text.startswith('```'):
		getline()
		formattext += '<pre>' + getlinesuntil('```') + '</pre>\n'
		getline()
	elif text.startswith('>'):
		formattext += '<blockquote>' + getblockquote() + '</blockquote>\n'
	else:
		formattext += '<p>' + gettext() + '</p>\n'

formattext = re.sub('```(.*?)```', '<span class="inline-pre">\\1</span>', formattext)

template = open('scripts/index.html.tmpl').read()
template = template.replace('{{Title}}', project)
template = template.replace('{{Body}}', formattext)

if not os.path.exists(project):
	os.mkdir(project)
open(project + '/index.html', 'w').write(template)
