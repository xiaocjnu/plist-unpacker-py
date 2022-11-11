#!python
import os
import sys
import json
from PIL import Image


def gen_png_from_spriteframe(spriteframe_filepath, texture_filepath, source_texture_filepath):
    # read meta object
    with open(spriteframe_filepath, "r") as f:
        meta_object = json.load(f)
        subMeta = list(meta_object["subMetas"].values())[0]

    spriteSize = [subMeta["width"], subMeta["height"]]
    textureRect = [subMeta["trimX"], subMeta["trimY"],
                   subMeta["width"], subMeta["height"]]
    rotated = subMeta["rotated"]

    # crop
    result_box = textureRect
    if texture_filepath.endswith(".jpg"):
        result_image = Image.new('RGB', spriteSize, 0)
    else:
        result_image = Image.new('RGBA', spriteSize, 0)
    if rotated:
        result_box[0] = int(textureRect[0])
        result_box[1] = int(textureRect[1])
        result_box[2] = int(textureRect[0] + textureRect[3])
        result_box[3] = int(textureRect[1] + textureRect[2])
    else:
        result_box[0] = int(textureRect[0])
        result_box[1] = int(textureRect[1])
        result_box[2] = int(textureRect[0] + textureRect[2])
        result_box[3] = int(textureRect[1] + textureRect[3])
    source_image = Image.open(source_texture_filepath)
    rect_on_source_image = source_image.crop(result_box)
    if rotated:
        rect_on_source_image = rect_on_source_image.transpose(Image.Transpose.ROTATE_90)
    result_image.paste(rect_on_source_image)

    # write texture
    dir_path = os.path.dirname(texture_filepath)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    outfile = texture_filepath
    result_image.save(outfile)

    # write meta
    meta_file_path = texture_filepath + ".meta"
    meta_object["width"] = subMeta["width"]
    meta_object["height"] = subMeta["height"]
    subMeta["rotated"] = False
    subMeta["offsetX"] = 0
    subMeta["offsetY"] = 0
    subMeta["trimX"] = 0
    subMeta["trimY"] = 0
    subMeta["rawWidth"] = subMeta["width"]
    subMeta["rawHeight"] = subMeta["height"]
    with open(meta_file_path, "w") as f:
        json.dump(meta_object, f, indent=2)

    os.remove(spriteframe_filepath)
    spriteframe_meta_filepath = spriteframe_filepath + ".meta"
    if os.path.exists(spriteframe_meta_filepath):
        os.remove(spriteframe_meta_filepath)

    print(outfile, "generated")


if __name__ == '__main__':
    spriteframe_filepath = sys.argv[1]
    texture_filepath = sys.argv[2]
    source_texture_filepath = sys.argv[3]
    if (os.path.exists(spriteframe_filepath) and os.path.exists(source_texture_filepath)):
        gen_png_from_spriteframe(spriteframe_filepath,
                                 texture_filepath, source_texture_filepath)
    else:
        print("make sure you have boith meta file & source texture file")
