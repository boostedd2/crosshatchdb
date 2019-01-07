
import os, errno
from tkinter import *
import tkinter as tk
import subprocess
import threading
from subprocess import Popen, PIPE
import time
from tkinter import filedialog
import zipfile
import urllib.request
from tkinter.messagebox import askokcancel
import ctypes
import webbrowser
import shutil
from bs4 import BeautifulSoup
import requests
import hashlib
from queue import Queue, Empty
from itertools import islice

version = 'crosshatchdb v2.0'
newversion = ''
currentversion = ''

changelog = """
crosshAtchDB v2.0 ~ boostedduece - xda

######## USAGE GUIDE AND CHANGELOG BELOW ######################
######## CREDIT TO THE XDA COMMUNITY FOR ALL YOUR WORK ########

Features:
Install ADB
Unlock bootloader
Reboot to bootloader
Download and install factory images
Download and install TWRP
Download Magisk
Easy to use GUI
ADB logcat
Reboot ADB server
Kill ADB server
Nothing gets installed to your system, no drivers, registry entries, not even
any changes to your path.
The idea is that you can use this tool anywhere on any PC, then remove it
without leaving a trace.

Whats new?:
All new GUI inspired by dark material design and 'pixel blue' accent
Refactored most of the codebase
Better threading support
Open source code

This tool is completely free and I removed any links for donation, I made this
tool as a project to learn more about python and also for my own usage, especially
when I jump from different desktops/laptops in my home, just thought I would share it.




##############################################################################
# WARNING: I am not responsible for anything that goes wrong using this tool,#
#          it works fine on my windows 10 machine, and tested on windows 7.  #
#          However, make sure you know what these tools are doing beforehand.#
##############################################################################

Please let me know if you have any suggestions for the app, I will try and
implement them.

Enjoy!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
USAGE:

Install ADB the first time you run the tool. This will install the latest ADB for you.
you can also update ADB this way if needed.

Most of the options are self explained by th buttons.

Before booting TWRP, download the img and then select the img from "select TWRP Image".

ADB push will pop up a file selector to choose a file to send to your sdcard

Copy TiBu will copy TiBu folder to a selected folder on your PC

Copy TWRP will do the same as ^^

Downloads:
TWRP sends you to the page to download TWRP zips/img

To Download factory image, select and image, then press Download Factory Image,
This will also check the hash and auto extract all files, wait for it to finish
before doing anything else.

Magisk sneds you to Magisk thread for info/downloads.

Flash image will give you the option to remove '-w' from the flash-all bat.
MAKE SURE YOU SAVE THE FILE AFTER EDITING.
CAUTION: IF YOU DON'T REMOVE '-W' THIS WILL FACTORY RESET EVERYTHING.

To unlock bootloader, reboot to bootloader and click the unlock button.
This will factory reset your device, for security reasons, there is no way around this.

"""

class Quitter(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, fg='#2488f4', bg='black', text='Quit', command=self.quit)
        widget.pack(side=LEFT, expand=YES, fill=BOTH)

    def quit(self):
        ans = askokcancel('Verify exit', 'Really quit?')
        if ans: Frame.quit(self)

root = Tk()
#multiple calls - lambda:[printme(),adbdevices()]
#TWRP images list
fdir = os.path.join(os.environ['USERPROFILE'], "Downloads")
fllist = ['hit changelog button to refresh']
for file in os.listdir(fdir):
    if file.endswith(".img"):
        fllist.append(os.path.join(fdir, file))

