#!/usr/bin/env python3
"""
裁剪照片为标准2寸证件照
2寸照片标准尺寸：3.5cm x 5.3cm (413x626 像素 @ 300dpi)
"""

from PIL import Image
import sys

def crop_to_2inch_photo(input_path, output_path):
    """
    裁剪照片为2寸证件照标准尺寸
    保持人脸居中，适当裁剪
    """
    # 打开图片
    img = Image.open(input_path)
    print(f"原始图片尺寸: {img.size}")
    
    # 2寸照片标准比例 (宽:高 = 3.5:5.3 ≈ 0.66)
    target_ratio = 3.5 / 5.3
    
    # 获取原始尺寸
    orig_width, orig_height = img.size
    orig_ratio = orig_width / orig_height
    
    # 计算裁剪区域
    if orig_ratio > target_ratio:
        # 原图太宽，需要裁剪宽度
        new_width = int(orig_height * target_ratio)
        new_height = orig_height
        # 居中裁剪
        left = (orig_width - new_width) // 2
        top = 0
        right = left + new_width
        bottom = orig_height
    else:
        # 原图太高，需要裁剪高度
        new_width = orig_width
        new_height = int(orig_width / target_ratio)
        # 从顶部开始裁剪（证件照通常头部在上方）
        left = 0
        top = 0
        right = orig_width
        bottom = new_height
    
    # 裁剪图片
    cropped = img.crop((left, top, right, bottom))
    print(f"裁剪后尺寸: {cropped.size}")
    
    # 调整到标准2寸照片尺寸 (413x626 @ 300dpi)
    final_size = (413, 626)
    resized = cropped.resize(final_size, Image.Resampling.LANCZOS)
    print(f"最终尺寸: {resized.size}")
    
    # 保存
    resized.save(output_path, quality=95, dpi=(300, 300))
    print(f"已保存到: {output_path}")

if __name__ == "__main__":
    input_file = "job_applications/cleaning_robot/newphoto.jpeg"
    output_file = "job_applications/cleaning_robot/photo_2inch.jpg"
    
    crop_to_2inch_photo(input_file, output_file)
    print("\n✅ 2寸证件照裁剪完成！")
