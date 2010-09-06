import Image
import numpy as np


gap = 200
left = Image.open('geometric-PCA-1-swarm-only.png')
right = Image.open('geometric-PCA-2-swarm-with-mean.png')
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

result.save('geometric-PCA-1-and-2-swarm-with-mean.png')

# ------------------
gap = 150
left = Image.open('geometric-PCA-3-centered.png')
right = Image.open('geometric-PCA-4-first-component.png')
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

result.save('geometric-PCA-3-and-4-centered-with-first-component.png')

# ------------------
gap = 150
left = Image.open('geometric-PCA-5-first-component-with-projections.png')
right = Image.open('geometric-PCA-6-second-component.png')
tranp = Image.open('transparent-pixel.png')
width = left.size[0] + right.size[0] + gap
height = max(left.size[1], right.size[1])
result = Image.new("RGBA", (width, height))

x = np.arange(0, width)
y = np.arange(0, height)
for xi in x:
    for yi in y:
        result.paste(tranp, (xi, yi))

result.paste(left, (0, 0))
result.paste(right, (left.size[0]+gap, 0))
result.save('geometric-PCA-5-and-6-first-component-with-projections-and-second-component.png')


# ------------------
gap = 150
left = Image.open('geometric-PCA-7-second-component-with-projections.png')
right = Image.open('geometric-PCA-8-noth-components-with-plane.png')
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

result.save('geometric-PCA-7-and-8-second-component-and-both-components.png')