#GUI
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs, background="#282828")
        self.parent = parent

        def tree():
            try:
                os.makedirs('c:\\crosshatch_stuff')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        def readme():
            cmd_box.insert('1.0', changelog)

        #List ADB devices
        def devices():
            cmd_box.delete('1.0',END)
            def runProcess():
                p = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\adb devices', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while(True):
                    # returns None while subprocess is running
                    retcode = p.poll()
                    line = p.stdout.readline()
                    yield line
                    if retcode is not None:
                        break
            def rp1():
                for line in runProcess():
                    cmd_box.insert(END, line)

            threading._start_new_thread(rp1, ())

        #Reboot bootloader
        def bootloader():
            cmd_box.delete('1.0',END)
            # start dummy subprocess to generate some output
            def runProcess():
                p = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\adb reboot bootloader', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while(True):
                    # returns None while subprocess is running
                    retcode = p.poll()
                    line = p.stdout.readline()
                    yield line
                    if retcode is not None:
                        break
            def rp1():
                for line in runProcess():
                    cmd_box.insert(END, line)
                cmd_box.insert(END, 'Pixel rebooted to bootloader.')

            threading._start_new_thread(rp1, ())

        #TWRP BOOT
        def twrpboot():
            cmd_box.delete('1.0',END)


            def runProcess():
                p = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\fastboot boot ' + var.get(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while(True):
                    # returns None while subprocess is running
                    retcode = p.poll()
                    line = p.stdout.readline()
                    yield line
                    if retcode is not None:
                        break
            def rp1():
                for line in runProcess():
                    cmd_box.insert(END, line)

            threading._start_new_thread(rp1, ())

        #Push via ADB
        def pushfile():
            cmd_box.delete('1.0',END)
            '''Redirects stdout from the method or function in module as a string.'''
            root = Tk()
            root.withdraw()
            filez = filedialog.askopenfilename()
            def runProcess(exe):
                p = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\adb push ' + filez + ' /sdcard', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while(True):
                    # returns None while subprocess is running
                    retcode = p.poll()
                    line = p.stdout.readline()
                    yield line
                    if retcode is not None:
                        break
            for line in runProcess('test'.split()):
                cmd_box.insert(END, line)

        def tbackup():
            cmd_box.delete('1.0',END)
            '''Redirects stdout from the method or function in module as a string.'''
            root = Tk()
            root.withdraw()
            filez = filedialog.askdirectory()
            def runProcess():
                p = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\adb pull /sdcard/TitaniumBackup ' + ' '+ filez, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while(True):
                    # returns None while subprocess is running
                    retcode = p.poll()
                    line = p.stdout.readline()
                    yield line
                    if retcode is not None:
                        break
            def rp1():
                for line in runProcess():
                    cmd_box.insert(END, line)

            threading._start_new_thread(rp1, ())

        def twbackup():
            cmd_box.delete('1.0',END)
            '''Redirects stdout from the method or function in module as a string.'''
            root = Tk()
            root.withdraw()
            filez = filedialog.askdirectory()
            def runProcess(exe):
                p = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\adb pull /sdcard/TWRP ' + ' '+ filez, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while(True):
                    # returns None while subprocess is running
                    retcode = p.poll()
                    line = p.stdout.readline()
                    yield line
                    if retcode is not None:
                        break
            for line in runProcess('test'.split()):
                cmd_box.insert('1.0', line)

        #adb logcat
        def adblog():
            cmd_box.delete('1.0',END)
            ans = askokcancel('ADB log', 'Starting ADB log, file will save as c:\\crosshatch_stuff\\logcat.txt, recreate the crash on your phone, Parse ADB logcat to stop, upload the log file or copy and paste the log to your developer.')
            if ans:
                subprocess.Popen(['cmd.exe', '/C', 'adb logcat > c:\\crosshatch_stuff\\logcat.txt'], cwd='C:\\crosshatch_stuff\\platform-tools')
                cmd_box.insert('1.0', 'Collecting ADB logcat, press parse logcat to stop logging.')

            #threading._start_new_thread(rp1, ())

        def parsedb():
            cmd_box.delete('1.0',END)
            os.system(r'C:\crosshatch_stuff\platform-tools\adb kill-server')
            with open('c:\\crosshatch_stuff\\logcat.txt', 'r') as parsefile:
                cmd_box.insert('1.0', parsefile.readlines())

        #killadb
        def killadb():
            cmd_box.delete('1.0',END)
            ans = askokcancel('Kill ADB', 'This will kill the ADB server, make sure your phone is not in the middle of flashing anything.')
            if ans:
                os.system(r'C:\crosshatch_stuff\platform-tools\adb kill-server')
                cmd_box.delete('1.0',END)
                cmd_box.insert('1.0', 'ADB sever was shutdown...')
        #cmd manual
        def manual():
            def cmd():
                subprocess.Popen(['cmd.exe'], cwd='C:\\crosshatch_stuff\\platform-tools')

            threading._start_new_thread(cmd, ())
        #xda page
        def xdapage():
            webbrowser.open('https://forum.xda-developers.com/pixel-3-xl/development/tool-crosshatchdb-one-pixel-3-xl-tool-t3864644')

            #install adb
        def adbinstall():
            tree()
            cmd_box.delete('1.0',END)
            cmd_box.insert('1.0', 'Installing ADB...')
            def theworks():
                os.system(r'C:\crosshatch_stuff\platform-tools\adb kill-server')
                '''Redirects stdout from the method or function in module as a string.'''
                urllib.request.urlretrieve('https://dl.google.com/android/repository/platform-tools-latest-windows.zip', r'C:\crosshatch_stuff\adbtools.zip')
                zip_ref = zipfile.ZipFile(r'C:\crosshatch_stuff\adbtools.zip', 'r')
                zip_ref.extractall(r'C:\crosshatch_stuff')
                zip_ref.close()
                cmd_box.delete('1.0',END)
                cmd_box.insert('1.0', 'ADB has been installed.')
            threading._start_new_thread(theworks, ())

        def twrpdown():
            webbrowser.open('https://twrp.me/google/googlepixel3xl.html')

        def magiskdown():
            webbrowser.open('https://forum.xda-developers.com/apps/magisk/official-magisk-v7-universal-systemless-t3473445')

        def bootunlock():
            ans = askokcancel('Verify unlock', 'WARNING: This will erase all data on the device, make sure you enable OEM unlock and adb debugging in developer options.')
            if ans: ans1 = askokcancel('Verify exit', 'Erase all data and unlock the bootloader?')
            if ans1: os.system(r'C:\crosshatch_stuff\platform-tools\fastboot flashing unlock'); os.system(r'C:\crosshatch_stuff\platform-tools\adb kill-server')

        def factoryimage():
            cmd_box.delete('1.0',END)
            '''Redirects stdout from the method or function in module as a string.'''

            ans = askokcancel('Factory Reset', 'WARNING: This will erase all data on the device, and restore factory settings.')
            if ans:
                ans1 = askokcancel('Factory Reset', 'Edit flash-all.bat before flashing? (Remove "-w" to keep data)')
                if ans1:
                    Popen(['notepad.exe', 'c:\\crosshatch_stuff\\platform-tools\\flash-all.bat'])
                    ans2 = askokcancel('Factory Reset', 'WARNING: MAKE SURE YOU EDITED THE FILE IN NOTEPAD. Last chance, flash factory image?')
                    if ans2:
                        cmd_box.delete('1.0',END)
                        def runProcess():
                            p = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\flash-all.bat', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='C:\\crosshatch_stuff\\platform-tools')
                            while(True):
                                # returns None while subprocess is running
                                retcode = p.poll()
                                line = p.stdout.readline()
                                yield line
                                if retcode is not None:
                                    break
                        def rp1():
                            for line in runProcess():
                                cmd_box.insert(END, line)

                        threading._start_new_thread(rp1, ())

                else:
                    ans3 = askokcancel('Factory Reset', 'WARNING: Last chance, flash factory image?')
                    if ans3:
                        cmd_box.delete('1.0',END)
                        def runProcess():
                            p = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\flash-all.bat', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='C:\\crosshatch_stuff\\platform-tools')
                            while(True):
                                # returns None while subprocess is running
                                retcode = p.poll()
                                line = p.stdout.readline()
                                yield line
                                if retcode is not None:
                                    break
                        def rp1():
                            for line in runProcess():
                                cmd_box.insert(END, line)

                        threading._start_new_thread(rp1, ())



        #download facotry image
        img_scrape = ['Scrape for images first!']
        def imgscraper():
            global img_scrape
            rurl = requests.get('https://developers.google.com/android/images')

            soup = BeautifulSoup(rurl.text, 'html.parser')

            soup = soup.find_all('table')[0]

            def get_links():
                llist = []
                for link in soup.find_all('a'):
                    llist.append(link.get('href'))
                return llist

            def get_hash():
                hl = []
                hashl = soup.find_all('td')
                for x in list(hashl):
                    if len(str(x)) == 73:
                            hl.append(str(x)[4:-5])
                return hl


            get_links()
            get_hash()
            img_scrape = (dict(zip(get_links(),get_hash())))
            return img_scrape

        def refresh():
            # Reset var and delete all old options
            var1.set('Select Factory Image')
            q['menu'].delete(0, 'end')

            # Insert list of new options (tk._setit hooks them up to var)
            new_choices = imgscraper()
            for choice in new_choices:
                q['menu'].add_command(label=choice, command=tk._setit(var1, choice))

        def refresh0():
            # Reset var and delete all old options
            var.set('Select TWRP Image')
            p['menu'].delete(0, 'end')

            # Insert list of new options (tk._setit hooks them up to var)
            new_choices = fllist
            for choice in new_choices:
                p['menu'].add_command(label=choice, command=tk._setit(var, choice))


        def downloadit():
            ans = askokcancel('INFO', 'This will download the factory image, check the SHA-256 hash provided by google, and then extract the zip to the correct folder, where you can then select the option to flash factory image. CHECK THE CONSOLE WINDOW FOR THE HASH ;-)')
            try:
                cmd_box.delete('1.0',END)
                cmd_box.insert('1.0', 'Downloading Factory image, please wait...')
                urllib.request.urlretrieve(var1.get(), 'c:\\crosshatch_stuff\\f_image.zip')
            except: cmd_box.insert(END, 'The Download Failed! Try again.')
            orig = str(imgscraper())
            filename = 'c:\\crosshatch_stuff\\f_image.zip'
            sha256_hash = hashlib.sha256()

            with open(filename,"rb") as f:
                        # Read and update hash string value in blocks of 4K
                        for byte_block in iter(lambda: f.read(4096),b""):
                            sha256_hash.update(byte_block)
                        check = sha256_hash.hexdigest()
                        print(orig)
                        print(check)

            if check in orig:
                cmd_box.delete('1.0',END)
                cmd_box.insert('1.0', '\n\n\nHash OK!, go ahead and flash the image.')
                cmd_box.insert('1.0', 'Your original hash was ' + check)
                imgfile = 'c:\\crosshatch_stuff\\f_image.zip'


                my_dir = r"c:\crosshatch_stuff\platform-tools"

                with zipfile.ZipFile(imgfile) as zip:
                    for zip_info in zip.infolist():
                        if zip_info.filename[-1] == '/':
                            continue
                        zip_info.filename = os.path.basename(zip_info.filename)
                        zip.extract(zip_info, my_dir)

            else:
                cmd_box.delete('1.0',END)
                cmd_box.insert('1.0','No good, try and download again!')

        def thread_downloadit():
            threading._start_new_thread(downloadit, ())

        def hasher(new_value):
            display.config(text = imgscraper()[new_value])

        def adbuninstall():
            ans = askokcancel('Uninstall tools', 'Uninstall all tools and delete factory image files. You will need to install adb again and download any image or zips if you delete them.')
            if ans:
                try:
                    shutil.rmtree(r"c:\crosshatch_stuff")
                except OSError as e:
                    print ("Error: %s - %s." % (e.filename, e.strerror))

        value=''
        #ADB
        statusbar = Label(self, text='CrosshAtchDB v2.0 -- Pixel 3 XL Flash Tool', fg='#4285F4', bg='#282828').grid(row=0, column=0, columnspan=3)
        uninstall_adb = Button(self, width=25, anchor='w', text='Uninstall ADB/Remove files', fg='red', bg='#212121', command=adbuninstall).grid(row=16, column=0)
        adb_tools = Label(self, text='Favorites                                         ', fg='#4285F4', bg='#282828').grid(row=1)
        adb_button = Button(self, width=25, anchor='w', text='Check for ADB device', fg='#4285F4', bg='#212121', command=devices).grid(row=2)
        bootloader_button = Button(self, anchor='w', width=25, text='Reboot to Bootloader', fg='#4285F4', bg='#212121', command=bootloader).grid(row=3)
        boot_twrp = Button(self, anchor='w', width=25, text='Boot selected TWRP', fg='#4285F4', bg='#212121', command=twrpboot).grid(row=4)
        adb_push = Button(self, anchor='w', width=25, text='ADB push file to /sdcard', fg='#4285F4', bg='#212121', command=pushfile).grid(row=6)
        tibu = Button(self, anchor='w', width=25, text='Copy /TiBu', fg='#4285F4', bg='#212121', command=tbackup).grid(row=7)
        twrpbu = Button(self, anchor='w', width=25, text='Copy /TWRP', fg='#4285F4', bg='#212121', command=twbackup).grid(row=8)
        adb_log = Button(self, anchor='w', width=25, text='Create logcat', fg='#4285F4', bg='#212121', command=adblog).grid(row=9)
        parse_adb = Button(self, anchor='w', width=25, text='Parse logcat', fg='#4285F4', bg='#212121', command=parsedb).grid(row=10)
        kill_adb = Button(self, anchor='w', width=25, text='Kill ADB server', fg='#4285F4', bg='#212121', command=killadb).grid(row=11)
        manual_adb = Button(self, anchor='w', width=25, text='Manual ADB prompt', fg='#4285F4', bg='#212121', command=manual).grid(row=12)
        resources_labal = Label(self, anchor='w', text='Resources                                       ', fg='#4285F4', bg='#282828').grid(row=13)
        changelog_crosshatch = Button(self, anchor='w', width=25, text='Changelog/Usage', fg='#4285F4', bg='#212121', command=lambda: [readme(), refresh0()]).grid(row=14)
        XDA_thread = Button(self, anchor='w', width=25, text='XDA crosshAtchDB Thread', fg='#4285F4', bg='#212121', comman=xdapage).grid(row=15)
        #options for boot twrp
        var = StringVar()
        var.set('Select TWRP image')
        p = OptionMenu(self, var, value, *fllist)
        p.config(anchor='w', width=24, fg='#4285F4', bg='#212121', highlightbackground='#212121')
        p.grid(row=5, padx=4)

        #Downloads
        Downloads_list = Label(self, anchor='w', width=25, text='Downloads', fg='#4285F4', bg='#282828').grid(row=1, column=2)
        install_adb = Button(self, anchor='w', width=25, text='Install ADB', fg='#4285F4', bg='#212121', command=adbinstall).grid(row=2, column=2)
        factory_image = Button(self, anchor='w', width=25, text='Download Factory Image', fg='#4285F4', bg='#212121', command=thread_downloadit).grid(row=4, column=2)
        scrape_image = Button(self, anchor='w', width=25, text='Scrape for Factory Images', fg='#4285F4', bg='#212121', command=lambda: [imgscraper(),refresh()]).grid(row=6, column=2)
        var1 = StringVar()
        var1.set('Select Factory Image')
        q = OptionMenu(self, var1, *img_scrape, command=hasher)
        q.config(anchor='w', width=24, fg='#4285F4', bg='#212121', highlightbackground='#212121')
        q.grid(row=5, column=2, padx=4)

        twrp_image = Button(self, anchor='w', width=25, text='TWRP', fg='#4285F4', bg='#212121', command=twrpdown).grid(row=3, column=2)
        magisk_button = Button(self, anchor='w', width=25, text='Magisk', fg='#4285F4', bg='#212121', command=magiskdown).grid(row=7, column=2)

        #additional
        flash_factory_stuff = Label(self, anchor='w', width=25, text='Flash Factory image', fg='#4285F4', bg='#282828').grid(row=13, column=2)
        flash_all_button = Button(self, anchor='w', width=25, text='Flash Image', fg='#4285F4', bg='#212121', command=factoryimage).grid(row=14, column=2)
        unlockbl_label = Label(self, anchor='w', width=25, text='Unlock Bootloader', fg='#4285F4', bg='#282828').grid(row=15, column=2)
        unlock_button = Button(self, anchor='w', width=25, text='Unlock', fg='#4285F4', bg='#212121', command=bootunlock).grid(row=16, column=2)

        #cmd
        cmd_box = Text(self, fg='#4285F4', bg='#212121')
        cmd_box.grid(row=1, rowspan=16, column=3, padx=4)
        vscroll = Scrollbar(self, orient=VERTICAL, command=cmd_box.yview)
        cmd_box['yscroll'] = vscroll.set
        vscroll.config(background='#313131', activebackground="#313131")
        vscroll.grid(row=1, rowspan=16, column=4, sticky=N+S)
        root.after(100, readme)


if __name__ == "__main__":
    root.title("crosshAtchDB v2.0")
    MainApplication(root).pack()
    root.protocol("WM_DELETE_WINDOW", lambda: Quitter.quit(root))
    root.mainloop()
