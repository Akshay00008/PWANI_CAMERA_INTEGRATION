import cv2
import numpy as np

# main gate

# WB2_back_exiting or WB2_front_entering
# WB2_back_entering or WB2_front_exiting

img = cv2.imread(r'images//main_gate_truck_20250507_155158.png')
cropped = img[1000:1825, 1400:2700] # main gate
# cv2.imwrite(r'images//cropped_main_gate_truck_20250507_155158.jpg', cropped)

img = cv2.imread(r'images//WB2_exiting_truck_back_20250507_155531.png')
cropped = img[800:1600, 1700:2900] # WB2_back_exiting or WB2_front_entering
# cv2.imwrite(r'images//cropped_WB2_exiting_truck_back_20250507_155531.jpg', cropped)

img = cv2.imread(r'images//WB2_entering_truck_back_20250507_155452.png')
cropped = img[800:1700, 900:2000] # WB2_back_entering or WB2_front_exiting
# cv2.imwrite(r'images//cropped_WB2_entering_truck_back_20250507_155452.jpg', cropped)

# img = cv2.imread(r'images//WB1_exiting_truck_back_20250508_145339.png')
# cropped = img[400:1350, 850:1800] # WB1_back_exiting or WB1_front_entering
# cv2.imwrite(r'images//cropped_WB1_exiting_truck_back_20250508_145339.jpg', cropped)

img = cv2.imread(r'images//WB1_exiting_truck_front_20250508_145911.png')
cropped = img[650:1850, 1800:3000] # WB1_back_entering or WB1_front_exiting
# cv2.imwrite(r'images//cropped_WB1_exiting_truck_front_20250508_145911.jpg', cropped)

cv2.imwrite(r'images//cropped_img.jpg', cropped)
