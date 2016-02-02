from images2gif import writeGif
from PIL import Image
import os
import glob

file_names = glob.glob("./static/travelMaps/*Age.jpg")
#['animation_a.png', 'animation_b.png', ...] "
print file_names

images = [Image.open(fn) for fn in file_names]

for i in images:
    print type(i)

#size = (150,150)
#for im in images:
#    im.thumbnail(size, Image.ANTIALIAS)

print writeGif.__doc__
# writeGif(filename, images, duration=0.1, loops=0, dither=1)
#    Write an animated gif from the specified images.
#    images should be a list of numpy arrays of PIL images.
#    ...
#    ...

filename = "my_gif_ageDist.GIF"
writeGif(filename, images, duration=1.)
