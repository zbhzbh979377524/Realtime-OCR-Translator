import cv2
import numpy as np
import pyautogui
import deepl
import pytesseract
from deep_translator import (GoogleTranslator,
                             PonsTranslator,
                             MyMemoryTranslator,
                             LingueeTranslator)
import os
import gettext
from translate import Translator
from googletrans import Translator as GoogleTranslator

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def set_language():
    if os.path.exists('cur_language.txt'):
        with open('cur_language.txt', 'r') as file:
            line = file.readline()
            if line != 'en_US' and line != 'ja_JP' and line != 'zh_CN':
                line = 'en_US'
    else:
        line = 'en_US'

    list1 = [line]
    localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
    translate = gettext.translation(domain='realtime_ocr_translator', localedir=localedir, languages=list1,
                                    fallback=True)
    translate.install()

class ScreenshotProcess:
    @staticmethod
    def is_tesseract_installed():
        """检查Tesseract是否已安装"""
        try:
            # 尝试执行一个简单的OCR测试
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False

    def __init__(self, select_area, recognize_language: str, translate_language: str, translator_engine, refresh_time,
                 font_size, user_api):
        # 首先检查Tesseract是否已安装
        if not self.is_tesseract_installed():
            raise SystemExit("Tesseract OCR not installed")
            
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

        # DeepL用の言語コードを設定
        if translate_language == "中文" or translate_language == "中国語" or translate_language == "Chinese":
            self.translate_code = 'zh'
        elif translate_language == "日语" or translate_language == "日本語" or translate_language == "Japanese":
            self.translate_code = 'ja'
        elif translate_language == "韩语" or translate_language == "韓国語" or translate_language == "Korean":
            self.translate_code = 'ko'
        else:
            self.translate_code = 'en-us'

        # Google用の言語コードを設定
        if translate_language == "中文" or translate_language == "中国語" or translate_language == "Chinese":
            self.google_translate_code = 'zh-cn'
        elif translate_language == "日语" or translate_language == "日本語" or translate_language == "Japanese":
            self.google_translate_code = 'ja'
        elif translate_language == "韩语" or translate_language == "韓国語" or translate_language == "Korean":
            self.google_translate_code = 'ko'
        else:
            self.google_translate_code = 'en'

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
        try:
            set_language()
            if self.screenshot_file is not None:
                # 转换为灰度图像
                img_array = np.array(self.screenshot_file)
                if len(img_array.shape) == 3:
                    gray_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                else:
                    gray_image = img_array
                    
                new_ocr_result = pytesseract.image_to_string(
                    gray_image, 
                    lang=self.recognize_language_code
                )
                # 改行を保持しつつ、余分なスペースのみを削除
                self.new_ocr_result = '\n'.join(line.strip() for line in new_ocr_result.splitlines())
                print(new_ocr_result)
                return new_ocr_result
            else:
                raise RuntimeError(_("截图失败"))
        except Exception as e:
            error_msg = str(e)
            if "TESSDATA_PREFIX" in error_msg or "tessdata" in error_msg:
                raise RuntimeError(_("找不到Tesseract OCR的语言文件"))
            raise RuntimeError(_("OCR错误: ") + str(e))

    def translate(self):
        if self.translator_engine == "GoogleTranslator":
            try:
                translator = GoogleTranslator()
                translated = translator.translate(
                    self.new_ocr_result,
                    dest=self.google_translate_code
                )
                translated_text = translated.text
                print(f"TRANSLATED TEXT: [{translated_text}]")
                return translated_text
            except Exception as e:
                print("Translation failed with Google Translate")
                raise RuntimeError(_("Google翻訳エラー: ") + str(e))

        elif self.translator_engine == "DeeplTranslator":
            # 检查API key是否为空
            if not self.user_api or self.user_api.strip() == "":
                raise RuntimeError(_("请输入DeepL API key"))
           
            try:
                print(self.translate_code)
                auth_key = self.user_api
                translator = deepl.Translator(auth_key)
                if self.translate_code == 'zh-cn':
                    self.translate_code = 'zh'
                result = translator.translate_text(text=self.new_ocr_result, target_lang=self.translate_code)
                translated_text = result.text
                print(f"TRANSLATED TEXT: [{translated_text}]")
                return translated_text
            except deepl.exceptions.AuthorizationException:
                # DeepL APIの認証エラー
                raise RuntimeError(_("DeepL API key is invalid. Please check your API key."))
            except Exception as e:
                error_msg = str(e)
                if "quota" in error_msg.lower():
                    raise RuntimeError(_("DeepL API quota has been exceeded."))
                elif "too many requests" in error_msg.lower():
                    raise RuntimeError(_("Too many requests to DeepL API. Please try again later."))
                else:
                    raise RuntimeError(_("DeepL API Error: ") + error_msg)

        # elif self.translator_engine == "TranslateAPI":
        #     try:
        #         translator = Translator(to_lang=self.translate_code)
        #         translated_text = translator.translate(self.new_ocr_result)
        #         print(f"TRANSLATED TEXT: [{translated_text}]")
        #         return translated_text
        #     except Exception as e:
        #         print("Translation failed with TranslateAPI")
        #         raise RuntimeError(str(e))

        # else:
        #     try:
        #         translated_text = MyMemoryTranslator(source=self.from_language_eng, target=self.trans_lang_eng).translate(
        #             self.new_ocr_result)
        #         print(f"TRANSLATED TEXT: [{translated_text}]")
        #         return translated_text
        #     except Exception as e:
        #         print("unsupported by MyMemoryTranslator")
        #         raise RuntimeError(str(e))


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
