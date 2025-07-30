from PIL import Image
import json
import math
import sys

imageName = "unnamed"
imageType = "jpg"
#newImageSize = [80, 45]
newImageSize = [30, 30]

paletteData = []

#paletteJson = json.load(open('colors.json',))

#for color in paletteJson:
    #for subColor in paletteJson[color]:
        #paletteData.append(paletteJson[color][subColor])

paletteData = ["ffffff", "0097fe", "00adfa", "00b7fb"]

def HexToRGB(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def PixelateImage(imageName, newImageName, newImageSize=[20,20], paletteData=["ffffff",'888888',"000000"]):
    
    palette = list(map(HexToRGB, paletteData))
    image = Image.open(f'{imageName}').convert('RGB')
    width, height = image.size
    width = math.floor(width / (width / newImageSize[0]))
    height = math.floor(height / (height / newImageSize[1]))
    #image = image.resize((width, height), Image.Resampling.LANCZOS)
    image = image.resize((width, height))
    pix = image.load();

    for x in range(width):
        for y in range(height):
            color = pix[x, y]
            mostSimilarity = 1000000000;
            mostSimilarColor = (0, 0, 0)
            similarity = 0
            for p in palette:
                # similarity = math.sqrt((color[0] - p[0])**2 + (color[1] - p[1])**2 + (color[2] - p[2])**2)
                similarity = 0.3 * ((color[0] - p[0]) ** 2) + 0.59 * ((color[1] - p[1]) ** 2) + 0.11 * (
                            (color[2] - p[2]) ** 2)
                if similarity < mostSimilarity:
                    mostSimilarity = similarity
                    mostSimilarColor = p

            pix[x, y] = mostSimilarColor

    image.show()
    image.save(f'{newImageName}');


if __name__ == '__main__':
    argc = len(sys.argv)

    Nx = 20
    Ny = 20

    for i in range(argc):
        if argc > i+2 and sys.argv[i] == '--size':
            Nx = int(sys.argv[i+1])
            Ny = int(sys.argv[i+2])            

    PixelateImage('Icon_Color.png','Output.png',[Nx,Ny])
