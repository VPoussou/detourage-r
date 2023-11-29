from PIL import Image, ImageFilter, ImageChops
import numpy as np
import os
import re

def split(font:str, gen_version:str, switcher_index:int):
    #Openin stuff
    font_number = font
    version = gen_version
    base_path = "ai-source/"
    switcheroo_version = str(switcher_index)

    masks_path = base_path + font_number
    letters_path = base_path + version + "export" + font_number + 'swap'  + switcheroo_version
    mask_path_list = os.listdir(masks_path)
    letter_path_list = os.listdir(letters_path)
    def sorter_funk(path):
        if path.endswith(".DS_Store"): 
            return float("inf")
        mootch = re.search(r'(\d+)_(\d+)', path)
        return int(mootch.group(2))
    mask_path_list.sort(key=sorter_funk)
    letter_path_list.sort(key=sorter_funk)

    mask_list = []
    letter_list = []

    # Loading images
    for mask_path in mask_path_list:
        mask_list.append(Image.open(masks_path + "/" + mask_path))
    for letter_path in letter_path_list:
        if letter_path.endswith(".DS_Store"): 
            continue
        letter_list.append(Image.open(letters_path + "/" + letter_path))

    trans_list = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "@",
        "#",
        "&",
        "'",
        "(",
        "!",
        "_",
        "^",
        "*",
        "$",
        "%",
        "/",
        "ç",
        "€",
        "void",
        "void1"
    ]
    le_trans = {}
    for count, i in enumerate(trans_list):
        le_trans[i] = count

    exports = {
        "A": [],
        "B": [],
        "C": [],
        "D": [],
        "E": [],
        "F": [],
        "G": [],
        "H": [],
        "I": [],
        "J": [],
        "K": [],
        "L": [],
        "M": [],
        "N": [],
        "O": [],
        "P": [],
        "Q": [],
        "R": [],
        "S": [],
        "T": [],
        "U": [],
        "V": [],
        "W": [],
        "X": [],
        "Y": [],
        "Z": [],
        "0": [],
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": [],
        "7": [],
        "8": [],
        "9": [],
        "@": [],
        "#": [],
        "&": [],
        "'": [],
        "(": [],
        "!": [],
        "_": [],
        "^": [],
        "*": [],
        "$": [],
        "%": [],
        "/": [],
        "ç": [],
        "€": [],
        "void": [],
        "void1": [],
    }
    letter_number = 0
    for mask, image in zip(mask_list, letter_list):
    # Removin white lines
        transparent = Image.new('RGBA', image.size, (255, 255, 255, 0))
        white_image_pil = Image.new("RGBA", (1024, 1024), (255, 255, 255, 0))
        cropped_mask = mask.crop((30, 30, 994, 994))
        white_image_pil.paste(cropped_mask, (30, 30))
        letter_mask = Image.alpha_composite(transparent, white_image_pil)
        # letter_mask.show()
        # print(letter_mask.size)


        #Dealin with mask
        expanded_mask = white_image_pil.filter(ImageFilter.MinFilter(11))
        inverted_mask = ImageChops.invert(expanded_mask)
        nb_mask = inverted_mask.convert('L')

        # Sizin quadrants
        width, height = image.size
        # print(width, height)          #PRINT
        quadrant_width = width // 2
        quadrant_height = height // 2

        top_left = image.crop((0, 0, quadrant_width, quadrant_height))
        top_right = image.crop((quadrant_width, 0, width, quadrant_height))
        bottom_left = image.crop((0, quadrant_height, quadrant_width, height))
        bottom_right = image.crop((quadrant_width, quadrant_height, width, height))

        blur_strength = 9

        top_left_blurred_alpha = top_left.split()[3].filter(ImageFilter.GaussianBlur(blur_strength))
        top_right_blurred_alpha = top_right.split()[3].filter(ImageFilter.GaussianBlur(blur_strength))
        bottom_left_blurred_alpha = bottom_left.split()[3].filter(ImageFilter.GaussianBlur(blur_strength))
        bottom_right_blurred_alpha = bottom_right.split()[3].filter(ImageFilter.GaussianBlur(blur_strength))

        top_left = Image.merge('RGBA', (top_left.split()[0], top_left.split()[1], top_left.split()[2], top_left_blurred_alpha))
        top_right = Image.merge('RGBA', (top_right.split()[0], top_right.split()[1], top_right.split()[2], top_right_blurred_alpha))
        bottom_left = Image.merge('RGBA', (bottom_left.split()[0], bottom_left.split()[1], bottom_left.split()[2], bottom_left_blurred_alpha))
        bottom_right = Image.merge('RGBA', (bottom_right.split()[0], bottom_right.split()[1], bottom_right.split()[2], bottom_right_blurred_alpha))

        top_left_mask = nb_mask.crop((0, 0, quadrant_width, quadrant_height))
        top_right_mask = nb_mask.crop((quadrant_width, 0, width, quadrant_height))
        bottom_left_mask = nb_mask.crop((0, quadrant_height, quadrant_width, height))
        bottom_right_mask = nb_mask.crop((quadrant_width, quadrant_height, width, height))

        # top_left.show()
        # top_right.show()
        # bottom_left.show()
        # bottom_right.show()

        # top_left_mask.show()
        # top_right_mask.show()
        # bottom_left_mask.show()
        # bottom_right_mask.show()

        temp_top_left_mask = top_left_mask.convert('L')
        temp_top_right_mask = top_right_mask.convert('L')
        temp_bottom_left_mask = bottom_left_mask.convert('L')
        temp_bottom_right_mask = bottom_right_mask.convert('L')

        bbox_top_left_mask = temp_top_left_mask.getbbox()
        bbox_top_right_mask = temp_top_right_mask.getbbox()
        bbox_bottom_left_mask = temp_bottom_left_mask.getbbox()
        bbox_bottom_right_mask = temp_bottom_right_mask.getbbox()


        crop1 = top_left.crop(bbox_top_left_mask)
        crop2 = top_right.crop(bbox_top_right_mask)
        crop3 = bottom_left.crop(bbox_bottom_left_mask)
        crop4 = bottom_right.crop(bbox_bottom_right_mask)
    

        exports[trans_list[letter_number]].append(crop1)
        letter_number += 1
        exports[trans_list[letter_number]].append(crop2)
        letter_number += 1
        exports[trans_list[letter_number]].append(crop3)
        letter_number += 1
        exports[trans_list[letter_number]].append(crop4)
        letter_number += 1


        # crop1.show()
        # print(crop1.size)
        # print(bbox_top_left_mask)
        # crop2.show()
        # print(crop2.size)
        # print(bbox_top_right_mask)
        # crop3.show()
        # print(crop3.size)
        # print(bbox_bottom_left_mask)
        # crop4.show()
        # print(crop4.size)
        # print(bbox_bottom_right_mask)

    exports["A"][0].show()
    if not os.path.exists(base_path + "semi_final" + version + font_number + 'swap' + switcheroo_version):
        os.makedirs(base_path + "semi_final" + version + font_number + 'swap'  + switcheroo_version)
    count = 0
    for key, value in exports.items():
        print(key)
        print(value)
        value[0].save(base_path + "semi_final" + version + font_number + 'swap' + switcheroo_version + "/" + str(count) + ".png")
        count += 1


    # negative_spacing = 60
    # total_width = sum([img.width for img in abcd_list]) - negative_spacing * len(abcd_list)
    # max_height = max([img.height for img in abcd_list])

    # new_im = Image.new('RGBA', (total_width, max_height), (0, 0, 0, 0))

    # current_x = 0
    # for letter in abcd_list:
    #     temp_alpha_img = Image.new('RGBA', (total_width, max_height), (0, 0, 0, 0))
    #     temp_alpha_img.paste(letter, (current_x, 0))
    #     new_im = Image.alpha_composite(new_im, temp_alpha_img)
    #     current_x += letter.width - negative_spacing

    # new_im.show()