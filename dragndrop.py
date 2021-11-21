import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(3, 1280)
capture.set(4, 720)
detector = HandDetector(detectionCon=0.5)
colorR = (255, 0, 255)

cx, cy, width, height = 100, 100, 200, 200


class DragRect:
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        width, height = self.size
        if cx - width // 2 < cursor[0] < cx + width // 2 and cy - height // 2 < cursor[1] < cy + height // 2:
            colorR = (0, 255, 0)
            self.posCenter = cursor


rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 250]))
while True:
    success, img = capture.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:
        l, _, _ = detector.findDistance(8, 12, img)
        if l < 65:
            cursor = lmList[8]
            for rect in rectList:
                rect.update(cursor)
    for rect in rectList:
        cx, cy = rect.posCenter
        width, height = rect.size
        cv2.rectangle(img, (cx - width // 2, cy - height // 2), (cx + width // 2, cy + height // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(img, (cx - width // 2, cy - height // 2, width, height), 20, rt=0)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
