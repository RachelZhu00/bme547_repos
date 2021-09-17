## get coordinate of a point on a linea

def getinput():
    print("Enter coordinates in x,y form")
    input_1 = input("Enter the first point.")
    input_2 = input("Enter the second point.")
    coor_x1 = float(input_1.split(',')[0])
    coor_y1 = float(input_1.split(',')[1])
    coor_x2 = float(input_2.split(',')[0])
    coor_y2 = float(input_2.split(',')[1])
    return coor_x1, coor_y1, coor_x2, coor_y2

def line_cal(coor_x1, coor_y1, coor_x2, coor_y2):
    slope = (coor_y2 - coor_y1) / (coor_x2 - coor_x1)
    intercept = coor_y2 -slope * coor_x2
    return slope, intercept

def getinput_2():
    input_x = input("Enter one x coordinate")
    input_x = float(input_x)
    return input_x

def ycoor_cal(slope, intercept, xcoor):
    ycoor = slope * xcoor + intercept
    return ycoor

if __name__ == "__main__":
    x1, y1, x2, y2 = getinput()
    slo, int = line_cal(x1, y1, x2, y2)
    x3 = getinput_2()
    y3 = ycoor_cal(slo, int, x3)
    print("The y-coordinate for x-coordinate you entered is {}".format(y3))
