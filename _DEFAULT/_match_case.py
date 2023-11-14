def identify_shape(shape):
    match shape:
        case "circle":
            print("It's a circle!")
        case "rectangle":
            print("It's a rectangle!")
        case "triangle":
            print("It's a triangle!")
        case _:
            print("Unknown shape")

identify_shape("circle")
identify_shape("hexagon")