import os
from bs4 import BeautifulSoup

def scanHTMLFile(filepath):
	soup = BeautifulSoup(open(filepath, encoding='utf-8'), 'html.parser')
	print(soup.title)



def traverseFiles():
	
	for subdir, dirs, files in os.walk(".\\recipes"):
		
		for file in files:
			filepath = subdir + os.sep + file

			if filepath.endswith(".html"):
				scanHTMLFile(filepath)



if __name__ == '__main__':
	traverseFiles()
