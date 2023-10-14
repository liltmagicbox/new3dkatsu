from PIL import Image
import numpy as np

['alpha_composite', 'close', 'convert', 'copy', 'crop', 'custom_mimetype',
'decoderconfig', 'decodermaxblock', 'default_image', 'draft',
'effect_spread', 'entropy', 'filename', 'filter', 'format', 'format_description', 'fp', 'frombytes',
'get_format_mimetype', 'getbands', 'getbbox', 'getchannel', 'getcolors',
'getdata', 'getexif', 'getextrema', 'getim', 'getpalette', 'getpixel', 'getprojection',
'getxmp', 'height', 'histogram', 'im', 'info', 'is_animated',
'load', 'load_end', 'load_prepare', 'load_read', 'mode', 'n_frames',
'palette', 'paste', 'png', 'point', 'private_chunks', 'putalpha', 'putdata',
'putpalette', 'putpixel', 'pyaccess', 'quantize', 'readonly', 'reduce', 'remap_palette',
'resize', 'rotate', 'save', 'seek', 'show', 'size', 'split', 'tell', 'text', 'thumbnail',
'tile', 'tobitmap', 'tobytes', 'toqimage', 'toqpixmap', 'transform', 'transpose', 'verify', 'width']

#print(img.mode) #RGBA gacha!
#print(img.info) #{'srgb': 0, 'gamma': 0.45455, 'dpi': (96.012, 96.012)}
#https://stackoverflow.com/questions/52307290/what-is-the-difference-between-images-in-p-and-l-mode-in-pil
#print(img.mode)P? palettised!
#img = img.convert('RGBA') #well. seems image returns fine rgba structure.. yeah. 10,10,4.
#print(img.getchannel(0)) #<PIL.Image.Image image mode=L size=10x10 at 0x16E5B738C10>        


def img_to_bgra(img_path):
    "-> height, width, BGRA nparr"
    img = Image.open(img_path)
    
    if not img.mode == "RGBA":
        #print('convert to RGBA from',img.mode)
        img = img.convert("RGBA")
    npimg = np.asarray(img) #0.00021540000000000448 / 1e-5 after img.convert, it cached!
    
    #print(npimg[0][0])#[238  27  36] R G B , so img.mode is RGB. /[238  27  36 255] converted.
    npimg = npimg[::-1] #reversed.  [238  27  36 255] -> [ 23 158  40 255], RGBA -> BGRA
    #print(npimg.shape) #(1080, 1920, 4)
    img.close()
    return npimg

def main():
    x = img_to_bgra('imj.jpg')
    #print(x)

if __name__ == '__main__':
    main()