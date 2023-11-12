import colorgram

rgb_colors = []
colors = cologram.extract('image.jpg', 30)

for color in colors:
    rgb_colors.append(color.rgb)

print(rgb_colors)