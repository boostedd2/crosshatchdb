import os, errno
from tkinter import *
import tkinter as tk
import subprocess
from subprocess import Popen, PIPE
import time
from tkinter import filedialog
import zipfile
import urllib.request
from tkinter.messagebox import askokcancel
import ctypes
import webbrowser
import requests
from queue import Queue, Empty
from itertools import islice

msg = """

  crosshAtchDB b2.2

  CMD:             Action:
  --------------------------------------------------
  devices    - List attached devices
  bootloader - Reboot to bootloader
  twrp       - Boot TWRP image (Select image file on popup)
  push       - Push file to /sdcard

  Extras:
  --------------------------------------------------
  install    - Install/Update ADB
  dltwrp     - Open download page for TWRP
  magisk     - Open magisk thread

"""



def create_root_dir():
    try:
        os.makedirs('c:\\crosshatchdb')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def download_adb():
    try:
        os.system(r'C:\crosshatchdb\platform-tools\adb kill-server')
    except:
        pass
    os.system('cls')
    print('Installing latest ADB version, please wait...')
    #Grab the latest adb zip from google
    urllib.request.urlretrieve('https://dl.google.com/android/repository/platform-tools-latest-windows.zip', 
    r'C:\crosshatchdb\adbtools.zip')
    #extract the zip
    zip_ref = zipfile.ZipFile(r'C:\crosshatchdb\adbtools.zip', 'r')
    zip_ref.extractall(r'C:\crosshatchdb')
    zip_ref.close()

def check_adb_devices():
    os.system('cls')
    process = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\adb devices')
    process.wait()
    #subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\adb reboot bootloader')

def reboot_bootloader():
    os.system('cls')
    process = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\adb reboot bootloader')

def boot_twrp():
    os.system('cls')
    root = Tk()
    root.withdraw()
    twrpimage = filedialog.askopenfilename()
    confirm = input('You selected ' + "'" + twrpimage + "'" + ' (y/n?): ')
    if confirm == 'y':
        process = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\fastboot boot ' + twrpimage)
        process.wait()
    else: print('TWRP boot has been stopped.')

def pushfile():
    os.system('cls')
    root = Tk()
    root.withdraw()
    pushfile = filedialog.askopenfilename()
    confirm = input('You selected ' + "'" + pushfile + "'" + ' (y/n?): ')
    if confirm == 'y':
        process = subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\adb push ' + pushfile + ' /sdcard')
        process.wait()
    else: print('Push has been stopped, no files have been transferred.')


def twrpdown():
            webbrowser.open('https://twrp.me/google/googlepixel3xl.html')

def magiskdown():
            webbrowser.open('https://forum.xda-developers.com/apps/magisk/official-magisk-v7-universal-systemless-t3473445')

if __name__ == '__main__':
    create_root_dir()
    while True:
        os.system('cls')
        print(msg)
        opt = input('  Type your command: ')
        if opt == 'install':
            download_adb()
            input('ADB Installed, press ENTER to continue.')
        elif opt == 'devices':
            check_adb_devices()
            input('\nPress ENTER to continue.')
        elif opt == 'bootloader': 
            reboot_bootloader()
        elif opt == 'twrp':
            boot_twrp()
            input('\nTWRP booted, Press ENTER to continue.')
        elif opt == 'dltwrp':
            twrpdown()
        elif opt == 'magisk':
            magiskdown()
        elif opt == 'push':
            pushfile()
            input('\nPress ENTER to continue.')
        