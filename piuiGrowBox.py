import functools
import os
import random
from time import strftime,sleep
from piui import PiUi

from stgs import stgs


current_dir = os.path.dirname(os.path.abspath(__file__))

def mainProcWrite(s):
  logs_file = open(os.path.join(current_dir,"pipe"), "a")
  logs_file.write(s)
  logs_file.close()

class DemoPiUi(object):

    def __init__(self):
        self.title = None
        self.txt = None
        self.img = None
        self.ui = PiUi(img_dir=os.path.join(current_dir, 'imgs'))

    def page_static(self):
        self.page = self.ui.new_ui_page(title="Static Content", prev_text="Back",
            onprevclick=self.main_menu)
        self.page.add_textbox("Add a mobile UI to your Raspberry Pi project", "h1")
        self.page.add_element("hr")
        self.page.add_textbox("You can use any static HTML element " + 
            "in your UI and <b>regular</b> <i>HTML</i> <u>formatting</u>.", "p")
        self.page.add_element("hr")
        self.page.add_textbox("Your python code can update page contents at any time.", "p")
        # update = self.page.add_textbox("Like this...", "h2")
        logBox = self.page.add_textbox("2015-04-17 10:39:51 Temp=12.5*C Hum=55.7% Moist=False\n time"
            + "<br /> newline", "pre")
        time.sleep(2)
        # for a in range(1, 5):
            # update.set_text(str(a))
            # time.sleep(1)
        lines = []
        with open(os.path.join(current_dir,'logs'), 'r') as content_file:
        # with open(os.path.join(current_dir,'stgs2.py'), 'r') as content_file:
              lines.append(content_file.read())
        message = '\n'.join(lines)
        logBox.set_text(message)

    def page_buttons(self):
        self.page = self.ui.new_ui_page(title="Commit changes", prev_text="Back", onprevclick=self.main_menu)
        self.title = self.page.add_textbox("", "h1")
        # plus = self.page.add_button("Up Button &uarr;", self.onupclick)
        minus = self.page.add_button("Commit &darr;", self.ondownclick)

    def page_input(self):
        self.page = self.ui.new_ui_page(title="Lights setup", prev_text="Back", onprevclick=self.main_menu)
        self.title = self.page.add_textbox("pPi time: "+strftime("%d-%X"), "h1")
        self.labelStart = self.page.add_textbox("Start [hour]: "+str(stgs.lightStart), "h2")
        self.txtStart = self.page.add_input("number", "new Start hour [0..23]")
        self.labelDuration = self.page.add_textbox("Duration [hour]: "+str(stgs.lightDuration), "h2")
        self.txtDuration = self.page.add_input("number", "new Duration hours [0..23]")
        button = self.page.add_button("Save", self.onlight)

    def page_treshold(self):
        self.page = self.ui.new_ui_page(title="Tresholds setup", prev_text="Back", onprevclick=self.main_menu)
        self.labelTemperature = self.page.add_textbox("Temperature [celsius]: "+str(stgs.temperature), "h2")
        self.txtTemperature = self.page.add_input("number", "new Temperature in celsius [0..100]")
        self.labelHumidity = self.page.add_textbox("Humidity [percentage]: "+str(stgs.humidity), "h2")
        self.txtHimidity = self.page.add_input("number", "new Humidity in percentage [0..100]")
        button = self.page.add_button("Save", self.ontreshold)

    def page_images(self):
        self.page = self.ui.new_ui_page(title="Images", prev_text="Back", onprevclick=self.main_menu)
        self.img = self.page.add_image("sunset.png")
        self.page.add_element('br')
        button = self.page.add_button("Change The Picture", self.onpicclick)

    def page_toggles(self):
        self.page = self.ui.new_ui_page(title="Toggles", prev_text="Back", onprevclick=self.main_menu)
        self.list = self.page.add_list()
        self.list.add_item("Lights", chevron=False, toggle=True, ontoggle=functools.partial(self.ontoggle, "lights"))
        self.list.add_item("TV", chevron=False, toggle=True, ontoggle=functools.partial(self.ontoggle, "tv"))
        self.list.add_item("Microwave", chevron=False, toggle=True, ontoggle=functools.partial(self.ontoggle, "microwave"))
        self.page.add_element("hr")
        self.title = self.page.add_textbox("Home Appliance Control", "h1")
        

    def page_console(self):
        con = self.ui.console(title="Console", prev_text="Back", onprevclick=self.main_menu)
        con.print_line("Hello Console!")

    def main_menu(self):
        self.page = self.ui.new_ui_page(title="Grow Box setup")
        self.list = self.page.add_list()
        self.list.add_item("Logs", chevron=True, onclick=self.page_static)
        self.list.add_item("Lights", chevron=True, onclick=self.page_input)
        self.list.add_item("Treshold", chevron=True, onclick=self.page_treshold)
        self.list.add_item("Pumps", chevron=True, onclick=self.page_input)
        self.list.add_item("Commit", chevron=False, onclick=self.page_buttons)
