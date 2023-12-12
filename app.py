import cv2
import numpy as np
import glob 
import pytesseract
from yoloDet import YoloTRT
from database import Database

db = Database()

def read_text(img):
   text=""
   if img.shape[0]/img.shape[1] > 0.2 and img.shape[0]/img.shape[1] < 0.7: 
      custom_config = r'--oem 3 --psm 6'
      
      text =text+pytesseract.image_to_string(img,config=custom_config)
   
   elif img.shape[0]/img.shape[1] > 0.7:
    
      custom_config = r'--oem 3 --psm 6'
      img2=img[:img.shape[0]//2,:]
      text1 =" "+pytesseract.image_to_string(img2,config=custom_config)
      img3=img[img.shape[0]//2:,:]
      text2 =" "+pytesseract.image_to_string(img3,config=custom_config)
      
      
      if text1[-1] == "\n":
            text1 = text1.replace("\n", "")
            
     
      if text2[-1] == "\n":
            text2 = text2.replace("\n", '')
           
      
      text=text1+text2
   text = text.rstrip("~,.!?'\"())").lstrip("~,.!?'\"()")
   text = "".join([char for id, char in enumerate(text) if char.isdigit() or char.isalpha()])
      
   return text
        
        
    
def crop_license_plate(image):
#  cv2.imshow("Original Image",image)
#  cv2.waitKey(0)
   gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
   unnoise=cv2.bilateralFilter(gray,11,17,17)
   
   edged=cv2.Canny(unnoise,30,200)
   cnts,new=cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
   cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:10]
   location=[]
   for c in cnts:
      approx=cv2.approxPolyDP(c,10,True)
      if len(approx) == 4:
         location.append(approx)
         break
   #print(location[0].shape)
   if len(location)==0:
      #cv2.imshow("cropped_image",image)
      #cv2.waitKey(0)
      return image
   else:
      mask=np.zeros(gray.shape,np.uint8)
      new_image=cv2.drawContours(mask,[location[0]],0,255,-1)
      new_image=cv2.bitwise_and(image,image,mask=mask)
      (x,y)=np.where(mask==255)
      (x1,y1)=(np.min(x),np.min(y))
      (x2,y2)=(np.max(x),np.max(y))
      cropped_image=gray[x1:x2,y1:y2]
      #cv2.imshow("cropped_image",cropped_image)
      #cv2.waitKey(0)
      return cropped_image
        
def license_plate_recognition_pipline(input,model):
   text=""
   detections, t = model.Inference(input)
   if len(detections)!=1:
      pass
   else:
      for obj in detections:
          bbox = obj["box"]
          x1,y1,x2,y2=bbox
          image=input[int(y1):int(y2),int(x1):int(x2)]
      image=crop_license_plate(image)
      cv2.imshow("cropped image",image)
      cv2.waitKey(0)
      text=read_text(image)
      if len(text)<5:
         text=read_text(input)
   return text



if __name__ == "__main__":
   # use path for library and engine file
   model = YoloTRT(library="yolov5/build/libmyplugins.so", engine="yolov5/build/last.engine", conf=0.7, yolo_ver="v5")
   image_path_list=glob.glob(r'/home/jetsionnano/JetsonYolov5/image/*.*')
   
   for image_path in image_path_list:
      image = cv2.imread(image_path)
      text = license_plate_recognition_pipline(image, model)
      print(text)
      print(image_path)
      
      
      
      db.insert_data(carID = db.count_db()+2, Lisence_plate=text,Status = 1, number_Car=5)
      #cv2.imshow("image", image)
      #cv2.waitKey(0)

   cv2.destroyAllWindows()

   







