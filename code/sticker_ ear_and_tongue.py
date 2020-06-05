import cv2
import datetime
import os

#these are the cascades: thay are already present in the opencv
cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml') 
cascade_smile = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_smile.xml')

#function ot detect the face

# gray image of our face, original image:
def detection(grayscale, img):
    
    #1.3 is the scale factor , 5 is te min neighbours
    face = cascade_face.detectMultiScale(grayscale, 1.3, 5)
    
    #4 corrdinates in faces
    for (x_face, y_face, w_face, h_face) in face:
        
        #draw rectangle
        #cv2.rectangle(img, (x_face, y_face), (x_face+w_face, y_face+h_face), (255, 130, 0), 2)
        
       
        #area of intreset in gray image
        ri_grayscale = grayscale[y_face:y_face+h_face, x_face:x_face+w_face]
        
        #area of intrest in coloured image
        ri_color = img[y_face:y_face+h_face, x_face:x_face+w_face] 
        
        # smile detection , 1.7 is the scale factor , 20 is the min neighbour
        smile = cascade_smile.detectMultiScale(ri_grayscale, 1.7, 30)
        
        #draw rectangle on smile ## uncomment to add rectangle to smile
        for (x_smile, y_smile, w_smile, h_smile) in smile: 
            #cv2.rectangle(ri_color,(x_smile, y_smile),(x_smile+w_smile, y_smile+h_smile), (255, 0, 130), 2)
            
            #import image of tongue
            img_tongue= cv2.imread('tongue.png',-1)
            #cv2.imshow('image', img_tongue) 
            
            #rectngle of smile , uncomment it to see rectangle of smile
            #cv2.rectangle(ri_color,(x_smile, y_smile),(x_smile+w_smile, y_smile+h_smile), (255, 0,225), 2)    

            #depth of tongue, width
            dept_tong, width_tong= img_tongue.shape[:2]
            
            #make width to that of 1/3rd of smile
            width_for_tongue= w_smile/3
            scale=   width_for_tongue/width_tong
            
            #adjust dept to same but maintining te aspect ratio
            depth_for_tongue= scale* dept_tong
            width_for_tongue = int(width_for_tongue)
            depth_for_tongue = int(depth_for_tongue)
            
            ##roi tongue
            img_tongue= cv2.resize(img_tongue, (width_for_tongue, depth_for_tongue))

            #finding centre of smile
            centre_smile_x= int(x_smile+ w_smile/2)
            centre_smile_y= int(y_smile+ h_smile/2)
            
            #finding the corrdinates for tongue
            x_tongue=int( centre_smile_x- width_for_tongue/2)
            y_tongue= int(centre_smile_y)
                
            #region of intrest for tongue
            roi_tongue= ri_color[y_tongue: y_tongue+depth_for_tongue, x_tongue: x_tongue+width_for_tongue]
            
            # Now create a mask of logo and create its inverse mask also
            img2gray = cv2.cvtColor(img_tongue,cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            
            
            # Now black-out the area of logo in ROI
            img1_bg = cv2.bitwise_and(roi_tongue,roi_tongue,mask = mask_inv)
            cv2.imshow('Video', img1_bg) 
            
            # Take only region of logo from logo image.
            img2_fg = cv2.bitwise_and(img_tongue,img_tongue,mask = mask)

            # Put logo in ROI and modify the main image
            dst = cv2.add(img1_bg,img2_fg)
            ri_color[y_tongue: y_tongue+depth_for_tongue, x_tongue: x_tongue+width_for_tongue] = dst


            # ears
            ear_width= w_face
            img_ear= cv2.imread('ears.png',-1)
            h,w,c= img_ear.shape
            ratio= ear_width/w
            w= int(w*ratio)
            d= int(h*ratio)
            img_ear= cv2.resize(img_ear, (w,d))
            #cv2.imshow('image3', img_ear)
            #cv2.waitKey(0) 
            #cv2.destroyAllWindows()
            roi_ear= img[y_face: y_face+d,x_face:x_face+w]
            
            dst = cv2.addWeighted(roi_ear, 0.9, img_ear, 0.5, 0)
            img[y_face: y_face+d,x_face:x_face+w]= dst
            #cv2.imshow('Video', img)
            #cv2.waitKey(0) 
            #cv2.destroyAllWindows()
       
    #return image        
    return img 





vc = cv2.VideoCapture(0) 

cnt=0
while cnt<500:
    #read status of camera and frame
    _, img = vc.read() 
    
    #convert image ot grayscale
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    #reuslt from detection function
    final = detection(grayscale, img) 
    
    #showing captured image
    cv2.imshow('Video', final) 
    
    #name of our image, wiht current time , so that it has new name each time.
    string = "pic"+str(datetime.datetime.now())+".jpg"
    
    #path
    path= "/media/suniti/Windows S/ml/face/data-stats/folder"
    
    #save image
    cv2.imwrite(os.path.join(path, string),final)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 
    
    cnt+=1

vc.release() 
cv2.destroyAllWindows() 