#        self.list.add_item("Images", chevron=True, onclick=self.page_images)
#        self.list.add_item("Toggles", chevron=True, onclick=self.page_toggles)
#        self.list.add_item("Console!", chevron=True, onclick=self.page_console)
        self.ui.done()


    def main(self):
        self.main_menu()
        self.ui.done()

    def onupclick(self):
        self.title.set_text("Up ")
        print "Up"

    def ondownclick(self):
        stgs_file = open("stgs2.py", "w")
        stgs_file.write("class Class(): pass\n"
          + "stgs=Class()\n\n")
        stgs_file.write("stgs.temperature = %s\n" % stgs.temperature)
        mainProcWrite  ("stgs.temperature = %s\n" % stgs.temperature)
        stgs_file.write("stgs.humidity = %s\n" % stgs.humidity)
        mainProcWrite  ("stgs.humidity = %s\n" % stgs.humidity)
        stgs_file.write("stgs.pomp1duration = %s\n" % stgs.pomp1duration)
        mainProcWrite  ("stgs.pomp1duration = %s\n" % stgs.pomp1duration)
        stgs_file.write("stgs.pomp2duration = %s\n" % stgs.pomp2duration)
        mainProcWrite  ("stgs.pomp2duration = %s\n" % stgs.pomp2duration)
        stgs_file.write("stgs.lightStart = %s\n" % stgs.lightStart)
        mainProcWrite  ("stgs.lightStart = %s\n" % stgs.lightStart)
        stgs_file.write("stgs.lightDuration = %s\n" % stgs.lightDuration)
        mainProcWrite  ("stgs.lightDuration = %s\n" % stgs.lightDuration)
        stgs_file.close()
        # call (["dir >lll"],shell=True)
        # os.spawnlp(os.P_NOWAIT,"screen top &")
        # call (["pkill -9 -f 'python /root/GrowBox/growRoom.py'"],shell=True)
        self.title.set_text("Saved..")

    def onlight(self):
        try:
          i = int(self.txtStart.get_text())
          if i>=0 and i<24: stgs.lightStart = i
          self.labelStart.set_text("Start [hour]: "+str(stgs.lightStart))
        except: None
        try:
          i = int(self.txtDuration.get_text())
          if i>=0 and i<24:  stgs.lightDuration = i
          self.labelDuration.set_text("Duration [hour]: "+str(stgs.lightDuration))
        except: None
        print "Start"

    def ontreshold(self):
        try:
          i = int(self.txtTemperature.get_text())
          if i>=0 and i<101: stgs.temperature = i
          self.labelTemperature.set_text("Temperature [celsius]: "+str(stgs.temperature))
        except: None
        try:
          i = int(self.txtHimidity.get_text())
          if i>=0 and i<101:  stgs.humidity = i
          self.labelHumidity.set_text("Humidity [percentage]: "+str(stgs.humidity))
        except: None
        print "Start"

    def onpicclick(self):
        if self.src == "sunset.png":
          self.img.set_src("sunset2.png")
          self.src = "sunset2.png"
        else:
          self.img.set_src("sunset.png")
          self.src = "sunset.png"

    def ontoggle(self, what, value):
        self.title.set_text("Toggled " + what + " " + str(value))

def main():
  piui = DemoPiUi()
  piui.main()

if __name__ == '__main__':
    main()
# ex: et sw=2 ts=2 nu
