An official DEXON DIVIP Python library

## Installation

Install the library using pip:

pip install PyDVP 

## Usage

import pydvp
import time

#open socket
pydvp.open("192.168.1.241", 6464)
#authentication
pydvp.setup("Administrator", "", False)

#query opened windows
xml_data = pydvp.query_windows()
#convert the given XML into a list of Window class instances 
windows = pydvp.parse_windows(xml_data)

#close all opened windows
pydvp.take_close_all()

#open a window
w1 = pydvp.Window()
w1.name = "python_win1"
w1.zorder = 0
w1.input = 1
w1.left = 0
w1.top = 0
w1.width = 640
w1.height = 360
pydvp.take([w1])

#recall layout by id
pydvp.recall_layout(1)

#close socket
pydvp.close()

## Contact

support@dexonsystems.com