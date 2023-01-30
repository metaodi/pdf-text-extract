#!/usr/bin/env python3
"""Extract text of given PDF file

Usage:
  extract_text.py [--file <path-to-pdf>] [--url <url-to-pdf] [--out <path-to-outfile>]
  extract_text.py (-h | --help)
  extract_text.py --version

Options:
  -h, --help                      Show this screen.
  --version                       Show version.
  -f, --file <path-to-pdf>        Path to PDF file.
  -u, --url <url-to-pdf>          URL to PDF file.
  -o, --out <path-to-outfile> Path to output file, defaults to stdout.

"""

import traceback
import sys
import os
import PyPDF2
import pandas as pd
from docopt import docopt
import download as dl


arguments = docopt(__doc__, version='Extract text from PDF file 1.0')
__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)

pdf_path = arguments['--file']
pdf_url = arguments['--url']

if not pdf_path and not pdf_url:
    raise ValueError("Must provide either file path or URL")

if pdf_url:
    content = dl.download_content(pdf_url)
    with io.BytesIO(content) as f:
        reader = PyPDF2.PdfReader(f)

if pdf_path:
    reader = PyPDF2.PdfReader(pdf_path)

texts = []

def visitor_body(text, cm, tm, font_dict, font_size):
    from pprint import pprint
    data = {
        'font_size': font_size,
        'text': text,
        'text_length': len(text),
        'cm': cm,
        'tm': tm,
    }
    data.update(font_dict)
    pprint(data)
    print("")

    texts.append(text)


for page in reader.pages:
    page.extract_text(visitor_text=visitor_body)
    #texts.append(text)

df_text = pd.DataFrame(texts)
df_agg = df_text.groupby(['font_size', '/Font']).agg(text_sum=('text_length', 'sum'))
print(df_agg)

outfile = arguments['--out']
if outfile:
    with open(outfile, 'w') as o:
        o.write("".join([t['text'] for t in texts]))
else:
    sys.stdout.write("".join([t['text'] for t in texts]))
    sys.stdout.flush()

