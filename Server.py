import socket
import cv2 
# from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import os
import requests

def read_plate(filename):
    img = cv2.imread(filename)
    ret,gray = cv2.threshold(img,120,255,cv2.THRESH_TOZERO)
    # plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

     
    canbang =  cv2.equalizeHist(gray)
    bfiler = cv2.bilateralFilter(canbang,11,70,70)
    ret,bfiler = cv2.threshold(bfiler,200,255,cv2.THRESH_TOZERO)
    edged = cv2.Canny(bfiler,30,200)
    # plt.imshow(cv2.cvtColor(edged,cv2.COLOR_BGR2RGB))

    keypoints = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    h=len(gray)
    w=len(gray[0])

    location = None 
    for contour in contours:
      approx = cv2.approxPolyDP(contour,20,True)
      if len(approx) >= 4 and len(approx) <=25: 
        x=np.array([])
        y=np.array([])
        for i in range(len(approx)):
          x = np.append(x,[approx[i][0][0]])
          y = np.append(y,[approx[i][0][1]])
        xmax = x.max()
        xmin = x.min()
        ymax = y.max()
        ymin = y.min()
        # if xmin>w*0.2 and xmax < 0.8*w and ymin>h*0.1 and ymax < 0.9*h:
        if xmax-xmin>50 and xmax-xmin<100:
          if ymax-ymin>30 and ymax-ymin<=100:
            if ((ymax-ymin)/(xmax-xmin))>0.6:
              location = approx
              break

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = img[x1:x2+1, y1:y2+1]


    # plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

    cropped_image_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    cropped_image_blur = cv2.GaussianBlur(cropped_image_gray, (3,3), 0)
    ret, thresh = cv2.threshold(cropped_image_gray, 0, 255,cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV )
    kernel = np.ones((2,2),np.uint8)
    erosion = cv2.erode(thresh,kernel,iterations = 1)

    # plt.imshow(cv2.cvtColor(erosion, cv2.COLOR_BGR2RGB))

    print("xong roi")

    result = reader.readtext(erosion)

    ten = ''
    for i in range(len(result)):
        ten += result[i][-2]
        print(ten)

        url = "http://localhost:3000/data"
        files = {'file': open('./uploads/102180237.74l1-28156.jpg', 'rb')}
        requests.post(url, files=files)

    return ten

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('192.168.1.3', 65432))
serv.listen(5)

reader = easyocr.Reader(['en'])

# currentDT = datetime.datetime.now()
while True:
    conn, addr = serv.accept()
    from_client = ''
    while True:
        with open('received_file.jpg','wb') as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    f.write(data)
        f.close()
        bsx = read_plate('received_file.jpg')
        os.rename('received_file.jpg', bsx+'.jpg')
        break
    conn.close()
    print ('client disconnected')
