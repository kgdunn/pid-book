import Image
import numpy as np

gap = 100
left = Image.open('pca-on-food-texture-both-scores.png')
right = Image.open('pca-on-food-texture-both-loadings.png')
tranp = Image.open('transparent-pixel.png')
width = left.size[0] + right.size[0] + gap
height = max(left.size[1], right.size[1])
result = Image.new("RGBA", (width, height))
result.paste(left, (0, 0))
result.paste(right, (left.size[0]+gap, 0))

if gap>0:
    x = np.arange(left.size[0]+0, left.size[0]+gap)
    y = np.arange(0, height)
    for xi in x:
        for yi in y:
            result.paste(tranp, (xi, yi))

result.save('pca-on-food-texture-scores-and-loadings.png')