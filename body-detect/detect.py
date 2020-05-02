import numpy as np
import cv2 as cv
body_cascade = cv.CascadeClassifier('haarcascade_fullbody.xml')
upper_cascade = cv.CascadeClassifier('haarcascade_upperbody.xml')
lower_cascade = cv.CascadeClassifier('haarcascade_lowerbody.xml')
img = cv.imread('orang.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)



bodies = body_cascade.detectMultiScale(
        gray,      
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30))
upper = upper_cascade.detectMultiScale(
        gray,       
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30))
lower = lower_cascade.detectMultiScale(
        gray,     
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30))

for (x,y,w,h) in bodies:
    cv.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
    cv.putText(img, str( ( ( (x+w)*(y+h) )/(w*h) ) ),  (x-10, y-10), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 


for (x,y,w,h) in upper:
    cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    cv.putText(img, str( ( ( (x+w)*(y+h) )/(w*h) ) ),  (x-10, y-10), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 

for (x,y,w,h) in lower:
    cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    cv.putText(img, str( ( ( (x+w)*(y+h) )/(w*h) ) ),  (x-10, y-10), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 

cv.imshow('img',img)
cv.waitKey(0)
cv.destroyAllWindows()