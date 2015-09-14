import glob
import os

source_dir = 'E:\\Rackspace Backup\\images.oldglory.com\\product_old\\'
des_dir = 'E:\\Rackspace Backup\\images.oldglory.com\\product\\'


for root, dirs, files in os.walk(source_dir, topdown=False):
    for name in files:
        to_file = des_dir + name
        from_file = source_dir + name
        if os.path.isfile(to_file):
            os.remove(from_file)
            print(from_file + ' *** exists - deleting.')
        else:
            os.rename(from_file, to_file)
            print (from_file + " ====> " + to_file)
