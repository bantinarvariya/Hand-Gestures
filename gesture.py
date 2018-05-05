import cv2
import numpy as np
import math
import pygame
pygame.init()
import time

width=800
height=600

sound0 = pygame.mixer.Sound("0.wav")
gameDisplay=pygame.display.set_mode((width,height))
pygame.display.set_caption('hand gestures')
image = pygame.image.load('handmain.jpg')

clock=pygame.time.Clock()
black=(0, 0, 0)
white=(255, 255, 255)
red=(255, 0, 0)
grey=(128,128,128)
green=(50,205,50)

def mainback(x,y):
    gameDisplay.blit(image,(x,y))

def introscreen():
    intro =True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        gameDisplay.fill(white)
        mainback(0,0)

        # text on intro screen
        # font = pygame.font.SysFont(None, 40)
        # text = font.render("HAND GESTURES", True, black)
        # gameDisplay.blit(text,(150,370))

        # buttons on screen
        pygame.draw.rect(gameDisplay,(225,0,255),(280,550,60,30))
        pygame.draw.rect(gameDisplay,(255,0,255),(370,550,60,30))
        pygame.display.update()

        # button interaction
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        (a,b,c) = click

        (x,y)=mouse

        if 280<=x<=340 and 550<=y<=580:
            pygame.draw.rect(gameDisplay,green,(280,550,60,30))
            if a==1:
                gesturenumbers()
        elif 370<=x<=430 and 550<=y<=580:
            pygame.draw.rect(gameDisplay,red,(370,550,60,30))
            if a==1:
                quit()
        # font
        font = pygame.font.SysFont(None,25)
        text = font.render("START",True,white)
        gameDisplay.blit(text,(283,555))
        text = font.render("QUIT",True,white)
        gameDisplay.blit(text,(373,555))

        pygame.display.update()
        clock.tick(15)
