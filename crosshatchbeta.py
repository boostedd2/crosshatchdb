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
import hashlib
import webbrowser
import requests
from queue import Queue, Empty
from itertools import islice

msg = """

  crosshAtchDB b2.3 by boostedd

  CMD:             Action:
  --------------------------------------------------
  devices    - List attached devices
  bootloader - Reboot to bootloader
  twrp       - Boot TWRP image (Select image file on popup)
  push       - Push file to /sdcard
  boot.img   - Select a 'boot.img' E.g. magisk patched or stock
  flashoem   - Flash OEM factory image (guided)
  cmd        - Open CMD prompt in the platform-tools folder

  Extras:
  --------------------------------------------------
  install    - Install/Update ADB
  dltwrp     - Open download page for TWRP
  magisk     - Open magisk thread
  factory    - Open factory image download page
  changelog  - Open crosshatchdb thread

  [!] To unlock bootloader type "bootloader unlock" [!]
  [!] Erases all data and unlocks the bootloader    [!]
  [!] Turn on adb debug and enable unlock toggle    [!]

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
    process = subprocess.Popen('c:\\crosshatchdb\\platform-tools\\adb devices')
    process.wait()
    #subprocess.Popen('c:\\crosshatch_stuff\\platform-tools\\adb reboot bootloader')

def reboot_bootloader():
    os.system('cls')
    process = subprocess.Popen('c:\\crosshatchdb\\platform-tools\\adb reboot bootloader')

def boot_twrp():
    os.system('cls')
    root = Tk()
    root.withdraw()
    twrpimage = filedialog.askopenfilename()
    confirm = input('You selected ' + "'" + twrpimage + "'" + ' (y/n?): ')
    if confirm == 'y':
        process = subprocess.Popen('c:\\crosshatchdb\\platform-tools\\fastboot boot ' + twrpimage)
        process.wait()
    else: print('TWRP boot has been stopped.')

def pushfile():
    os.system('cls')
    root = Tk()
    root.withdraw()
    pushfile = filedialog.askopenfilename()
    confirm = input('You selected ' + "'" + pushfile + "'" + ' (y/n?): ')
    if confirm == 'y':
        process = subprocess.Popen('c:\\crosshatchdb\\platform-tools\\adb push ' + pushfile + ' /sdcard')
        process.wait()
    else: print('Push has been stopped, no files have been transferred.')

def boot_image():
    os.system('cls')
    input('Make sure you are in bootloader before flashing! -- Press "Enter" to continue.')
    root = Tk()
    root.withdraw()
    img = filedialog.askopenfilename()
    confirm = input('You selected ' + "'" + img + "'" + ' (y/n?): ')
    if confirm == 'y':
        process = subprocess.Popen('c:\\crosshatchdb\\platform-tools\\fastboot flash boot --slot all ' + img)
        process.wait()
    else: print('Flash has been stopped, boot.img has not been flashed.')

### FACTORY IMAGE ###

def check_hash():
    os.system('cls')
    user_in = input('Do you want to check the image sha-256 hash first? (y/n): ')
    if user_in == 'y':
        input('\nChoose the factory image you need to check. Press ENTER to continue.')
        root = Tk()
        root.withdraw()
        img = filedialog.askopenfilename()
        sha256_hash = hashlib.sha256()
        orig = input('Paste the sha-256 hash for your download: ')
        with open(img, "rb") as f:
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
            check = sha256_hash.hexdigest()
            
    
            if check in orig:
                print('\n\nFile Hash:')
                print(orig)
                print('\n')
                print('Provided Hash:')
                print(check)
                print('\n\n\nMATCH!\n')
    else:
        print('Skipping hash check...')

def extract_oem():
    os.system('cls')
    input('Press "Enter" and choose the factory image to extract.')

    my_dir = r"c:\crosshatchdb\platform-tools"

    root = Tk()
    root.withdraw()
    img = filedialog.askopenfilename()
    confirm = input('You selected ' + "'" + img + "'" + ' (y/n?): ')
    if confirm == 'y':
        try:
            with zipfile.ZipFile(img) as zip:
                for zip_info in zip.infolist():
                    if zip_info.filename[-1] == '/':
                        continue
                    zip_info.filename = os.path.basename(zip_info.filename)
                    zip.extract(zip_info, my_dir)
        except:
            print('Something went wrong try again.')

    else:
        print('Extract Factory image zip failed.')

def edit_bat():
    os.system('cls')
    user_in = input('Do you want to edit flashall.bat? (remove -w to preserve data) (y/n): ')
    if user_in == 'y':
        Popen(['notepad.exe', 'c:\\crosshatchdb\\platform-tools\\flash-all.bat'])
    else:
        confirm = input('WARNING: running flashall.bat without removing -w will perform a factory reset. (Press ENTER)')

# :-)
def final_flash():
    process = subprocess.Popen('c:\\crosshatchdb\\platform-tools\\flash-all.bat', cwd='C:\\crosshatchdb\\platform-tools')
    process.wait()

def flashoem():
    os.system('cls')
    check_hash()
    user_in = input('Do you want to extract the file?(required if you have not done this yet - y/n): ')
    if user_in == 'y':
        extract_oem()
    else:
        pass
    edit_bat()
    user_confirm = input('\n\n[!!!!] - Make sure you remove "-w" if needed. Again this will wipe data if "-w" is present. Type "confirm": ')
    if user_confirm == 'confirm':
        final_flash()
    else:
        input('\n\nOperation canceled. Enter to continue.')
        pass

def free_terminal():
    os.system('cls')
    process = subprocess.Popen('cmd.exe /K cd c:\\crosshatchdb\\platform-tools')
    process.wait()

def unlock_boot():
    os.system(r'C:\crosshatchdb\platform-tools\fastboot flashing unlock')
    
    

def twrpdown():
            webbrowser.open('https://twrp.me/google/googlepixel3xl.html')

def magiskdown():
            webbrowser.open('https://forum.xda-developers.com/apps/magisk/official-magisk-v7-universal-systemless-t3473445')

def factory_img_down():
            webbrowser.open('https://developers.google.com/android/images#crosshatch')

def xdapage():
            webbrowser.open('https://forum.xda-developers.com/pixel-3-xl/development/tool-crosshatchdb-one-pixel-3-xl-tool-t3864644')

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
        elif opt == 'boot.img':
            boot_image()
            input('\nPress ENTER to continue.')
        elif opt == 'factory':
            factory_img_down()
        elif opt == 'flashoem':
            flashoem()
        elif opt == 'cmd':
            free_terminal()
        elif opt == 'bootloader unlock':
            unlock_boot()
        elif opt == 'changelog':
            xdapage()
        