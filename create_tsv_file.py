import csv
import os
import glob

# images = os.listdir(r'C:\Users\chen\Documents\TAU\Thesis\Ha-NeRF\data\WikiScenes\Wells_Cathedral\dense\images')
root_dir = r'C:\Users\chen\Documents\TAU\Thesis\Towers_Of_Babel\data\WikiScenes1200px\cathedrals\50'

with open(r'C:\Users\chen\Documents\TAU\Thesis\Ha-NeRF\data\WikiScenes\Wells_Cathedral\Wells_Cathedral_2.tsv', 'wt', newline='') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(['filename', 'id', 'split', 'dataset'])
    id = 0
    for filename in glob.iglob(root_dir + '**/**', recursive=True):
        if filename.endswith(".jpg"):

            if id % 10 == 0:
                split = 'test'
            else:
                split = 'train'
            try:
                tsv_writer.writerow([filename[84:].replace('\\', '/'), str(id), split, 'Wells_Cathedral'])
                id += 1

            except:
                print(filename)
