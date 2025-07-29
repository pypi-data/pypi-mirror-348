from os import _wrap_close
from .tcp_client import TCPClient
import hashlib
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
    return "v3.1.2"

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

'''