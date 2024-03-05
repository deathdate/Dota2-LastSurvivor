import time, cv2, ctypes, pyautogui, sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QPoint
from mss import mss
import numpy as np


def getScreen():
    user32 = ctypes.windll.user32
    sct = mss()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    monitorSize = {'top': 0, 'left': 0, 'width': screensize[0], 'height': screensize[1]}
    return (np.array(sct.grab(monitorSize)))


class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Translucent background percentage (adjust as needed)
        self.translucent_percentage = 90
        # Initialize variables for mouse drag
        self.dragging = False
        self.offset = QPoint()

        ## initialise label
        self.statusLabel()

    def statusLabel(self):
        # Create and set the layout
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Overlay Windowwwwwwwwwwww")
        self.layout.addWidget(self.label)

        # Set static font size
        font = self.label.font()
        font.setPointSize(20)  # Adjust the font size as needed
        self.label.setFont(font)

        # Set static font color
        self.label.setStyleSheet("QLabel { color : grey; }")  # Adjust the color as needed

        # Set static label position
        self.label.setAlignment(Qt.AlignCenter)  # Adjust the alignment as needed

    def paintEvent(self, event):
        painter = QPainter(self)
        alpha_value = int((255 * self.translucent_percentage) / 100)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 128))  # Adjust the alpha value for transparency

    def mousePressEvent(self, event):
        # Capture the initial position of the mouse when pressed
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        # Move the window while dragging
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        # Stop dragging when the mouse is released
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def mouseDoubleClickEvent(self, event):
        # Close the overlay window on double-click
        self.close()

    def updateLabelText(self, new_text):
        # Update the label text dynamically
        self.label.setText(new_text)


def inMainPortal():
    target_image = getScreen()
    # target_image = cv2.imread('Templates/mainPortal.jpg')
    template_image = cv2.imread('Templates/guideStageSelection.jpg')

    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(target_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    top_left = max_loc
    refPoint_bottom_right = (top_left[0] + template_image.shape[1], top_left[1] + template_image.shape[0])

    matching_percentage = max_val * 100
    print(f"Matching Percentage: {matching_percentage:.2f}%")
    if matching_percentage > 70:
        # cv2.rectangle(target_image, top_left, bottom_right, (0, 255, 0), 2)
        # cv2.imshow('Result', target_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # pyautogui.moveTo(1100, 1250)

        stageSelectPosition = (refPoint_bottom_right[0] - 100, refPoint_bottom_right[1] + 50)
        portalPosition = (refPoint_bottom_right[0] + 104, refPoint_bottom_right[1] + 157)  ### 1460, 677
        pyautogui.rightClick(portalPosition)


def mainUI():
    app = QApplication(sys.argv)

    overlay = OverlayWindow()
    overlay.setGeometry(800, 600, 200, 200)  # (position, size)
    overlay.show()

    ## to update statusss
    # overlay.updateLabelText("New Label Text")

    sys.exit(app.exec_())


def mainLoop():
    pass


if __name__ == "__main__":
    mainUI()
    mainLoop()