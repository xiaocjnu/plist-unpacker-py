#!python
import os,sys
import plistlib
from PIL import Image

def gen_png_from_plist(plist_filename, png_filename):
    file_path = plist_filename.replace('.plist', '')
    big_image = Image.open(png_filename)
    with open(plist_filename, "rb") as f:
        root = plistlib.load(f)
    frames = root['frames']
    to_list = lambda x: x.replace('{','').replace('}','').split(',')
    to_int = lambda x:int(x)
    for frame in frames:
        framename = frame.replace('.png', '')
        # size = frames[frame]["sourceColorRect"]
        # size = to_list(size)
        # size = map(to_int, size)

        spriteSize = frames[frame]["sourceSize"]
        spriteSize = to_list(spriteSize)
        spriteSize = list(map(to_int, spriteSize))

        textureRect = frames[frame]["frame"]
        textureRect = to_list(textureRect)
        textureRect = list(map(to_int, textureRect))

        result_box = textureRect
        result_image = Image.new('RGBA', spriteSize, 0)
        if frames[frame]["rotated"]:
            result_box[0] = int(textureRect[0])
            result_box[1] = int(textureRect[1])
            result_box[2] = int(textureRect[0] + textureRect[3])
            result_box[3] = int(textureRect[1] + textureRect[2])
        else:
            result_box[0] = int(textureRect[0])
            result_box[1] = int(textureRect[1])
            result_box[2] = int(textureRect[0] + textureRect[2])
            result_box[3] = int(textureRect[1] + textureRect[3])

        #print(result_box, frames[frame].rotated, frame)
        
        rect_on_big = big_image.crop(result_box)
        if frames[frame]["rotated"]:
            rect_on_big = rect_on_big.transpose(Image.ROTATE_90)
        result_image.paste(rect_on_big)
        
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        outfile = (file_path+'/' + framename+'.png')
        print(outfile, "generated")
        result_image.save(outfile)

if __name__ == '__main__':
    filename = sys.argv[1]
    plist_filename = filename + '.plist'
    png_filename = filename + '.png'
    if (os.path.exists(plist_filename) and os.path.exists(png_filename)):
        gen_png_from_plist( plist_filename, png_filename )
    else:
        print("make sure you have boith plist and png files in the same directory")