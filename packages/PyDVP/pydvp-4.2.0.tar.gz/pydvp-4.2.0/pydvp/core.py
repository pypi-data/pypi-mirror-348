from os import _wrap_close
from .tcp_client import TCPClient
import hashlib
import xml.etree.ElementTree as ET
import time

class Window:
    name = '' 
    close = False
    zorder = 0
    opacity = 100
    input = 0
    left = 0.0
    top = 0.0
    width = 0.0
    height = 0.0
    crop_left = 0.0
    crop_top = 0.0
    crop_width = 100.0
    crop_height = 100.0
    keep_aspect_ratio = False
    transition_effect = "Cut"
    open_effect = "Cut"
    close_effect = "Cut"
    osd_mode = False
    osd_left = 19
    osd_top = 10    
    osd_line1 = ''
    osd_line2 = ''
    osd_background = True
    frame_mode = False
    frame_color = 0xC0FF;
    frame_width = 10.0
  
client = None

def version():
    return "v4.2.0"

def parse_windows(xml_string):
    root = ET.fromstring(xml_string)
    windows = []

    for win_elem in root.findall("window"):
        w = Window()
        w.name = win_elem.attrib.get("id", "")
        w.input = int(win_elem.attrib.get("input_id", 0))
        w.zorder = int(win_elem.attrib.get("zorder", 0))
        w.opacity = int(win_elem.attrib.get("opacity", 100))

        # placement
        placement = win_elem.find("placement")
        if placement is not None:
            w.left = float(placement.findtext("left", 0.0))
            w.top = float(placement.findtext("top", 0.0))
            w.width = float(placement.findtext("width", 0.0))
            w.height = float(placement.findtext("height", 0.0))

        # crop
        crop = win_elem.find("crop")
        if crop is not None:
            w.crop_left = float(crop.findtext("left", 0.0))
            w.crop_top = float(crop.findtext("top", 0.0))
            w.crop_width = float(crop.findtext("width", 100.0))
            w.crop_height = float(crop.findtext("height", 100.0))

        # aspect ratio
        aspect = win_elem.find("keepaspectratio")
        if aspect is not None:
            w.keep_aspect_ratio = aspect.text.strip().lower() == "yes"

        # frame
        frame = win_elem.find("frame")
        if frame is not None:
            w.frame_width = float(frame.attrib.get("left", 10))
            w.frame_color = int(frame.attrib.get("color", "0x000000"), 16)
            w.frame_mode = frame.text.strip().lower() == "yes"

        # osd
        osd = win_elem.find("osd")
        if osd is not None:
            w.osd_left = int(osd.attrib.get("left", 0))
            w.osd_top = int(osd.attrib.get("top", 0))
            w.osd_line1 = osd.attrib.get("line1", "")
            w.osd_line2 = osd.attrib.get("line2", "")
            w.osd_background = osd.attrib.get("background", "Yes").lower() == "yes"
            w.osd_mode = osd.text.strip().lower() == "yes"

        # effects
        w.transition_effect = win_elem.findtext("transition_eff", "Cut").strip('"')
        w.open_effect = win_elem.findtext("open_eff", "Cut").strip('"')
        w.close_effect = win_elem.findtext("close_eff", "Cut").strip('"')

        windows.append(w)

    return windows


def open(ip: str, port: int):
    global client 
    client = TCPClient(ip, port)
    client.connect()

def close():
    if client is None:
        raise ConnectionError("Client is not opened. Call open() first.")
    client.close()

def setup(user: str, passw: str, withReply = True):
    if client is None:
        raise ConnectionError("Client is not connected. Call open() first.")
    
    md5_pwd = hashlib.md5(passw.encode()).hexdigest()
    client.send_message("<setup><username>"+user+"</username><password>"+md5_pwd+"</password><needack>No</needack></setup>")
    response = client.receive_message()
    if withReply:
        return (f"{response}")    

def send_xml(xml):
    if client is None:
        raise ConnectionError("Client is not connected. Call open() first.")
    client.send_message(xml)
    response = client.receive_message()
    return (f"{response}")   

def query_windows():
    if client is None:
        raise ConnectionError("Client is not connected. Call open() first.")
    client.send_message("<query_windows_status />")
    response = client.receive_message()
    return (f"{response}")     
    
def take_close_all():
    if client is None:
        raise ConnectionError("Client is not connected. Call open() first.")
    client.send_message("<take_close_all />")

