# Dynamical Billiards Simulation
# http://en.wikipedia.org/wiki/Dynamical_billiards
# Only 1 ball is simulated.
# FB - 201101027
import math
import random

from PIL import Image, ImageDraw

imgx = 700
imgy = 700
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)

maxSteps = 20000  # of steps of ball motion (in constant speed)

# create a grid of n by m circular obstacles
n = random.randint(1, 9)  # horizontal grid size
m = random.randint(1, 9)  # vertical grid size
crMax = int(min(imgx / (n + 1) / 2, imgy / (m + 1) / 2)) - 1  # max radius
crMin = 10  # min radius
cr = random.randint(crMin, crMax)  # circle radius (same for all grid circles)
cxList = []
cyList = []
crList = []
for j in range(m):
    cy = int((j + 1) * imgy / (m + 1))  # circle center y
    for i in range(n):
        cx = int((i + 1) * imgx / (n + 1))  # circle center x
        cxList.append(cx)
        cyList.append(cy)
        crList.append(cr)
        draw.ellipse((cx - cr, cy - cr, cx + cr, cy + cr))

# initial location of the ball must be outside of the circle(s)
while (True):
    x = float(random.randint(0, imgx - 1))
    y = float(random.randint(0, imgy - 1))
    flag = False
    for i in range(n * m):
        if math.hypot(x - cxList[i], y - cyList[i]) <= crList[i]:
            flag = True
            break
    if flag == False:
        break

# initial direction of the ball
a = 2.0 * math.pi * random.random()
s = math.sin(a)
c = math.cos(a)

for i in range(maxSteps):
    image.putpixel((int(x), int(y)), (255, 255, 255))
    xnew = x + c
    ynew = y + s

    # reflection from the walls
    if xnew < 0 or xnew > imgx - 1:
        c = -c
        xnew = x
    if ynew < 0 or ynew > imgy - 1:
        s = -s
        ynew = y

    # reflection from the circle(s)
    for i in range(n * m):
        if math.hypot(xnew - cxList[i], ynew - cyList[i]) <= crList[i]:
            # angle of the circle point
            ca = math.atan2(ynew - cyList[i], xnew - cxList[i])
            # reversed collision angle of the ball
            rca = math.atan2(-s, -c)
            # reflection angle of the ball
            rab = rca + (ca - rca) * 2
            s = math.sin(rab)
            c = math.cos(rab)
            xnew = x
            ynew = y

    x = xnew
    y = ynew

image.save("Dynamical_Billiards.png", "PNG")
