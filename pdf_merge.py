'''
consolidate relevant Python cheat sheets from datacamp.com
into a single file

Packages: os
          PyPDF2

'''

import os
from PyPDF2 import PdfWriter
merger = PdfWriter()

# prior wd = = C:\Users\zacha\PycharmProjects

os.chdir("C:/Users/zacha/OneDrive/Documents/Data Work/Misc Files/Cheat_Sheets")

for pdf in ['1.pdf', '2.pdf', '3.pdf', '4.pdf', '5.pdf', '6.pdf', '7.pdf', '8.pdf', '9.pdf', '10.pdf', '11.pdf','12.pdf','13.pdf']:
    merger.append(pdf)

merger.write("cheat_sheet.pdf")
merger.close()

os.chdir("C:\Users\zacha\PycharmProjects")
