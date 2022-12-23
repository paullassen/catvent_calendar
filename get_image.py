import PIL
from PIL import Image

HEIGHT = 600
WIDTH = 448

# Open the image
im = Image.open("image.jpg")

# Get the image size
width, height = im.size

# Resize the image
im = im.resize((WIDTH, HEIGHT), PIL.Image.ANTIALIAS)

# Save the image as bmp
im.save("image.bmp")
