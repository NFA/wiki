
def get_term_size():
   try:
      import os
      columns = os.get_terminal_size().columns
   except AttributeError:
      try:
         import subprocess
         columns = int(subprocess.check_output(['stty', 'size']).split()[1])
      except OSError:
         columns = 80
   return columns

def get_json_page(search):
   url = 'http://en.wikipedia.org/w/api.php?continue=&action=query&titles={0}&prop=extracts&exintro=&explaintext=&format=json&redirects'
   query = url.format(search)
   try:
      import urllib2
      page = urllib2.urlopen(query).read()
   except ImportError:
      import urllib.request
      page = urllib.request.urlopen(query).read().decode("utf-8")
   return page

def print_json_page(page):
   import json
   data = json.loads(page)
   data = data['query']['pages']
   page_id = list(data.keys())[0]

   if page_id == '-1':
      page_title = data['-1']['title']
      summary = "Wiki article missing. Check spelling of '{0}'.".format(page_title)
   else:
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