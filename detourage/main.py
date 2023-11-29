
from PIL import Image, ImageFilter, ImageChops, ImageOps
import numpy as np
import os
import re
import cv2

def initial_background_removal(font:str, gen_version:str, switcher_index:int):
    base_path = "ai-source/"
    mask_name = font
    version = gen_version

    # 0 for normal, 1 to 5 for switcheroo
    swhitcher_index = switcher_index
    brightness_threshold = 23
    blur_strength = 5


    def importer(folder_path, full_import:bool):
        image_list = []
        paths = os.listdir(folder_path)
        # print(paths)          # PRINT
        def mootching(path):
            if path.endswith(".DS_Store"): 
                paths.remove(path)
                return float("inf")
            mootch = re.search(r'_(\d+)', path)
            # print(path)         # PRINT
            # print(mootch)         # PRINT
            return int(mootch.group(1))
        
        sorted_paths = sorted(paths, key=mootching)
        for filename in sorted_paths:
            # print(filename)         # PRINT
            if filename.endswith(".DS_Store"): 
                continue
            cv2_img = cv2.imread(os.path.join(folder_path, filename))
            img = Image.open(os.path.join(folder_path, filename))
            hsv_img = img.convert("HSV")
            match = re.search(r'_(\d+)', filename)
            butchered_filename = filename[:-4]
            if full_import == True :
                image_list.append([cv2_img, img, hsv_img, butchered_filename, match.group(), int(match.group(1))-1])
            else : 
                image_list.append(img.convert("L"))
                # img.show()           # SHOW
            # Image.fromarray(cv2_img).show()               # SHOW

        return image_list


    mask_folder_path = base_path + mask_name
    letters_folder_path = base_path + mask_name + "_letters_" + version
    end_path = base_path + version + "export" + mask_name + 'swap' + str(swhitcher_index)

    if not os.path.exists(end_path):
        os.makedirs(end_path)
        print("Directory ", end_path, " Created ")
    else:
        print("Directory ", end_path, " already exists")


    #  PATHS
    background_path = "Concrete1024.png"
    letters_list = importer(letters_folder_path, full_import=True)
    mask_list = importer(mask_folder_path, full_import=False)
    # for imgs in letters_list:         # PRINT
        # print (imgs[-1])        # PRINT
    # mask_list[0].show()           # SHOW

    # # reading the images
    background = cv2.imread(background_path)
    pil_background = Image.open(background_path)
    pil_background = pil_background.convert("RGB")


    for count, mask in enumerate(mask_list):
        expanded_mask = mask
        blurred_mask = expanded_mask.filter(ImageFilter.GaussianBlur(blur_strength))
        mask_list[count] = blurred_mask

    for count, imgs in enumerate(letters_list):
        # print(count)
        letter_mask = mask_list[imgs[-1]]
        # letter_mask.show()           # SHOW
        letter_mask = ImageOps.invert(letter_mask)
        # letter_mask.show()           # SHOW 

        finool_image_pil = Image.composite(imgs[1], Image.new('RGBA', imgs[1].size, (0, 0, 0, 0)), letter_mask)
        r, g, b, a = finool_image_pil.split()
        switcheroo = [(r, g, b, a), (b, g, r, a), (g, b, r, a), (b, r, g, a), (r, b, g, a), (g, r, b, a)]
        most_final_img = Image.merge("RGBA", switcheroo[swhitcher_index])
        # most_final_img.show()
        most_final_img.save(end_path + "/" + version + imgs[-3] + "MASK" + str(imgs[-1]) + "GEN" +imgs[-2] + ".png")

    genned_files_path = os.listdir(end_path)
    genned_files = []
    end_sequences = []
    for genned_file_path in genned_files_path:
        if genned_file_path.endswith(".DS_Store"): 
            os.remove(end_path + "/" + '.DS_Store')
            continue
        genned_image = Image.open(end_path + "/" + genned_file_path)
        # Extract the number between underscores in the image path
        end_sequence = re.search(r'_(\d+)_0', genned_file_path)[1]
        end_sequences.append(end_sequence)
        genned_files.append(genned_image)
    print(end_sequences)
    matching_files = []
    for count, genned_file in enumerate(genned_files):
        for count2, end_sequence in enumerate(end_sequences):
            print(end_sequences[count], end_sequence)
            if (end_sequences[count] == end_sequence) and (count != count2):
                matching_files.append([[genned_file, genned_files_path[count]], [genned_files[count2], genned_files_path[count2]]])

    for count, matching_file_set in enumerate(matching_files):
        for count2, matching_file in enumerate(matching_file_set):
            matching_file[0].show()
        choice = int(input("Which one do you want to keep ?) Starting from 0"))
        if choice == 0:
            print("You chose to keep " + matching_file_set[0][1] + " and delete " + matching_file_set[1][1])
            os.remove(end_path + "/" + matching_file_set[1][1])
        elif choice == 1:
            print("You chose to keep " + matching_file_set[1][1] + " and delete " + matching_file_set[0][1])
            os.remove(end_path + "/" + matching_file_set[0][1])
        else:
            print("You didn't choose a valid option, both files will be kept")


        

