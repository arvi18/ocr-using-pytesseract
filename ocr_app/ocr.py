import PIL
from PIL import ImageDraw
from pdf2image import convert_from_path
import easyocr

print("importinging!")
reader = easyocr.Reader(['en'])
print("imported!")


def pdfToImg(path, pdfname):
    pages = convert_from_path(path, 500, userpw='XXX')

    image_counter = 1

    extractedText = ""
    for page in pages:
        filepath = "media/"+pdfname+"_" + str(image_counter) + ".jpg"
        page.save(filepath, 'JPEG')

        img = PIL.Image.open(filepath)
        bounds=reader.readtext(filepath)

        print("@Earlier: ", bounds)
        print(draw_boxes(img, bounds))

        bounds = reader.readtext(filepath, contrast_ths=0.05, adjust_contrast=0.7,
                                 add_margin=0.45, width_ths=0.7, decoder='beamsearch')
        print(bounds)
        for bound in bounds:
            text = bound[1]
            extractedText = extractedText+' '+text

        image_counter = image_counter + 1
        print(extractedText)

    return extractedText


def draw_boxes(image, bounds, color='red', width=7):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p1, *p1, *p2, *p3], fill=color, width=width)
    return image
