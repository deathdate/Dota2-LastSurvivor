import time, cv2, ctypes
import numpy as np
from mss import mss

time.sleep(2)

def getScreen():
    user32 = ctypes.windll.user32
    sct = mss()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    monitorSize = {'top': 0, 'left': 0, 'width': screensize[0], 'height': screensize[1]}
    return (np.array(sct.grab(monitorSize)))

def templateMatch():
    # Load the images
    #target_image = cv2.imread('Templates/mainPortal.jpg')
    target_image = getScreen()
    template_image = cv2.imread('Templates/guideStageSelection.jpg')

    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(target_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    top_left = max_loc
    bottom_right = (top_left[0] + template_image.shape[1], top_left[1] + template_image.shape[0])

    matching_percentage = max_val * 100
    print(f"Matching Percentage: {matching_percentage:.2f}%")
    if matching_percentage > 70:
        #cv2.rectangle(target_image, top_left, bottom_right, (0, 255, 0), 2)
        #cv2.imshow('Result', target_image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        return bottom_right
    else:
        return None
