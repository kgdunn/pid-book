import Image
import numpy as np


left = Image.open('brushing-illustration.png')
right = Image.open('brushing-illustration-colour.png')

width = left.size[0] + right.size[0] 
height = max(left.size[1], right.size[1])
result = Image.new("RGBA", (width, height))
result.paste(left, (0, 0))
result.paste(right, (left.size[0], 0))

result.save('brushing-illustration-combined.png')
