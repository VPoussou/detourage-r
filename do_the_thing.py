import main
import split_n_crop

#HERE GO THE THINGS
font = 'f9'
gen_version = 'v1'
#I SAID HERE

#This does the rest
for switcher_index in range(6):    
    main.initial_background_removal(font, gen_version, switcher_index)
    split_n_crop.split(font, gen_version, switcher_index)