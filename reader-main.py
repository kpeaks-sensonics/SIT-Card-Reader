from csv import reader
from itertools import count
import cv2
import numpy as np
import keyboard
import sUtils
import ryanReader as rr

def startGrade():
    group = input("Please enter Group, then press enter: ")
    name = input("Please enter Name, then press enter: ")
    sex = input("Please enter Sex, then press enter: ")
    age = input("Please enter Age, then press enter: ")
    smoke = input("Please enter Smoke, then press enter: ")
    pack = input("Please enter Pack Years, then press enter: ")
    test1 = input("Please enter Test 1 Date, then press enter: ")
    test2 = input("Please enter Test 2 Date, then press enter: ")
    education = input("Please enter Education, then press enter: ")
    occupation = input("Please enter Occupation, then press enter: ")
    occuCode = input("Please enter Occupation Code, then press enter: ")
    ethnic = input("Please enter Ethnicity, then press enter: ")
    meds = input("Please enter Medication, then press enter: ")
    medsName = input("Please enter Medication Name, then press enter: ")

    print("Please place Booklet 1 under the camera.")
    print("Once in postion, press Ctrl to grade Booklet 1")
    keyboard.wait('Ctrl')
    bk1 = rr.reader(1)

    print("Please place Booklet 2 under the camera.")
    print("Once in postion, press Ctrl to grade Booklet 2")
    keyboard.wait('Ctrl')
    bk2 = rr.reader(2)

    print("Please place Booklet 3 under the camera.")
    print("Once in postion, press Ctrl to grade Booklet 3")
    keyboard.wait('Ctrl')
    bk3 = rr.reader(3)

    print("Please place Booklet 4 under the camera.")
    print("Once in postion, press Ctrl to grade Booklet 4")
    keyboard.wait('Ctrl')
    bk4 = rr.reader(4)

    print(group)
    print(name)
    print(sex)
    print(age)
    print(smoke)
    print(pack)
    print(test1)
    print(test2)
    print(education)
    print(occupation)
    print(occuCode)
    print(ethnic)
    print(meds)
    print(medsName)
    print(bk1)
    print(bk2)
    print(bk3)
    print(bk4)

def main():
    print ("Hello Ryan")
    while True:
        print("To end program, press q")
        print("To start grading, press g")
        if keyboard.read_key(suppress=True) == "q":
            break
        if keyboard.read_key(suppress=True) == 'g':
            startGrade()

    print("done")

main()