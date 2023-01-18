from itertools import count
import cv2
import numpy as np
import sUtils

path = "SIT Card Reader\/mcq.jpg"
path1 = "SIT Card Reader\/mcqDk.jpg"
#path1 does not work idk why lul
path2 = "SIT Card Reader\/mcqBlk.jpg"
path3 = "SIT Card Reader\/mcqBrdr.jpg"
img = cv2.imread(path)
scl = 0.3
#iWidth = int(img.shape[1] * scl)
#iHeight = int(img.shape[0] * scl)
iWidth = 900
iHeight = 700
questions = 10
choices = 4
ans = [3,1,1,3,2,1,0,1,0,0]


img = cv2.resize(img,(iWidth,iHeight))
imgEdit = img.copy()
imgContours = img.copy()
imgBiggestContours = img.copy()
imgGrey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGrey,(5,5),0)
#imgThresh = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)
#imgThresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 5)
imgThrsh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
#imgThrsh = cv2.threshold(imgBlur,130,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
imgCanny = cv2.Canny(imgThrsh,5,50)

#finding all contours
#contours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#print(contours)
#cv2.drawContours(imgContours,contours,-1,(0,255,0),5)

######### GRID DETECTION ##############
#https://maker.pro/raspberry-pi/tutorial/grid-detection-with-opencv-on-raspberry-pi
contours, _ = cv2.findContours(imgThrsh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

max_area = 0
c = 0
for i in contours:
        area = cv2.contourArea(i)
        if area > 100:
                if area > max_area:
                    max_area = area
                    best_cnt = i
        c+=1

mask = np.zeros((imgGrey.shape),np.uint8)
cv2.drawContours(mask,[best_cnt],0,255,-1)
cv2.drawContours(mask,[best_cnt],0,0,2)
#cv2.imshow("mask", mask)
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(mask,contours,-1,(0,255,0),5)

out = np.zeros_like(imgGrey)
out[mask == 255] = imgGrey[mask == 255]
#cv2.imshow("New image", out)

#######################################

imgBlur = cv2.GaussianBlur(out,(5,5),0)
imgCanny = cv2.Canny(imgBlur,10,80)

contours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
##################CHESSBOARD BORDER#######################

# get all non-zero points
points = np.column_stack(np.where(imgCanny.transpose() > 0))
hull = cv2.convexHull(points)

# draw convex hull vertices on input image
result = img.copy()
cv2.polylines(result, [hull], True, (0,0,255), 2)
##########################################################

#find Rectangles
#print(hull)
rectCon = sUtils.rectContour([hull])
biggestContour = sUtils.getCornerPoints(rectCon[0])

if biggestContour.size != 0:
    cv2.drawContours(imgBiggestContours, biggestContour,-1,(0,255,0),25)

    biggestContour = sUtils.reorder(biggestContour)

    pt1 = np.float32(biggestContour)
    pt2 = np.float32([[0,0], [iWidth, 0], [0, iHeight], [iWidth, iHeight]])
    matrix = cv2.getPerspectiveTransform(pt1,pt2)
    imgWarpColored = cv2.warpPerspective(img,matrix,(iWidth,iHeight))

    #apply bubble threshold
    imgWarpGrey = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpGrey,130,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #imgBlur = cv2.GaussianBlur(imgWarpGrey,(7,7),1)
    #imgThresh = cv2.adaptiveThreshold(imgWarpGrey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 9)
    #imgThreshcop = cv2.resize(imgThresh,(900,700))
    crop = imgThresh[130:498, 0:900]
    cv2.imshow('thr',crop)
    print(imgThresh.shape)

    #splitting bubbles
    #print(imgThreshcop.shape)
    boxes = sUtils.splitBoxes(crop)
    #cv2.imshow("test",boxes[36])
    #print (cv2.countNonZero(boxes[1]),cv2.countNonZero(boxes[2]),cv2.countNonZero(boxes[7]))

    myPixelVal = np.zeros((questions,choices))
    countCol = 0
    countRow = 0
    bIndex = 0

    #getting non zero vals of each bubble
    for image in range(0,len(boxes)):
        totalPixels = cv2.countNonZero(boxes[bIndex])
        myPixelVal[countRow][countCol] = totalPixels
        countCol += 1
        bIndex += 10
        if(countCol == choices): countRow += 1; countCol = 0; bIndex = countRow
    #print(myPixelVal)


    #Finding index vals of filled in bubbles
    myIndex = [] #array of filled in bubbles with choice val. a=0 b=1 c=2 d =3 e=4
    for x in range (0,questions) :
        arr = myPixelVal[x]
        myIndexVal = np.where(arr == np.amax(arr))
        #print(myIndexVal[0][0])
        myIndex.append(myIndexVal[0][0])

    #GRading
    grading = []
    for x in range (0, questions):
        if ans[x] == myIndex[x]:
            grading.append(1)
        else:
            grading.append(0)
    #print(grading)
    score = (sum(grading)/questions) * 100
    print(grading)
    print(score)
    #print(myIndex)

    imgResult = imgWarpColored.copy()
    imgResult = cv2.resize(imgResult,(900,700))
    imgResult = sUtils.showAnswers(imgResult,myIndex,grading,ans,questions,choices)


imgBlank = np.zeros_like(img)
imageArray = ([img,imgGrey,imgBlur,imgThresh],
    [imgCanny, result,imgBiggestContours, imgBlank])
imgStacked = sUtils.stackImages(imageArray,0.4)

cv2.imshow('Stacked Imgs',imgStacked)
cv2.imshow('result',imgResult)
cv2.waitKey(0)