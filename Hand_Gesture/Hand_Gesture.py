# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 13:24:39 2020

@author: Ishan SS
"""

import cv2
import numpy as np
import math

#Open Camera
cap=cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()
    
    cv2.rectangle(frame,(100,100),(300,300),(0,255,0),1)
    crop_image=frame[100:300,100:300]
    
    imgCanny=cv2.Canny(crop_image,100,100)
    cv2.imshow("Edge",imgCanny)
    blur=cv2.GaussianBlur(crop_image,(3,3),0)
    hsv=cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
    
    mask=cv2.inRange(hsv,np.array([0,50,80]),np.array([30,200,255]))
    
    kernel=np.ones((5,5))
    
    dilation=cv2.dilate(mask,kernel,iterations=1)
    erosion=cv2.erode(mask,kernel,iterations=1)
    
    filtered=cv2.GaussianBlur(erosion,(3,3),0)
    ret,thresh=cv2.threshold(filtered,127,255,0)
    cv2.imshow("Thresholded",thresh)
    
    contours,_=cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    try:
        contour=max(contours,key=lambda x: cv2.contourArea(x))
        
        x,y,w,h=cv2.boundingRect(contour)
        cv2.rectangle(crop_image,(x,y),(x+w,y+h),(0,0,255),0)
        
        hull=cv2.convexHull(contour)
        
        drawing=np.zeros(crop_image.shape,np.uint8)
        drawing=cv2.drawContours(drawing,[contour],-1,(0,255,0),0)
        drawing=cv2.drawContours(drawing,[hull],-1,(0,0,255),0)
        
        hull=cv2.convexHull(contour,returnPoints=False)
        defects=cv2.convexityDefects(contour,hull)
        
        count_defects=0
        for i in range(defects.shape[0]):
            s,e,f,d=defects[i,0]
            start=tuple(contour[s][0])
            end=tuple(contour[e][0])
            far=tuple(contour[f][0])
            
            a=math.sqrt((end[0]-start[0])**2+(end[1]-start[1])**2)
            b=math.sqrt((far[0]-start[0])**2+(far[1]-start[1])**2)
            c=math.sqrt((end[0]-far[0])**2+(end[1]-far[1])**2)
            angle=(math.acos((b**2+c**2-a**2)/(2*b*c))*180)/3.14
            
            if angle<=90:
                count_defects+=1
                cv2.circle(crop_image,far,1,[0,0,255],-1)
                
            cv2.line(crop_image,start,end,[0,255,0],2)
        
        if count_defects==0:
            cv2.putText(frame,"One",(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
        elif count_defects==1:
            cv2.putText(frame,"Two",(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
        elif count_defects==2:
            cv2.putText(frame,"Three",(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
        elif count_defects==3:
            cv2.putText(frame,"Four",(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
        elif count_defects==4:
            cv2.putText(frame,"Five",(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
        else:
            pass
    except:
        pass
    
    cv2.imshow("Gesture",frame)
    all_image=np.hstack((drawing,crop_image))
    cv2.imshow("Contours",all_image)
        
    if cv2.waitKey(1)==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
        