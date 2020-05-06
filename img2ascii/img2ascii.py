from colorama import init, deinit, Style, Fore
from PIL import Image

def pix2str_bw(p, charset, space):
    p *= len(charset)-1
    p //= 255
    return charset[p] + ' ' * space

def pix2str(p, char, space):
    apx = [(12,12,12), (197,15,31), (19,161,14), (193,156,0), (0,55,218), (136,23,152), (58,150,221), (204,204,204),
          (118,118,118), (231,72,86), (22,198,12), (249,241,165), (59,120,255), (180,0,158), (97,214,214), (242,242,242)]
    b = 3*255*255
    i = 0

    for j in range(len(apx)):
        x = pow(apx[j][0] - p[0], 2) + pow(apx[j][1] - p[1], 2) + pow(apx[j][2] - p[2], 2)
        if x < b:
            b = x
            i = j
    
    if i > 7:
        i += 82
    else:
        i += 30

    return '\033[' + str(i) + 'm' + char + ' ' * space

def create_str(img, dim, charset, space, colors):
    img = img.resize(dim)
    if not colors:
        img = img.convert('L')
    m = img.load()
    s = ''

    if colors:
        for y in range(dim[0]):
            for x in range(dim[1]):
                s += pix2str(m[x, y], charset, space)
            s += '\n'
        s += Style.RESET_ALL
    else:
        for y in range(dim[0]):
            for x in range(dim[1]):
                s += pix2str_bw(m[x, y], charset, space)
            s += '\n'
    
    return s

def print_img(img, dim, charset = '.+oO@', space = 1, colors = False):
    s = create_str(img, dim, charset, space, colors)
    if colors:
        init()
        print(s)
        deinit()
    else:
        print(s)