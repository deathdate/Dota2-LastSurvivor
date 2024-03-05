import time, cv2, ctypes, pyautogui
import numpy as np
from mss import mss
from templateMatch import getScreen

time.sleep(2)

### Verify main menu
def inMainPortal():
    target_image = getScreen()
    #target_image = cv2.imread('Templates/mainPortal.jpg')
    template_image = cv2.imread('Templates/guideStageSelection.jpg')

    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(target_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    top_left = max_loc
    bottom_right = (top_left[0] + template_image.shape[1], top_left[1] + template_image.shape[0])

    if matching_percentage > 70:
        """
        cv2.rectangle(target_image, top_left, bottom_right, (0, 255, 0), 2)
        cv2.imshow('Result', target_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        """
        #pyautogui.moveTo(1100, 1250)
        pyautogui.rightClick(portalPosition)

def clicksssdss():
    stageSelectPosition = (bottom_right[0] - 100, bottom_right[1] + 50)
    portalPosition = (bottom_right[0] + 104, bottom_right[1] + 157)  ### 1460, 677
    print(stageSelectPosition)
    print(portalPosition)
    matching_percentage = round(max_val * 100)
    print(f"Matching Percentage: {matching_percentage:.2f}%")


inMainPortal()


##        pyautogui.moveTo(1100, 1250)
##        pyautogui.click()