def recall_layout(id):
    if client is None:
        raise ConnectionError("Client is not connected. Call open() first.")
    client.send_message("<recall_layout id=\""+str(id)+"\" />")

def take(windows):
    if client is None:
        raise ConnectionError("Client is not connected. Call open() first.")
    
    cmd = "<take>"
    for w in windows: 
        if w.close:
            cmd += "<window id=\""+w.name+"\" input_id=\"Close\">"
        else:
            cmd += "<window id=\""+w.name+"\" input_id=\""+str(w.input)+"\" zorder=\""+str(w.zorder)+"\" opacity=\""+str(w.opacity)+"\">"
            cmd += "<placement><left>"+str(w.left)+"</left><top>"+str(w.top)+"</top><width>"+str(w.width)+"</width><height>"+str(w.height)+"</height></placement>"        
            cmd += "<crop><left>"+str(w.crop_left)+"</left><top>"+str(w.crop_top)+"</top><width>"+str(w.crop_width)+"</width><height>"+str(w.crop_height)+"</height></crop>"    
            cmd += "<keepaspectratio keep_dimension=\"Width\" keep_position=\"Center\">"
            if w.keep_aspect_ratio:
                cmd += "Yes</keepaspectratio>"
            else:
                cmd += "No</keepaspectratio>"   
            osd_bg = "Yes"
            if w.osd_background:
                osd_bg = "No"
            cmd += "<osd left=\""+str(w.osd_left)+"\" top=\""+str(w.osd_top)+"\" background=\""+osd_bg+"\" line1=\""+str(w.osd_line1)+"\" line2=\""+str(w.osd_line2)+"\">"
            if w.osd_mode:
                cmd += "Yes</osd>"
            else:
                cmd += "No</osd>"            
            cmd += "<open_eff duration=\"1\">\""+w.open_effect+"\"</open_eff>"
            cmd += "<transition_eff duration=\"1\">\""+w.transition_effect+"\"</transition_eff>"
            cmd += "<close_eff duration=\"1\">\""+w.close_effect+"\"</close_eff>"
            cmd += "<frame left=\""+str(w.frame_width)+"\" top=\""+str(w.frame_width)+"\" right=\""+str(w.frame_width)+"\" bottom=\""+str(w.frame_width)+"\" color=\""+str(w.frame_color)+"\">"
            if w.frame_mode:
                cmd += "Yes</frame>"
            else:
                cmd += "No</frame>"
                
        cmd += "</window>"
    cmd += "</take>"
    client.send_message(cmd)


#######

'''
print(version())
'''
'''
try:
    open("192.168.1.241", 6464)
except:
    print("ERROR LOGIN")    
    
try:
    setup("Administrator", "dexon", False)
except:
    print("ERROR SETUP")   
    
try:
    print(query_windows())
except:
    print("ERROR QUERY WINDOWS")  

try:
    take_close_all()
except:
    print("ERROR TAKE CLOSE ALL")  

try:
    w1 = Window()
    w1.name = "python_win1"
    w1.zorder = 0
    w1.input = 1
    w1.left = 0
    w1.top = 0
    w1.width = 640
    w1.height = 360

    w2 = Window()
    w2.name = "python_win2"
    w2.zorder = 1
    w2.input = 2
    w2.left = 640
    w2.top = 360
    w2.width = 640
    w2.height = 360
    
    w11 = Window()
    w11.name = "python_win1"
    w11.zorder = 0
    w11.input = 1
    w11.left = 1280
    w11.top = 0
    w11.width = 640
    w11.height = 360

    w21 = Window()
    w21.name = "python_win2"
    w21.zorder = 1
    w21.input = 2
    w21.left = 0
    w21.top = 720
    w21.width = 640
    w21.height = 360

    for count in range(5):
        take([w1, w2])
        time.sleep(5)
        take([w11, w21])
        time.sleep(5)
except:
    print("ERROR TAKE")  

try:
    close()
except:
    print("ERROR CLOSE")  
    
    
pypi-AgEIcHlwaS5vcmcCJDJmMzE4MzNjLTAyM2QtNGNiMC1iYzFjLTlmNjk3NGI3ZTYzNwACKlszLCJiZTM3ZDVkMy0yNDgyLTRkOTItYTc1My0wNjk1MTI2ZTkwY2UiXQAABiCWyMvpdMw7n6iCmcF0OLIyh18B0FIe_SStAs1QsMRNXA

python setup.py sdist bdist_wheel
twine upload dist/*

twine upload --config-file .pypirc  dist/* --verbose

'''