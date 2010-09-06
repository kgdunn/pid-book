import Image
import numpy as np

left = Image.open('frames/020.jpg')
mid = Image.open('frames/169.jpg')
right = Image.open('frames/303.jpg')
width = left.size[0] + right.size[0] + mid.size[0]
height = max(left.size[1], right.size[1])
result = Image.new("RGBA", (width, height))
result.paste(left, (0, 0))
result.paste(mid, (left.size[0], 0))
result.paste(right, (left.size[0]+mid.size[0], 0))

result.save('room-temperature-plots-combine.png')
