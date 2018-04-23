import cv2
import sys

FLOWSKIP = 10

if len(sys.argv) != 3:
  sys.exit("Please input two arguments: imagename1 imagename2")

inputImageFirst = cv2.imread(sys.argv[1], 0)
inputImageSecond = cv2.imread(sys.argv[2], 0)

desImageHS = cv2.imread(sys.argv[1], 1)
desImageLK = cv2.imread(sys.argv[1], 1)

cols, rows = inputImageFirst.shape

cv.SetZero (velx)
cv.SetZero (vely)

cv.CalcOpticalFlowHS(inputImageFirst, inputImageSecond, False, velx, vely, 100.0,(cv.CV_TERMCRIT_ITER | cv.CV_TERMCRIT_EPS,64, 0.01))

for i in range(0, cols, FLOWSKIP):
  for j in range(0, rows, FLOWSKIP):
    dx = int(cv.GetReal2D (velx, j, i))
    dy = int(cv.GetReal2D (vely, j, i))
    cv.Line(desImageHS,(i, j),(i + dx, j + dy), (255, 0, 0), 1, cv.CV_AA, 0)

cv.SetZero (velx)
cv.SetZero (vely)

cv.CalcOpticalFlowLK(inputImageFirst,inputImageSecond,(15,15),velx,vely)

for i in range(0, cols, FLOWSKIP):
  for j in range(0, rows, FLOWSKIP):
    dx = int(cv.GetReal2D (velx, j, i))
    dy = int(cv.GetReal2D (vely, j, i))
    cv.Line(desImageLK,(i, j),(i + dx, j + dy), (255, 0, 0), 1, cv.CV_AA, 0)

cv.SaveImage("resultHS.png", desImageHS)
cv.SaveImage("resultLK.png", desImageLK)

cv.NamedWindow("Optical flow HS")
cv.ShowImage("Optical flow HS", desImageHS)

cv.NamedWindow("Optical flow LK")
cv.ShowImage("Optical flow LK", desImageLK)

cv.WaitKey(0)
cv.DestroyAllWindows()

