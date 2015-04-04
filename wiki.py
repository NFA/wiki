
import textwrap

def get_term_size():
   import subprocess
   columns = int(subprocess.check_output(['stty', 'size']).split()[1])
   return columns


def get_json_page(search):
   import urllib2
   url = 'http://en.wikipedia.org/w/api.php?continue=&action=query&titles={0}&prop=extracts&exintro=&explaintext=&format=json&redirects'
   query = url.format(search)
   page = urllib2.urlopen(query).read()
   return page

def print_json_page(page):
   import json
   data = json.loads(page)
   data = data['query']['pages']
   page_id = data.iterkeys().next()

   summary = data[page_id]['extract']
   summary = summary.replace('\n', '\n\n')

   import textwrap
   summary = textwrap.fill(summary, get_term_size())

   print(summary)



if __name__ == '__main__':
   import sys
   search = "_".join(sys.argv[1:])
   page = get_json_page(search)
   print_json_page(page)