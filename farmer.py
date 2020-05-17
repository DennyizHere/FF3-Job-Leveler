import pyautogui
import win32gui
import time
import pydirectinput
from PIL import ImageGrab, Image
from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2

def walkingMacro():
    pydirectinput.keyDown('w')
    time.sleep(3)
    comparing()
    pydirectinput.keyUp('w')
    pydirectinput.keyDown('s')
    comparing()
    time.sleep(3)
    pydirectinput.keyUp('s')

toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)

def screenshot():
    ff3 = [(hwnd, title) for hwnd, title in winlist if 'final fantasy iii' in title.lower()]
    # just grab the hwnd for first window matching final fantasy iii
    ff3 = ff3[0]
    hwnd = ff3[0]

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    img.save("win2.jpg")

    im = Image.open("win2.jpg")

    left = 10
    top = 80
    right = 1025
    bottom = 130

    im2 = im.crop((left, top, right, bottom))
    im2.save("banner2.jpg")


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compare_images(imageA, imageB):
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    return [m, s]

def comparing():
    screenshot()
    original = cv2.imread("banner.jpg")
    contrast = cv2.imread("banner2.jpg")
    # convert the images to grayscale
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

    [m, s] = compare_images(original, contrast)
    print(m)
    print(s)
    while m < 1000 and s > .70:
        pydirectinput.press('enter')
        screenshot()
        original = cv2.imread("banner.jpg")
        contrast = cv2.imread("banner2.jpg")
        # convert the images to grayscale
        original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
        [m, s] = compare_images(original, contrast)
        print(m)
        print(s)

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def makeTopWindow():
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if "final fantasy iii" in i[1].lower():
            win32gui.ShowWindow(i[0],5)
            win32gui.SetForegroundWindow(i[0])
            return True
    return False

def main():

    print ("Opening FF3 windows")
    if (makeTopWindow()):
        print ("Successfully made FF3 foreground window")
    else:
        print ("Unable to find FF3 open, exiting program")
        exit(1)

    start = time.time()
    while True:
        print ("Entering walking cycle")
        walkingMacro()




if __name__ == "__main__":
    main()