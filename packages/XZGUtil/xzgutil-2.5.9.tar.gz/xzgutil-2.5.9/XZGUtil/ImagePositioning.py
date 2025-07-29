#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author   : 许老三
# @Time    : 2025/4/24 下午2:18
# @Site    : 技术创新中心
# @File    : ImagePositioning.py
# @Software: PyCharm
from PIL import ImageGrab
import cv2
import numpy as np
from XZGUtil.logger import conlog


def window_rectangle(window):
    """截取主窗口"""
    # 获取窗口的位置和大小
    rect = window.rectangle()  # 获取窗口的矩形区域
    left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
    # 截取窗口区域
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    # 将截图转换为OpenCV格式
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # 转换为BGR格式
    return screenshot


def find_img(win, path, show=True, threshold=0.98,sp=300):
    """
    /&zwnj;**图片命名不要用中文**&zwnj;/
    在指定窗口的截图中查找模板图片，并标记匹配位置。
    参数:
        win: 目标窗口对象（通过pywinauto或其他方式获取）。
        path: 模板图片的路径，默认为'./img/select_true.png'。
        show: 是否显示匹配结果（默认True）
        threshold: 匹配阈值（0-1），只有匹配程度大于等于该值的位置才会被选中（默认0.7）
    返回:
        匹配区域信息列表（包含窗口坐标和屏幕坐标）或False
    """
    try:
        # 获取窗口矩形区域和截图（替换原window_rectangle实现）
        window_rect = win.rectangle()  # 获取窗口的屏幕坐标矩形
        screenshot = win.capture_as_image().convert("RGB")  # 使用pywinauto原生截图方法
        screenshot = np.array(screenshot)  # PIL Image转numpy数组
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # RGB转BGR（OpenCV格式）
        # 读取模板图片（保留彩色信息）
        template = cv2.imread(path, cv2.IMREAD_COLOR)
        if template is None:
            conlog(f"无法读取模板图片，请检查路径: {path}")
            return False
        # 获取模板图片的宽度和高度
        h, w = template.shape[:2]  # 彩色图像的shape为 (height, width, channels)
        # 使用彩色图像进行模板匹配
        res = cv2.matchTemplate(
            screenshot,  # 直接使用BGR三通道截图
            template,  # 三通道模板
            cv2.TM_CCOEFF_NORMED
        )
        loc = np.where(res >= threshold)  # 找到匹配程度大于等于阈值的位置
        # 检查是否找到匹配位置
        if len(loc[0]) == 0:
            return False
        # 遍历所有匹配位置，并在屏幕截图上绘制矩形框
        rel = []
        for pt in zip(*loc[::-1]):  # loc[::-1]将匹配位置从(y, x)转换为(x, y)
            # 窗口相对坐标
            top_left = pt
            bottom_right = (pt[0] + w, pt[1] + h)
            center = (pt[0] + w // 2, pt[1] + h // 2)
            # 转换为屏幕绝对坐标
            screen_top_left = (pt[0] + window_rect.left, pt[1] + window_rect.top)
            screen_bottom_right = (pt[0] + w + window_rect.left, pt[1] + h + window_rect.top)
            screen_center = (pt[0] + w // 2 + window_rect.left, pt[1] + h // 2 + window_rect.top)

            rel.append({
                "window_coords": {
                    "top_left": top_left,
                    "bottom_right": bottom_right,
                    "center": center
                },
                "screen_coords": {
                    "top_left": screen_top_left,
                    "bottom_right": screen_bottom_right,
                    "center": screen_center
                }
            })

        # 显示匹配结果
        if show and rel:
            for pt in zip(*loc[::-1]):
                cv2.rectangle(
                    screenshot,
                    pt,
                    (pt[0] + w, pt[1] + h),
                    (0, 0, 255),
                    2
                )
            cv2.namedWindow('Matched', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('Matched', cv2.WND_PROP_TOPMOST, 1)
            cv2.imshow('Matched', screenshot)
            cv2.waitKey(sp)
            cv2.destroyAllWindows()
        return rel if rel else False
    except Exception as e:
        conlog(f"图像匹配过程中发生错误: {e}")
        return False
