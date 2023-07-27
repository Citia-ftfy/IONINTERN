import cv2
import numpy as np

def start(filename):
    # read image
    img = cv2.imread("output.png")
    b,g,r = cv2.split(img)
    b = cv2.bitwise_not(b)
    g = cv2.bitwise_not(g)
    r = cv2.bitwise_not(r)
    # convert img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if "blue" in filename:
        gray = b
    if "green" in filename:
        gray = g
    if "red" in filename:
        gray = r
    # do adaptive threshold on gray image
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 3)
    ret, thresh = cv2.threshold(gray,150,255,0)

    # apply morphology open then close
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    blob = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    blob = cv2.morphologyEx(blob, cv2.MORPH_CLOSE, kernel)

    # invert blob
    blob = (255 - blob)

    # Get contours
    cnts = cv2.findContours(blob, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    big_contour = max(cnts, key=cv2.contourArea)

    # test blob size
    blob_area_thresh = 1000
    blob_area = cv2.contourArea(big_contour)
    if blob_area < blob_area_thresh:
        print("Blob Is Too Small")

    return blob

blob1 = start("blue_output.png")
blob2 = start("green_output.png")
blob3 = start("red_output.png")

# draw contour
#result = img.copy()
result = np.zeros((512,512,3), np.uint8)
#cv2.drawContours(result, [big_contour], -1, (0,0,255), 1)
abb = cv2.imread("abb.png")
#abb = cv2.imread("noise.png")
for i in range(512):
    for k in range(512):
        if(blob1[i,k]==255):
            if(abb[i,k][0]>=148):
                result[i,k] = abb[i,k]
for i in range(512):
    for k in range(512):
        if(blob2[i,k]==255):
            if(abb[i,k][1]>=148):
                result[i,k] = abb[i,k]
for i in range(512):
    for k in range(512):
        if(blob3[i,k]==255):
            if(abb[i,k][2]>=148):
                result[i,k] = abb[i,k]


# write results to disk
#cv2.imwrite("doco3_threshold.jpg", thresh)
cv2.imwrite("blob.png", blob1)
#cv2.imwrite("doco3_contour.jpg", result)
#print(big_contour)

# display it
#cv2.imshow("IMAGE", img)
#cv2.imshow("THRESHOLD", thresh)
#cv2.imshow("BLOB", blob)
cv2.imwrite("result.png",result)
cv2.imshow("RESULT", result)
cv2.waitKey(0)