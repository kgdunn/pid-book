import Image
import numpy as np

# Plots extracted from MACCMIA's right-click feature

chop = 120

left = Image.open('lumber-example-original-image.png')
mid = Image.open('lumber-example-scores-1.png')
right = Image.open('lumber-example-SPE-after-one-PC.png')

box = (chop, 0, left.size[0]-chop, left.size[1]) # (left, upper, right, lower)
left = left.crop(box)
mid = mid.crop(box)
right = right.crop(box)

width = left.size[0] + right.size[0] + mid.size[0] 
height = max(left.size[1], right.size[1])
result = Image.new("RGBA", (width, height))
result.paste(left, (0, 0))
result.paste(mid, (left.size[0], 0))
result.paste(right, (left.size[0]+mid.size[0], 0))

result.save('lumber-example-combine.png')
