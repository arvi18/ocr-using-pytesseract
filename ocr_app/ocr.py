import PIL
from PIL import ImageDraw

def pdfToImg(path, pdfname, easyOCR, addBorder, removeBorder, deskew):
    print("ocr.py says: ", easyOCR, addBorder, removeBorder, deskew)
    from pdf2image import convert_from_path

    pages = convert_from_path(path, 500, userpw='XXX')

    image_counter = 1

    extractedText = ""
    for page in pages:
        filepath = "media/"+pdfname+"_" + str(image_counter) + ".jpg"
        page.save(filepath, 'JPEG')

        if easyOCR:
            extractedText = extractedText+usingEasyOCR(filepath)
        else:
            extractedText = extractedText+usingPytesseract(filepath, addBorder, removeBorder, deskew)
        print(extractedText[:40])

        image_counter = image_counter + 1

    return extractedText


def usingEasyOCR(filepath):
    print('using easyocr')
    img = PIL.Image.open(filepath)
    import easyocr
    reader = easyocr.Reader(['en'])
    bounds = reader.readtext(filepath, contrast_ths=0.05, adjust_contrast=0.7,
                             add_margin=0.45, width_ths=0.7, decoder='beamsearch')
    print(bounds)
    # print(draw_boxes(img, bounds))
    text = ""
    for bound in bounds:
        boundText = bound[1]
        text = text+' '+boundText
    return text


def draw_boxes(image, bounds, color='red', width=7):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p1, *p1, *p2, *p3], fill=color, width=width)
    return image


def usingPytesseract(filepath, addBorder, removeBorder, deskew):
    print('using pytes')
    import cv2
    import pytesseract
    from PIL import Image
    from matplotlib import pyplot as plt

    def makeBorder(image):
        color = [0, 0, 0]
        top, bottom, left, right = [50]*4
        image_with_border = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return image_with_border

    def remove_borders(image):
        contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
        cnt = cntsSorted[-1]
        x, y, w, h = cv2.boundingRect(cnt)
        crop = image[y:y+h, x:x+w]
        return (crop)

    def grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def binarize(img):
    # thresh, im_bw = cv2.threshold(gray_img, 210, 230, cv2.THRESH_BINARY)
        return cv2.threshold(img, 210, 230, cv2.THRESH_BINARY)

    def noise_removal(image):
        # thresh, image = cv2.threshold(image, 210, 230, cv2.THRESH_BINARY)
        import numpy as np
        kernel = np.ones((1, 1), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        kernel = np.ones((1, 1), np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        image = cv2.medianBlur(image, 3)
        return (image)
    
    def erode_(image):
        import numpy as np
        image = cv2.bitwise_not(image)
        kernel = np.ones((2,2),np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return (image)

    def dilate_(image):
        import numpy as np
        image = cv2.bitwise_not(image)
        kernel = np.ones((2,2),np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return (image)
    
    def deSkew(cvImage):
        angle = getSkewAngle(cvImage)
        return rotateImage(cvImage, -1.0 * angle)

    def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
        newImage = cvImage.copy()
        gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Apply dilate to merge text into meaningful lines/paragraphs.
        # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
        # But use smaller kernel on Y axis to separate between different blocks of text
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
        dilate = cv2.dilate(thresh, kernel, iterations=2)

        # Find all contours
        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)
        for c in contours:
            rect = cv2.boundingRect(c)
            x,y,w,h = rect
            cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

        # Find largest contour and surround in min area box
        largestContour = contours[0]
        # print (len(contours))
        minAreaRect = cv2.minAreaRect(largestContour)
        # Determine the angle. Convert it to the value that was originally used to obtain skewed image
        angle = minAreaRect[-1]
        if angle < -45:
            angle = 90 + angle
        return -1.0 * angle
    
    def rotateImage(cvImage, angle: float):
        newImage = cvImage.copy()
        (h, w) = newImage.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return newImage

    def display(im_path):
        dpi = 80
        im_data = plt.imread(im_path)

        height, width  = im_data.shape[:2]
        print('im_data.shape:', im_data.shape)
        
        # What size does the figure need to be in inches to fit the image?
        figsize = width / float(dpi), height / float(dpi)

        # Create a figure of the right size with one axes that takes up the full figure
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1])

        # Hide spines, ticks, etc.
        ax.axis('off')

        # Display the image.
        ax.imshow(im_data, cmap='gray')

        plt.show()

    img = cv2.imread(filepath)
    if addBorder:
        img=makeBorder(img)
    if deskew:
        img=deSkew(img)
    gray_img = grayscale(img)
    binarized_img = binarize(gray_img)
    no_noise_img = noise_removal(gray_img)
    if removeBorder:
        no_noise_img=remove_borders(no_noise_img)

    cv2.imwrite(filepath, no_noise_img)
    text=pytesseract.image_to_string(filepath)
    return text