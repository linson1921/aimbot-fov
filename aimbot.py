import cv2
import numpy as np
import pyautogui
import time
import mss

# 目标图像路径（例如：敌人头像图片）
TARGET_IMAGE_PATH = 'target.png'

# FOV 范围设置
FOV_RADIUS = 100  # FOV范围，单位为像素

# 屏幕截图设置
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}  # 你可以修改为你的屏幕分辨率

# 初始化屏幕截图工具
sct = mss.mss()

# 加载目标图像
target_img = cv2.imread(TARGET_IMAGE_PATH, 0)
target_w, target_h = target_img.shape[::-1]

def find_target_on_screen():
    """
    通过图像匹配找到目标位置
    """
    screenshot = np.array(sct.grab(monitor))
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 使用模板匹配查找目标
    res = cv2.matchTemplate(gray_screenshot, target_img, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # 匹配的阈值
    loc = np.where(res >= threshold)

    return loc

def move_to_target(x, y):
    """
    移动鼠标到目标位置
    """
    screen_width, screen_height = pyautogui.size()
    
    # 将目标位置标准化为屏幕坐标
    target_x = x + target_w / 2
    target_y = y + target_h / 2
    
    # 计算鼠标的中心位置
    pyautogui.moveTo(target_x, target_y, duration=0.1)

def is_target_within_fov(x, y):
    """
    检查目标是否在FOV范围内
    """
    screen_width, screen_height = pyautogui.size()
    
    # 获取屏幕中心位置
    center_x = screen_width / 2
    center_y = screen_height / 2
    
    # 计算目标与屏幕中心的距离
    distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    
    return distance <= FOV_RADIUS

def main():
    print("FOV Aimbot 启动...")
    
    while True:
        # 找到目标
        loc = find_target_on_screen()
        
        if loc[0].size > 0:
            # 获取匹配到的目标位置
            for pt in zip(*loc[::-1]):
                x, y = pt
                
                if is_target_within_fov(x, y):
                    print(f"目标位置: ({x}, {y})，在 FOV 范围内，移动鼠标...")
                    move_to_target(x, y)
                else:
                    print(f"目标位置: ({x}, {y})，不在 FOV 范围内，跳过...")
        
        time.sleep(0.1)  # 每 0.1 秒检查一次

if __name__ == "__main__":
    main()
