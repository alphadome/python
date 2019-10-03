# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:23:56 2019

@author: thoma
"""

import matplotlib.backends.backend_pdf
pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
for fig in xrange(1, figure().number): ## will open an empty extra figure :(
    pdf.savefig( fig )
pdf.close()