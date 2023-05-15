import cv2
import numpy as np

    
def tomarPuntos(idImageStr, imageDraw, color):
    points=[]
    def click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append([x, y])
            #print(points)
    cv2.namedWindow(idImageStr)
    cv2.setMouseCallback(idImageStr, click)
    points1 = []
    point_counter = 0
    while True:
        cv2.imshow(idImageStr, imageDraw)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points1 = points.copy()
            points = []
            break
        if len(points) > point_counter:
            point_counter = len(points)
            cv2.circle(imageDraw, (points[-1][0], points[-1][1]), 1, color, -1)
            #print(points)
        if len(points) > 0 and len(points) % 2 == 0:
            #print("longitud ",len(points), points[0])
            x1 = points[len(points)-2]
            x2 = points[len(points)-1]
            
            cv2.rectangle(imageDraw,(x1[0],x1[1]),(x2[0],x2[1]),(255,0,0),1)
    cv2.destroyWindow(idImageStr) #una vez selecionados los puntos cierra la imagen
    print("puntos con click ", points1)
    return points1 # retorna los puntos