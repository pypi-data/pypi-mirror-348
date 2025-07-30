"""
LibSrd 1.3.2
==================
Sam Davis

Commands
------------------
1. ```libsrd```
Displays the commands available in libsrd.  

2. ```mergepdfs```  
Will merge all pdf's found in the current directory, and save the result at: ./Output/Output.pdf  
  
3. ```imgconvert [args]```  
Will convert all images of ```InitalFormat``` in current directory to ```FinalFormat``` in ./Output/   

4. ```markhtml [args]```  
Will convert a markdown file to a html file.  

5. ```pdfresize```  
Will resize the all pdf's in current directory to a4.


Classes
---------------
1. Table  
A custom TSV reading and writing table class, that can read, write and parse.  

2. HtmlBuilder  
A very nice html building class, that is used to programatically build html files.   
"""

from libsrd.__version__ import __version__
from libsrd.htmlbuilder import HtmlBuilder
from libsrd.image_convert import convert_images
from libsrd.markhtml import Markdown
from libsrd.merge_pdf import merge_pdfs
from libsrd.pdf_resizer import resize_pdfs
from libsrd.table import Table


def _script():
	print(__doc__.replace("```", ""))