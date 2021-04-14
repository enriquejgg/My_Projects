#!/Users/enriquejosegonzalezgarcia/Compartida/python/Projects Jupyter/final project/f_project/venv/bin/python

'''
usage:   nr-pdf-rotate.py my.pdf rotation result.pdf

        Rotation must be multiple of 90 degrees, clockwise.

Creates result.pdf with all rotated.

'''

import sys
import os

# import find_pdfrw
from pdfrw import PdfReader, PdfWriter

inpfn = sys.argv[1]
rotate = sys.argv[2]
outfn = sys.argv[3]

rotate = int(rotate)
assert rotate % 90 == 0

# ranges = [[int(y) for y in x.split('-')] for x in ranges]
trailer = PdfReader(inpfn)
pages = trailer.pages

ranges = [[1, len(pages)]]

for onerange in ranges:
    onerange = (onerange + onerange[-1:])[:2]
    for pagenum in range(onerange[0]-1, onerange[1]):
        pages[pagenum].Rotate = (int(pages[pagenum].inheritable.Rotate or 0) + rotate) % 360

outdata = PdfWriter()
outdata.trailer = trailer
outdata.write(outfn)

