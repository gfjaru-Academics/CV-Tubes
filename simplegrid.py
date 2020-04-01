import numpy as np
import cv2
 
img = cv2.imread('example.jpg') # read image, replace with yours
 
grid = 40 # determine grid size, rectangle with the same size of size
height = np.size(img, 0) # finding the height of the picture
width = np.size(img, 1) # finding the width of the picture
 
print(height) # print height on console to verify
print(width) # print width on console to verify
 
# compute the coordinate of height and width in each grid
h= [x for x in range(0,height) if x%grid==0]
w= [x for x in range(0,width) if x%grid==0]
 
print(h,np.size(h,0)) # print h grid on console to verify
print(w,np.size(w,0)) # print w grid on console to verify
 
# cv2.rectangle(resized,(h[0],0),(h[1],50),(0,255,0),0)
for i in range(0,np.size(w,0)-1):
    for j in range(0,np.size(h,0)-1):
        # draw rectangle (input image, [x1,y1],[x2,y2],RGB,thickness
        cv2.rectangle(img,(w[i],h[j]),(w[i+1],h[j+1]),(0,255,0),2)
 
#show the image
while (True):
    cv2.imshow('Judul Foto',img)
    k = cv2.waitKey(1) &amp; 0xFF
    if k == 27:  # wait for ESC key to exit
        break
cv2.destroyAllWindows()
