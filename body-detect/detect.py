import numpy as np
import cv2 as cv
body_cascade = cv.CascadeClassifier('haarcascade_fullbody.xml')
upper_cascade = cv.CascadeClassifier('haarcascade_upperbody.xml')
lower_cascade = cv.CascadeClassifier('haarcascade_lowerbody.xml')
img = cv.imread('bagas.jpg')
scale_percent = 60 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)




bodies = body_cascade.detectMultiScale(
        gray,      
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30))
upper = upper_cascade.detectMultiScale(
        gray,       
        scaleFactor=1.1,
        minNeighbors=1,
        minSize=(30, 30))

for (x,y,w,h) in bodies:
    cv.rectangle(resized,(x,y),(x+w,y+h),(255,0,0),2)
    cv.putText(resized, str( ( ( (x+w)*(y+h) )/(width*height) ) ),  (x-10, y-10), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 


for (x,y,w,h) in upper:
    cv.rectangle(resized,(x,y),(x+w,y+h),(0,255,0),2)
    cv.putText(resized, str( ( ( (x+w)*(y+h) )/(width*height)  ) ),  (x-10, y-10), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 


cv.imshow('img',resized)
cv.waitKey(0)
cv.destroyAllWindows()
