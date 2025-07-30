#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 9:50
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .portrait_main import MortalPortraitMain


class MortalPortrait(MortalPortraitMain):
    """
    MortalPortrait类继承自MortalPortraitMain，用于处理图像肖像相关任务。

    Attributes:
        onnx_path (str, optional): ONNX模型文件的路径。默认为None。
    """

    def __init__(self, onnx_path=None):
        """
        初始化MortalPortrait类实例。

        Args:
            onnx_path (str, optional): ONNX模型文件的路径。默认为None。
        """
        super().__init__(onnx_path)

    def image(self, image_path, save_path, input_size=(512, 512)):
        """
        处理输入的图像文件，并将处理结果保存到指定路径。

        Args:
            image_path (str): 输入图像文件的路径。
            save_path (str): 处理结果保存的路径。
            input_size (tuple, optional): 输入图像的尺寸，默认为(512, 512)。
        """
        self._image(image_path, save_path, input_size)
