# Input: a readwise CSV export from https://readwise.io/export
# Output: .md files for import to Roam

import sys
import csv
import os

READWISE_FIELDS = ['Highlight', 'Book Title','Book Author','Amazon Book ID','Note','Color','Tags','Location Type','Location']
OUTPUT_DIR = './output'

if not os.path.exists(OUTPUT_DIR):
  os.mkdir(OUTPUT_DIR)

if sys.argv[1:]:
  readwise_file = sys.argv[1]
else:
  readwise_file = 'readwise-data.csv'

content = {}

with open(readwise_file) as f:
  reader = csv.DictReader(f, READWISE_FIELDS)
  rows = [row for row in reader][1:] # ignore header
  for row in rows[:]:
    entry = content.setdefault(row['Book Title'], {
      'author': row['Book Author'],
      'highlights': []    
    })

    entry['highlights'].append({
      'highlight': row['Highlight'],
      'location': row['Location']
    })

for title, entry in content.items():
  output = f"""- #ReadwiseImport
- Author: {entry['author']}
- Highlights"""

  for highlight in sorted(entry['highlights'], key=lambda h: h['location']):
    output += "\n    - " + highlight['highlight'].replace('\n', '  ')

  filename = f"""{OUTPUT_DIR}/{title.replace('/','')}.md"""

  with open(filename, 'w') as f:
    f.write(output)

  print(output)