import zipfile
import kraken

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')



#take the images from the zip and return a dictionary
#with the pages name and the images
def getimage_dict(zip_path):

    images_zip = zipfile.ZipFile(zip_path, "r")
    imageNames_zip = images_zip.namelist()

    #print(imageNames_zip)

    img_dict = {}
    for image_name in imageNames_zip:
        img_bytes = images_zip.open(image_name)          # 1
        img = Image.open(img_bytes)                      # 2
        #display(img)
        img_dict[image_name] = [img]

    
    return img_dict



#add the text of each page to the dictionary containing
#the image and the page name as dictionary key
def getTextFromImage(pagesDict):
    
    for image_name in list(pagesDict.keys()):
        img = pagesDict[image_name][0]
        #display(img)
        text = pytesseract.image_to_string(img)
        pagesDict[image_name].append(text)

    return pagesDict




#get the pages that contain the keyword
#in a dictionary containing page name and image
def getThePages_text(baseDict, keyword):
    
    pageswithword = {}
    
    for pagename in list(baseDict.keys()):
        
        if keyword in baseDict[pagename][1]:
            pageswithword[pagename] = baseDict[pagename]
    
    return pageswithword
    
    

#with the image object and the page name as an input
#print the faces if there are or print a message
def faceRecognition(newspaperimage, page_name):
    
    rgb_im = newspaperimage.convert('RGB')
    rgb_im.save('colors.jpg')
    img = cv.imread('colors.jpg')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray,1.35)
    
    #pil_img=Image.fromarray(gray,mode="L")
    #display(pil_img)
    
    try:
        face_rectangles = faces.tolist()
        faces_in_page = True
    except:
        print("""Results found in {} \nBut there were no faces in that file!""".format(page_name))
        faces_in_page = False
    
    if faces_in_page:
        
        print("""Results found in {}""".format(page_name))
                
        
        if len(face_rectangles) <= 5:
            base_sheet=Image.new(newspaperimage.mode, (100*len(face_rectangles),100))
            
        
        if (len(face_rectangles) > 5):
            base_sheet = Image.new(newspaperimage.mode, (100*5,100*((len(face_rectangles) // 5)+1)))
            
            
        x = 0
        y = 0          
        for face in face_rectangles:   

            cropped_face = newspaperimage.crop((face[0],face[1],face[0]+face[2],face[1]+face[3]))
            cropped_face = cropped_face.resize((100,100))
            
            base_sheet.paste(cropped_face, (x, y))
            x = x + 100
            if x == 500:
                x = 0
                y = y + 100
            
        display(base_sheet)
            

    return "Done" 
    
    
    

#get a dictionary with the name of the page and the image as a value
name_image_dict = getimage_dict("readonly/images.zip")

#get a dictionary with the names of the pages, and a list as value
#the list is including the image object and the text included in it
name_image_text_dict = getTextFromImage(name_image_dict)

#the keyword to search in the newspaper
keyword = "Mark"

#enter the keyword to the dictionary and get a dictionary with the 
#only with the pages that contain the keyword
pageswithword = getThePages_text(name_image_text_dict, keyword)


#take dictionary with the pages containing the keyword and
#print the faces and the message
for pages in list(pageswithword.keys()):
    #print(pages)
    faceRecognition(name_image_dict[pages][0], pages)

#print(faceRecognition(name_image_dict["a-0.png"][0], "izenaa"))

#final_text = faceRecognition(name_image_dict["a-0.png"][0], pages)
#image = name_image_dict["a-0.png"][0]
#image.convert('RGB').save("image_name.jpg","JPEG")

#print(image.mode)

#display(name_image_dict["a-0.png"][0])