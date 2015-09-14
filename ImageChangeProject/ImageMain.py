import glob
import os
import shutil
from PIL import Image
from utils import send_email

ERROR_SET = set()
global debug
# noinspection PyRedeclaration
debug = True

#  Keys: Image type.  Values: Image size.
SIZE_MAP = {
    'ne': (640, 480), 'a': (50, 50), 'b': (100, 100),
    'c': (350, 350), 'd': (575, 575), 'e': (150, 150),
    'f': (1001, 1001), 'g': (3000, 3000), 'h': (180, 180), 'j': (500, 500)
}

SIZE_LIMIT = {(500, 500)}


# create new file name
# if image_size_type is 'g'
# eg. foo.jpg ---> foog.jpg
def remove_extension(filename):
    return ''.join(filename.split('.')[:-1])


# noinspection PyTypeChecker
def create_image(size_type, filename, dest='./dest'):
    """
    Takes a filename and size type and saves a resized Image object
    to the dest directory
    :type filename: object
    """
    # will retrieve a tuple from the size map i.e. (w, h)
    width_height = SIZE_MAP[size_type]

    new_filename = remove_extension(filename) + size_type + '.jpg'
    # Attempt to open file
    try:
        image = Image.open(filename)
        width, height = image.size
    except IOError:
        pass

    # Create square image if not square already
    if not os.path.isfile(dest + '/' + new_filename):
        try:
            if not height == width:
                if height > width:
                    width = height
                else:
                    height = width
                new_background_image = Image.new("RGB", (width, height), "white")
                new_background_image.paste(image.resize((1001, 1001), Image.ANTIALIAS))
                base_image = new_background_image
            elif size_type == 'ne':
                new_background_image = Image.new("RGB", (width, height), "white")
                new_background_image.paste(image.resize((1001, 1001), Image.ANTIALIAS))
                base_image = new_background_image
            else:
                base_image = Image.open(filename)
        except (IOError, AttributeError, UnboundLocalError):
            pass
        try:
            final_image = base_image.resize(width_height, Image.ANTIALIAS)
        except (AttributeError, UnboundLocalError):
            pass

        # Try to save the newly created image
        try:
            final_image.save(new_filename)
        except (UnboundLocalError, IOError, AttributeError):
            ERROR_SET.add(filename)
            for fname in glob.glob("dest/" + remove_extension(filename) + "*"):
                os.remove(fname)

        # Try to move new file to destination folder
        try:
            shutil.move(new_filename, dest)
        except(shutil.Error, IOError):
            ERROR_SET.add(filename)
            for fname in glob.glob("dest/" + remove_extension(filename) + "*"):
                os.remove(fname)
            for fname in glob.glob(remove_extension(filename) + "*"):
                os.remove(fname)


def main():
    filenames = glob.glob("*.jpg")
    filenames += glob.glob("*.jpeg")
    for filename in filenames:
        image = Image.open(filename)
        for size_type in SIZE_MAP.keys():
            for limits in SIZE_LIMIT:
                width, height = image.size
                limit_width = limits[0]
                limit_height = limits[1]
                if width > limit_width and height > limit_width and height > limit_height\
                        and height > limit_width:
                    image.close()
                    create_image(size_type, filename)
                else:
                    image.close()
                    ERROR_SET.add(filename)
                    try:
                        os.remove(filename)
                    except (IOError, WindowsError):
                        pass

    # remove the files!
    try:
        map(os.remove, filenames)
    except WindowsError:
        pass

    success = [filename for filename in filenames if filename not in ERROR_SET]

    outfile = 'Errors: \n' + str(ERROR_SET) + '\n\nProcessed: \n' + str(success)
    if debug:
        print outfile
    else:
        send_email(outfile)


if __name__ == '__main__':
    main()
