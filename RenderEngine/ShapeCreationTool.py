import Shape
import RenderEngine2D
import mouse
import time

if __name__ == "__main__":
    engine = RenderEngine2D.RenderEngine()
    points = []
    objectPoints = []
    leftClickDown = False
    rightClickDown = False
    middleClickDown = False
    while True:
        timeMark = time.time()
        inScreenSpace, pos = engine.GetMouseScreenPos()
        if inScreenSpace:
            engine.PieceList = [Shape.Piece([0, 0], [1, 1], points+[pos], [255,255,255])]
        else:
            engine.PieceList = [Shape.Piece([0, 0], [1, 1], points, [255,255,255])]

        engine.PieceList += [Shape.Piece([350, 350], [100, 100], objectPoints, [255,255,255])]
        if len(objectPoints) > 2:
            engine.PieceList += [Shape.Piece([350, 350], [100, 100], Shape.Square(), [255,0,0])]
            engine.PieceList += [Shape.Piece([350, 350], [100, 100], objectPoints, [255,255,255])]

        if mouse.is_pressed(button="left") and not leftClickDown:
            inScreenSpace, pos = engine.GetMouseScreenPos()
            if inScreenSpace:
                points += [pos]
            leftClickDown = True
        elif not mouse.is_pressed(button="left"):
            leftClickDown = False

        if mouse.is_pressed(button="right") and not rightClickDown:
            points = points[:-1]
            rightClickDown = True
        elif not mouse.is_pressed(button="right"):
            rightClickDown = False

        if mouse.is_pressed(button="middle") and not middleClickDown:
            objectPoints = []
            if len(points) > 0:
                minX = points[0][0]
                maxX = points[0][0]
                minY = points[0][1]
                maxY = points[0][1]

                for loop in range(1,len(points)):
                    minX = min(minX, points[loop][0])
                    maxX = max(maxX, points[loop][0])
                    maxY = max(maxY, points[loop][1])
                    minY = min(minY, points[loop][1])

                xWidth = maxX-minX
                yWidth = maxY-minY
                maxWidth = max(xWidth, yWidth)
                for loop in range(len(points)):
                    x = points[loop][0] - minX
                    y = points[loop][1] - minY

                    if xWidth != maxWidth:
                        x += (maxWidth-xWidth)/2

                    if yWidth != maxWidth:
                        y += (maxWidth-yWidth)/2

                    x = ((x / maxWidth)*2)-1
                    y = ((y / maxWidth)*2)-1
                    x = round(x, ndigits=4)
                    y = round(y, ndigits=4)

                    objectPoints += [[x,y]]

            print(objectPoints)
            middleClickDown = True
        elif not mouse.is_pressed(button="middle"):
            middleClickDown = False
        
        timeMark = time.time()-timeMark
        if not engine.UpdateWindow(timeMark):
            break
