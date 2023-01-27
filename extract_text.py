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
for page in reader.pages:
    text = page.extract_text()
    texts.append(text)

outfile = arguments['--out']
if outfile:
    with open(outfile, 'w') as o:
        o.write("\n".join(texts))
else:
    sys.stdout.write("\n".join(texts))
    sys.stdout.flush()