def gesturenumbers():

    cap = cv2.VideoCapture(0)
    gameDisplay1=pygame.display.set_mode((1,1))
    while True:


        ret, img = cap.read()
        img = cv2.flip(img,1)
        img= cv2.resize(img,(800,600))
        cv2.rectangle(img,(350,350),(100,100),(0,255,0),0)
        crop_img = img[100:350, 100:350]
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        value = (5, 55)
        kernel = np.ones((3,3),np.uint8)
        dilated = cv2.erode(grey,kernel,iterations = 2)
        blurred = cv2.GaussianBlur(grey, value, 0)
        blurred1 = cv2.GaussianBlur(dilated, value, 0)
        _, thresh2 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


        _,contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
                cv2.CHAIN_APPROX_NONE)
        max_area = -1
        for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i
        cnt=contours[ci]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
        hull = cv2.convexHull(cnt)
        drawing = np.zeros(crop_img.shape,np.uint8)
        cv2.drawContours(drawing,[cnt],0,(0,255,0),1)
        cv2.drawContours(drawing,[hull],0,(0,0,255),2)
        hull1 = cv2.convexHull(cnt)
        areahull = cv2.contourArea(hull1)
        areacnt = cv2.contourArea(cnt)
        hull = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull)
        count_defects = 0
        #find the percentage of area not covered by hand in convex hull
        arearatio=((areahull-areacnt)/areacnt)*100
        cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            d=(2*ar)/a
            if angle <= 90 and d>30:
                count_defects += 1
                cv2.circle(crop_img,far,1,[0,0,255],-1)
            #dist = cv2.pointPolygonTest(cnt,far,True)
            cv2.line(crop_img,start,end,[0,255,0],2)
            #cv2.circle(crop_img,far,5,[0,0,255],-1)
        if count_defects < 1:
            if areacnt<2000:
                cv2.putText(img,'Put hand in the box',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            else:
                if arearatio<15:
                    cv2.putText(img,'0',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

                # elif arearatio <25:
                #     cv2.putText(img,'All THE BEST',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                else:
                    cv2.putText(img,'1',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

        elif count_defects == 1:
            if 30<arearatio< 40:
                arearatio
                # print(arearatio)
                cv2.putText(img,"2", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                # gesturewords()

            else:
                # print(arearatio)
                cv2.putText(img,"2", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 2:
            str = "3"
            cv2.putText(img,"3", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 3:
            cv2.putText(img,"4", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 4:
            cv2.putText(img,"5", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 5:
            cv2.putText(img,"6", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            gesturewords()
            break
        elif count_defects == 6:
            cv2.putText(img,"7 ", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 7:
            cv2.putText(img,"8", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 8:
            cv2.putText(img,"9 ", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 9:
            cv2.putText(img,"10", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        else:
            cv2.putText(img,"more", (50,50),\
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        #cv2.imshow('drawing', drawing)
        #cv2.imshow('end', crop_img)
        # cv2.imshow('Gesture', img)

        lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)


        #-----Splitting the LAB image to different channels-------------------------
        l, a, b = cv2.split(lab)


        #-----Applying CLAHE to L-channel-------------------------------------------
        clahe = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(10,10))
        cl = clahe.apply(l)


        #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
        limg = cv2.merge((cl,a,b))

        #-----Converting image from LAB Color model to RGB model--------------------
        img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        cv2.imshow('Gesture', img)


        all_img = np.hstack((drawing, crop_img))
        # cv2.imshow('Contours', all_img)

        ch = cv2.waitKey(1)
        if ch & 0xFF ==ord('q'):
            break
    gameDisplay1=pygame.display.set_mode((width,height))
    cap.release()
    cv2.destroyAllWindows()
def gesturewords():

    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        img = cv2.flip(img,1)
        img= cv2.resize(img,(800,600))
        cv2.rectangle(img,(350,350),(100,100),(0,255,0),0)
        crop_img = img[100:350, 100:350]
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        value = (5, 55)
        kernel = np.ones((3,3),np.uint8)
        dilated = cv2.erode(grey,kernel,iterations = 2)
        blurred = cv2.GaussianBlur(grey, value, 0)
        blurred1 = cv2.GaussianBlur(dilated, value, 0)
        _, thresh2 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


        _,contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
                                                 cv2.CHAIN_APPROX_NONE)
        max_area = -1
        for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i
        cnt=contours[ci]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
        hull = cv2.convexHull(cnt)
        drawing = np.zeros(crop_img.shape,np.uint8)
        cv2.drawContours(drawing,[cnt],0,(0,255,0),1)
        cv2.drawContours(drawing,[hull],0,(0,0,255),2)
        hull1 = cv2.convexHull(cnt)
        areahull = cv2.contourArea(hull1)
        areacnt = cv2.contourArea(cnt)
        hull = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull)
        count_defects = 0


        #find the percentage of area not covered by hand in convex hull
        arearatio=((areahull-areacnt)/areacnt)*100
        cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            d=(2*ar)/a
            if angle <= 90 and d>30:
                count_defects += 1
                cv2.circle(crop_img,far,1,[0,0,255],-1)
            #dist = cv2.pointPolygonTest(cnt,far,True)
            cv2.line(crop_img,start,end,[0,255,0],2)
            #cv2.circle(crop_img,far,5,[0,0,255],-1)
        if count_defects < 1:
            if areacnt<2000:
                cv2.putText(img,'Put hand in the box',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            else:
                if arearatio<10:
                    cv2.putText(img,'0',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                else:
                    cv2.putText(img,'like...! ',(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)


        elif count_defects == 1:
            if arearatio<30:
                cv2.putText(img,"call me", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                print(arearatio)
            elif arearatio<100:
                cv2.putText(img,"peace", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                print(arearatio)
        elif count_defects == 2:
            cv2.putText(img,"super", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 3:
            cv2.putText(img,"for you", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 4:
            cv2.putText(img,"high-five", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 5:
            arearatio
            # gesturenumbers()
        elif count_defects == 6:
            cv2.putText(img,"7 ", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            gesturenumbers()
        elif count_defects == 7:
            cv2.putText(img,"8", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 8:
            cv2.putText(img,"9 ", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 9:
            cv2.putText(img,"10", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        else:
            cv2.putText(img,"more", (50,50), \
                        cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        #cv2.imshow('drawing', drawing)
        #cv2.imshow('end', crop_img)
        # cv2.imshow('Gesture', img)

        lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)


#-----Splitting the LAB image to different channels-------------------------
        l, a, b = cv2.split(lab)


#-----Applying CLAHE to L-channel-------------------------------------------
        clahe = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(10,10))
        cl = clahe.apply(l)


#-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
        limg = cv2.merge((cl,a,b))

#-----Converting image from LAB Color model to RGB model--------------------
        img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        cv2.imshow('Gesture', img)

        all_img = np.hstack((drawing, crop_img))
        # cv2.imshow('Contours', all_img)

        h = cv2.waitKey(1)
        if h & 0xFF ==ord('q'):
            break


introscreen()