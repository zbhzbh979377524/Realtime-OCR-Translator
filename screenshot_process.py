import cv2
import numpy as np
import pyautogui
import deepl
import pytesseract
from deep_translator import (GoogleTranslator,
                             PonsTranslator,
                             MyMemoryTranslator,
                             LingueeTranslator)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class ScreenshotProcess:
    def __init__(self, select_area, recognize_language: str, translate_language: str, translator_engine, refresh_time,
                 font_size, user_api):
        self.translator_engine = translator_engine
        self.refresh_time = refresh_time
        self.font_size = font_size
        self.new_ocr_result = None
        self.screenshot_file = None
        self.select_area = select_area
        self.recognize_language = recognize_language
        self.translate_language = translate_language
        self.start_x = select_area[0]
        self.start_y = select_area[1]
        self.end_x = select_area[2]
        self.end_y = select_area[3]
        self.user_api = user_api

        # 设置ocr语言代码
        if recognize_language == "中文" or recognize_language == "中国語" or recognize_language == "Chinese":
            self.recognize_language_code = 'chi_sim'
        elif recognize_language == "日语" or recognize_language == "日本語" or recognize_language == "Japanese":
            self.recognize_language_code = 'jpn'
        elif recognize_language == "韩语" or recognize_language == "韓国語" or recognize_language == "Korean":
            self.recognize_language_code = 'kor'
        else:
            self.recognize_language_code = 'eng'

        # 设置翻译代码
        if translate_language == "中文" or translate_language == "中国語" or translate_language == "Chinese":
            self.translate_language_code = 'zh-cn'
        elif translate_language == "日语" or translate_language == "日本語" or translate_language == "Japanese":
            self.translate_language_code = 'ja'
        elif translate_language == "韩语" or translate_language == "韓国語" or translate_language == "Korean":
            self.translate_language_code = 'ko'
        else:
            self.translate_language_code = 'en'

        # 设置原文的英文
        if recognize_language == "中文" or recognize_language == "中国語" or recognize_language == "Chinese":
            self.from_language_eng = 'chinese (simplified)'
        elif recognize_language == "日语" or recognize_language == "日本語" or recognize_language == "Japanese":
            self.from_language_eng = 'japanese'
        elif recognize_language == "韩语" or recognize_language == "韓国語" or recognize_language == "Korean":
            self.from_language_eng = 'korean'
        else:
            self.from_language_eng = 'english'

        # 设置目标语言的英文
        if translate_language == "中文" or translate_language == "中国語" or translate_language == "Chinese":
            self.trans_lang_eng = 'chinese (simplified)'
        elif translate_language == "日语" or translate_language == "日本語" or translate_language == "Japanese":
            self.trans_lang_eng = 'japanese'
        elif translate_language == "韩语" or translate_language == "韓国語" or translate_language == "Korean":
            self.trans_lang_eng = 'korean'
        else:
            self.trans_lang_eng = 'english'

    def screenshot(self):
        # 检查坐标顺序是否正确，如果不正确就交换坐标值
        if self.start_x > self.end_x:
            self.start_x, self.end_x = self.end_x, self.start_x
        if self.start_y > self.end_y:
            self.start_y, self.end_y = self.end_y, self.start_y

        screenshot = pyautogui.screenshot(
            region=(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y))
        self.screenshot_file = screenshot
        return screenshot

    def ocr(self):
        self.screenshot_file = cv2.cvtColor(np.array(self.screenshot_file), cv2.COLOR_BGR2GRAY)
        new_ocr_result = pytesseract.image_to_string(self.screenshot_file, lang=self.recognize_language_code)
        self.new_ocr_result = " ".join(new_ocr_result.split())
        print(new_ocr_result)
        return new_ocr_result

    def translate(self):
        if self.translator_engine == "GoogleTranslator":
            try:
                translated_text = GoogleTranslator(source='auto', target=self.translate_language_code).translate(
                    self.new_ocr_result)
                print(f"TRANSLATED TEXT: [{translated_text}]")
                return translated_text
            except Exception:
                print("unsupported by GoogleTranslate")

        elif self.translator_engine == "DeeplTranslator":
            try:
                print(self.translate_language_code)
                auth_key = self.user_api
                translator = deepl.Translator(auth_key)
                if self.translate_language_code == 'zh-cn':
                    self.translate_language_code = 'zh'
                result = translator.translate_text(text=self.new_ocr_result, target_lang=self.translate_language_code)
                translated_text = result.text
                print(f"TRANSLATED TEXT: [{translated_text}]")
                return translated_text
            except Exception:
                print("unsupported by DeeplTranslator")

        elif self.translator_engine == "PonsTranslator":
            try:
                translated_text = PonsTranslator(source=self.from_language_eng, target=self.trans_lang_eng).translate(
                    self.new_ocr_result)
                print(f"TRANSLATED TEXT: [{translated_text}]")
                return translated_text
            except Exception:
                print("unsupported by PonsTranslator")
        elif self.translator_engine == "LingueeTranslator":
            try:
                translated_text = LingueeTranslator(source=self.from_language_eng, target=self.trans_lang_eng).translate(
                    self.new_ocr_result)
                print(f"TRANSLATED TEXT: [{translated_text}]")
                return translated_text
            except Exception:
                print("unsupported by LingueeTranslator")
        else:
            try:
                translated_text = MyMemoryTranslator(source=self.from_language_eng, target=self.trans_lang_eng).translate(
                    self.new_ocr_result)
                print(f"TRANSLATED TEXT: [{translated_text}]")
                return translated_text
            except Exception:
                print("unsupported by MyMemoryTranslator")


if __name__ == '__main__':
    screenshot_process = ScreenshotProcess(select_area=(10, 10, 500, 500),
                                           recognize_language='英语',
                                           translate_language='中文',
                                           translator_engine="DeeplTranslator",
                                           refresh_time=0.5,
                                           font_size=10,
                                           user_api="7f48025c-0df4-f8f2-16df-fcb5ae046859:fx")
    screenshot_process.screenshot()
    screenshot_process.ocr()
    screenshot_process.translate()
