from PIL import Image, ImageDraw, ImageFont

image = Image.new('RGB', (200, 100), color = (73, 109, 137))
d = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", 15)
text = "Hello World"
print(ImageDraw.__file__)
print(dir(ImageDraw))
width, height = d.textsize(text, font=font)
d.text((10,10), text, fill=(255,255,0), font=font)
image.show()