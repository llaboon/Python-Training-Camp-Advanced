# exercises/contour_detection.py
"""
练习：轮廓检测

描述：
使用 OpenCV 检测图像中的轮廓并将其绘制出来。

请补全下面的函数 `contour_detection`。
"""
import cv2
import numpy as np
import os
def contour_detection(image_path):
    """
    使用 OpenCV 检测图像中的轮廓
    参数:
        image_path: 图像路径
    返回:
        tuple: (绘制轮廓的图像, 轮廓列表) 或 (None, None) 失败时
    """
    # 请在此处编写代码
    # 提示：
    # 1. 使用 cv2.imread() 读取图像。
    # 2. 检查图像是否成功读取。
    # 3. 使用 cv2.cvtColor() 转为灰度图。
    # 4. 使用 cv2.threshold() 进行二值化处理。
    # 5. 使用 cv2.findContours() 检测轮廓 (注意不同 OpenCV 版本的返回值)。
    # 6. 创建图像副本 img.copy() 用于绘制。
    # 7. 使用 cv2.drawContours() 在副本上绘制轮廓。
    # 8. 返回绘制后的图像和轮廓列表。
    # 9. 使用 try...except 处理异常。
    try:
        # 检查路径是否存在（优先使用环境变量中的测试图片目录）
        base_dir = os.environ.get('TEST_PICTURE_DIR', '')
        full_path = os.path.join(base_dir, image_path) if base_dir else image_path

        # 如果路径不存在，尝试从测试目录的同级目录查找
        if not os.path.exists(full_path):
            test_dir = os.path.dirname(os.path.abspath(__file__))
            alt_path = os.path.join(test_dir, "..", image_path)
            if os.path.exists(alt_path):
                full_path = alt_path
            else:
                raise FileNotFoundError(f"图像路径不存在: {image_path}")

        # 读取图像
        img = cv2.imread(full_path)
        if img is None:
            raise ValueError(f"无法读取图像（可能损坏或格式不支持）: {full_path}")

        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 二值化处理
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # 检测轮廓（兼容所有OpenCV版本）
        output = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 根据返回值数量判断版本
        if len(output) == 2:  # OpenCV 4.x/3.x
            contours, _ = output
        elif len(output) == 3:  # OpenCV 2.x
            _, contours, _ = output
        else:
            raise ValueError(f"不支持的OpenCV版本: 返回值长度 {len(output)}")

        # 确保contours是列表类型（兼容特殊环境）
        if not isinstance(contours, list):
            contours = list(contours)

        # 绘制轮廓
        img_contours = img.copy()
        cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)

        return img_contours, contours
    except Exception as e:
        print(f"轮廓检测异常: {str(e)}")
        return None, None