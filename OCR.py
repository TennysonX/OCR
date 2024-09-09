# import os
# from PIL import Image
# import pytesseract
# import re

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# folder_path = r"C:\Users\tenpo\Desktop\OCR\Bills"

# # สร้างโฟลเดอร์สำหรับเก็บไฟล์ผลลัพธ์ถ้าไม่มี
# output_folder = r"C:\Users\tenpo\Desktop\OCR\Results"
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # ลูปผ่านไฟล์ในโฟลเดอร์
# for filename in os.listdir(folder_path):
#     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#         image_path = os.path.join(folder_path, filename)
#         result_text = ""

#         try:
#             image = Image.open(image_path)
#             custom_config = r'--oem 3 --psm 6'
#             text = pytesseract.image_to_string(image, lang='tha+eng', config=custom_config)
            
#             result_text += f'ข้อความจาก {filename}:\n{text}\n'
#             result_text += '-' * 100 + '\n'

#             # สกัดชื่อสาขา
#             branch_name = re.search(r'(CP Axtra PCL\s+[^\n]+)', text)
#             if branch_name:
#                 result_text += 'ชื่อสาขา: ' + branch_name.group(1) + '\n'

#             # สกัดวันที่และเวลา
#             datetime_info = re.search(r'(\d{2}-\d{2}-\d{4})\s+(\d{2}:\d{2})', text)
#             if datetime_info:
#                 date, time = datetime_info.groups()
#                 result_text += 'วันที่: ' + date + '\n'
#                 result_text += 'เวลา: ' + time + '\n'

#             # สกัดรายการสินค้าที่มีหลายบรรทัด
#             product_pattern = re.compile(r'([^\n]+)\s+(\d+(\.\d+)?)\s*\*\s*(\d+(\.\d+)?)[^\n]*\n(\d+(\.\d+)?)', re.DOTALL)
#             matches = product_pattern.findall(text)
#             result_text += "\nรายการสินค้า:\n"
#             for i, match in enumerate(matches, start=1):
#                 product_name, quantity, _, unit_price, _, total_price, _ = match
#                 result_text += f"{i}. {product_name.strip()}, จำนวน: {quantity}, ราคาต่อหน่วย: {unit_price}, ราคาสินค้า: {total_price}\n"

#             # สกัดยอดรวมใบเสร็จ
#             total = re.search(r'TOTAL\s+(\d+\.\d+)', text)
#             if total:
#                 result_text += '\nยอดรวม: ' + total.group(1) + '\n'

#             result_text += '-' * 100 + '\n'

#             # บันทึกข้อมูลลงในไฟล์
#             output_file = os.path.join(output_folder, filename.split('.')[0] + '.txt')
#             with open(output_file, 'w', encoding='utf-8') as f:
#                 f.write(result_text)

#         except Exception as e:
#             print(f'ไม่สามารถประมวลผลไฟล์ {filename} ได้: {e}')

import os
from PIL import Image
import pytesseract
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# ตั้งค่าพาธของ Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ตั้งค่าโฟลเดอร์เก็บไฟล์ผลลัพธ์
output_folder = r"C:\Users\tenpo\Desktop\OCR\Results"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# ฟังก์ชันสำหรับประมวลผลไฟล์ภาพ
def process_image(image_path):
    result_text = ""
    try:
        image = Image.open(image_path)
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, lang='tha+eng', config=custom_config)
        
        result_text += f'ข้อความจาก {os.path.basename(image_path)}:\n{text}\n'
        result_text += '-' * 100 + '\n'

        # สกัดชื่อสาขา
        branch_name = re.search(r'(CP Axtra PCL\s+[^\n]+)', text)
        if branch_name:
            result_text += 'ชื่อสาขา: ' + branch_name.group(1) + '\n'

        # สกัดวันที่และเวลา
        datetime_info = re.search(r'(\d{2}-\d{2}-\d{4})\s+(\d{2}:\d{2})', text)
        if datetime_info:
            date, time = datetime_info.groups()
            result_text += 'วันที่: ' + date + '\n'
            result_text += 'เวลา: ' + time + '\n'

        # สกัดรายการสินค้าที่มีหลายบรรทัด
        product_pattern = re.compile(r'([^\n]+)\s+(\d+(\.\d+)?)\s*\*\s*(\d+(\.\d+)?)[^\n]*\n(\d+(\.\d+)?)', re.DOTALL)
        matches = product_pattern.findall(text)
        result_text += "\nรายการสินค้า:\n"
        for i, match in enumerate(matches, start=1):
            product_name, quantity, _, unit_price, _, total_price, _ = match
            result_text += f"{i}. {product_name.strip()}, จำนวน: {quantity}, ราคาต่อหน่วย: {unit_price}, ราคาสินค้า: {total_price}\n"

        # สกัดยอดรวมใบเสร็จ
        total = re.search(r'TOTAL\s+(\d+\.\d+)', text)
        if total:
            result_text += '\nยอดรวม: ' + total.group(1) + '\n'

        result_text += '-' * 100 + '\n'

        # บันทึกข้อมูลลงในไฟล์
        output_file = os.path.join(output_folder, os.path.basename(image_path).split('.')[0] + '.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result_text)

    except Exception as e:
        print(f'ไม่สามารถประมวลผลไฟล์ {os.path.basename(image_path)} ได้: {e}')

# สร้างหน้าต่างเพื่อให้ผู้ใช้เลือกไฟล์ภาพ
Tk().withdraw()  # ซ่อนหน้าต่างหลัก
image_path = askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
if image_path:
    process_image(image_path)
else:
    print("ไม่มีไฟล์ถูกเลือก")
