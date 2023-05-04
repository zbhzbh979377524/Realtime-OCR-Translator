import os
import sys
import time
import tkinter as tk
import webbrowser
import gettext

import pyautogui

import screenshot_process
from PIL import Image, ImageDraw, ImageFont
from tkinter import ttk, messagebox, colorchooser
from PyQt5.QtCore import QPoint, QRectF, Qt, QRect, QSize
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget


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


def reboot_soft(next_language):
    f = open('cur_language.txt', 'w')
    if next_language == 'zh_CN':
        f.write('zh_CN')
    elif next_language == 'ja_JP':
        f.write('ja_JP')
    else:
        f.write('en_US')
    f.close()
    python = sys.executable
    os.execl(python, python, *sys.argv)
    sys.exit()


class Main:

    def __init__(self):
        self.image = None
        set_language()
        self.x_new_window = None
        self.y_new_window = None
        self.past_translated = None
        self.past_text = None
        self.past_img = None
        self.root = None
        self.select_color = None
        self.select_area = None
        self.icon_img = pyautogui.screenshot(region=(0, 0, 1, 1))
        self.select_range = SelectRange()

    def main(self):
        def start_translation():
            recognize_language = combo_recognize.get()
            translate_language = combo_translate.get()
            translator_engine = combo_translator_engine.get()
            refresh_time = combo_refresh_time.get()
            font_size = font_size_entry.get()
            # 判断输入是否合法
            try:
                font_size = float(font_size)
                font_size = round(font_size)
            except ValueError:
                font_size = 10

            user_api = font_API.get()
            if translator_engine == 'DeeplTranslator' and user_api == '':
                translator_engine = "MyMemoryTranslator"

            self.select_range.get_pos()
            if self.select_range.cur_pos and self.select_range.cur_pos != [0, 0, 0, 0]:
                print(self.select_range.cur_pos)
                print(type(self.select_range.cur_pos))
                selected_area = self.select_range.cur_pos
                self.root.iconify()
                self.open_new_window(selected_area, recognize_language, translate_language, translator_engine,
                                     refresh_time,
                                     font_size, user_api, self.select_color)
            else:
                messagebox.showerror(_("Error"), _("请先选择区域"))

        def select_region():
            del self.select_range.snip
            self.select_range.snip = Snip()
            self.select_range.start()

        def select_color():
            # 弹出颜色选择器对话框
            select_color_temp = colorchooser.askcolor()[1]
            self.select_color = select_color_temp
            return select_color_temp

        self.select_area = ''
        self.select_color = '#000000'

        # 创建宣传图片
        root = tk.Tk()
        set_language()
        if os.path.isfile('./Image/logo.png'):
            img_logo = tk.PhotoImage(file="./Image/logo.png")
        else:
            # 创建一个黄色背景的图像，大小为(160, 160)
            image = Image.new('RGB', (340, 360), color=(204, 255, 255))

            # 获取ImageDraw对象
            draw = ImageDraw.Draw(image)

            # 加载字体
            font = ImageFont.truetype('simhei.ttf', size=22)
            # 设置文本内容
            text_top = 'Realtime_Ocr_Translator'
            text_bottom = 'Logo Picture broken'
            text_bottom_1 = 'file missing'
            text_bottom_2 = 'Recommend to download again '
            text_kaomoji = '(ó﹏ò。)      from Github'
            text_jp = 'Logo読み込み失敗'
            text_jp_2 = 'GitHubからの再ダウンロードを'
            text_zh = 'Logo已损坏          お勧め'
            text_zh_2 = '推荐在GitHub上重新下载完整版'

            # 绘制文本
            draw.text((30, 10), text_top, fill='black', font=font, align='center', angle=-30)
            draw.text((20, 45), text_bottom, fill='black', font=font, align='center', angle=-30)
            draw.text((10, 80), text_bottom_1, fill='black', font=font, align='center', angle=-30)
            draw.text((10, 115), text_bottom_2, fill='black', font=font, align='center', angle=-30)
            draw.text((10, 150), text_kaomoji, fill='black', font=font, align='center', angle=-30)
            draw.text((20, 185), text_jp, fill='black', font=font, align='center', angle=-30)
            draw.text((10, 220), text_jp_2, fill='black', font=font, align='center', angle=-30)
            draw.text((20, 255), text_zh, fill='black', font=font, align='center', angle=-30)
            draw.text((10, 290), text_zh_2, fill='black', font=font, align='center', angle=-30)
            draw.text((30, 325), text_top, fill='black', font=font, align='center', angle=-30)
            image.save('./Image/logo.png')
            img_logo = tk.PhotoImage(file="./Image/logo.png")
        # 隐藏边框和标题栏
        root.overrideredirect(True)
        # 获取屏幕尺寸
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        # 计算图片位置
        x = (screen_width - 340) // 2
        y = (screen_height - 360) // 2
        label = tk.Label(root, image=img_logo)
        root.geometry(f"340x360+{x}+{y}")
        label.pack()
        # 刷新窗口
        root.update()
        time.sleep(1)

        # 关闭宣传图片窗口
        root.destroy()

        # 创建主窗口
        self.root = tk.Tk()
        self.root.geometry(f"500x500+{x}+{y}")
        self.root.title('Realtime-OCR-Translator')
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap("./Image/icon.ico")
        except Exception:
            pass

        # 创建一个标签控件并添加到主窗口
        tabControl = ttk.Notebook(self.root)
        tabControl.pack(expand=1, fill="both")

        # 设置标签控件的样式
        tabControl.configure(style='My.TNotebook')

        # 创建自定义样式
        style = ttk.Style()
        style.configure('My.TNotebook.Tab', font=('Yu Gothic', 12))
        style.configure('My.TNotebook', width=600, height=400)

        # 创建4个标签页
        tab1 = tk.Frame(tabControl)
        tabControl.add(tab1, text=_('主页面'))

        tab2 = tk.Frame(tabControl)
        tabControl.add(tab2, text=_('翻译设置'))

        tab3 = tk.Frame(tabControl)
        tabControl.add(tab3, text=_('通用设置'))

        tab4 = tk.Frame(tabControl)
        tabControl.add(tab4, text=_('关于本软件'))

        # 添加“识别语言”下拉菜单
        label_recognize = ttk.Label(tab1, text=_("识别语言："), font=('Yu Gothic', 14))
        label_recognize.grid(column=0, row=1, padx=10, pady=10)

        combo_recognize = ttk.Combobox(tab1, width=15, values=[_("中文"), _("日语"), _("英语"), _("韩语")],
                                       state="readonly",
                                       font=('Yu Gothic', 12))
        combo_recognize.grid(column=1, row=1, padx=10, pady=10, columnspan=3)
        combo_recognize.current(0)

        # 添加“翻译语言”下拉菜单
        label_translate = ttk.Label(tab1, text=_("翻译语言："), font=('Yu Gothic', 14))
        label_translate.grid(column=0, row=2, padx=10, pady=10)

        combo_translate = ttk.Combobox(tab1, width=15, values=[_("中文"), _("日语"), _("英语"), _("韩语")],
                                       state="readonly",
                                       font=('Yu Gothic', 12))
        combo_translate.grid(column=1, row=2, padx=10, pady=10, columnspan=3)
        combo_translate.current(0)

        # 创建“选择区域”按钮
        button_select_region = tk.Button(tab1, text=_("选择区域"), command=select_region, height=5, width=20,
                                         font=('Yu Gothic', 14))
        button_select_region.grid(column=0, row=3, padx=10, pady=10)

        button_start = tk.Button(tab1, text=_("开始"), command=start_translation, height=5, width=20,
                                 font=('Yu Gothic', 14))
        button_start.grid(column=1, row=3, padx=10, pady=10, columnspan=3)

        # 添加“翻译工具”下拉菜单
        label_translator_engine = tk.Label(tab2, text=_("翻译工具："), font=('Yu Gothic', 14))
        label_translator_engine.grid(column=0, row=0, padx=10, pady=10)

        combo_translator_engine = ttk.Combobox(tab2, width=30,
                                               values=["DeeplTranslator", "GoogleTranslator", "PonsTranslator",
                                                       "LingueeTranslator", "MyMemoryTranslator"], state="readonly",
                                               font=('Yu Gothic', 12))
        combo_translator_engine.grid(column=1, row=0, padx=10, pady=10)
        combo_translator_engine.current(0)

        # 添加“刷新时间”下拉菜单
        label_refresh_time = tk.Label(tab3, text=_("刷新时间： 秒"), font=('Yu Gothic', 12))
        label_refresh_time.grid(column=0, row=1, padx=10, pady=10)

        combo_refresh_time = ttk.Combobox(tab3, width=15, values=["0.5", "1", "2", "3", "4", "5"], state="readonly",
                                          font=('Yu Gothic', 12))
        combo_refresh_time.grid(column=1, row=1, padx=10, pady=10)
        combo_refresh_time.current(1)

        # 添加“字体大小”标签和文本框
        label_font_size = tk.Label(tab3, text=_("字体大小： 输入半角数字"), font=('Yu Gothic', 12))
        label_font_size.grid(column=0, row=2, padx=10, pady=10)

        font_size_entry = ttk.Entry(tab3, width=10, font=('Yu Gothic', 12))
        font_size_entry.grid(column=1, row=2, padx=10, pady=10)

        # 添加“API”标签和文本框
        label_API = tk.Label(tab2, text=_("当你使用Deepl时，请输入你的API："), font=('Yu Gothic', 13))
        label_API.grid(column=0, row=2, padx=10, pady=10, columnspan=2)

        font_API = tk.Entry(tab2, width=50, font=13)
        font_API.grid(column=0, row=3, padx=10, pady=10, columnspan=2)

        label2 = tk.Label(tab2, text=_('免费获取Deepl API（官网）'), foreground='blue',
                          font='TkDefaultFont 14 underline', cursor='hand2')
        label2.grid(column=0, row=5, padx=10, pady=10, columnspan=2)
        label2.bind('<Button-1>',
                    lambda event: webbrowser.open_new(_('https://www.deepl.com/zh/pro-api?cta=header-pro-api/')))

        # キャンバス作成
        canvas = tk.Canvas(tab4, bg="#deb887", height=155, width=155, cursor='hand2')
        # キャンバス表示
        canvas.place(x=170, y=10)
        canvas.bind('<Button-1>',
                    lambda event: webbrowser.open_new('https://twitter.com/zzzzzzbh'))
        # 在 Canvas 上添加图片

        if os.path.isfile('./Image/twitter.png'):
            pass
        else:
            # 创建一个黄色背景的图像，大小为(160, 160)
            image_temp = Image.new('RGB', (160, 160), color='yellow')

            # 获取ImageDraw对象
            draw = ImageDraw.Draw(image_temp)

            # 加载字体
            font = ImageFont.truetype('simhei.ttf', size=16)
            # 设置文本内容
            text_top = 'twitter:@zzzzzzbh'
            text_bottom = 'avatar loading'
            text_kaomoji = '(ó﹏ò。)  failed'
            text_top_recommend_0 = 'file missing'
            text_top_recommend = 'recommend to '
            text_top_recommend_2 = '  download again'

            # 绘制文本
            draw.text((23, 30), text_top, fill='black', font=font, align='center', angle=-30)
            draw.text((10, 50), text_bottom, fill='black', font=font, align='center', angle=-30)
            draw.text((20, 70), text_kaomoji, fill='black', font=font, align='center', angle=-30)
            draw.text((30, 95), text_top_recommend_0, fill='black', font=font, align='center', angle=-30)
            draw.text((5, 110), text_top_recommend, fill='black', font=font, align='center', angle=-30)
            draw.text((10, 125), text_top_recommend_2, fill='black', font=font, align='center', angle=-30)
            image_temp = image_temp.rotate(30)
            image_temp.save('./Image/twitter.png')

        image = tk.PhotoImage(file="./Image/twitter.png")
        canvas.create_image(0, 0, anchor=tk.NW, image=image)
        # 添加“twitter”标签和文本框
        label_twitter = tk.Label(tab4, text="Twitter：", font=('Yu Gothic', 14))
        label_twitter.grid(column=0, row=2, padx=10, pady=10)

        # 添加空白标签和文本框
        label_block = tk.Label(tab4, text="@zzzzzzbh", font=('Yu Gothic', 12), foreground='blue', cursor='hand2')
        label_block.grid(column=0, row=3, padx=10, pady=50)
        label_block.bind('<Button-1>',
                         lambda event: webbrowser.open_new(
                             'https://twitter.com/zzzzzzbh'))
        # 添加“github”标签和文本框
        label_github = tk.Label(tab4, text="Github：", font=('Yu Gothic', 14))
        label_github.grid(column=0, row=6, padx=10, pady=10)
        label_github_url = tk.Label(tab4, text='https://github.com/zbhzbh979377524/Realtime-OCR-Translator',
                                    foreground='blue', font='TkDefaultFont 14 underline', cursor='hand2',
                                    wraplength=310)
        label_github_url.grid(column=1, row=6, padx=10, pady=10)
        label_github_url.bind('<Button-1>',
                              lambda event: webbrowser.open_new(
                                  'https://github.com/zbhzbh979377524/Realtime-OCR-Translator'))
        # 添加点星标签和文本框
        label_star = tk.Label(tab4, text=_("如果觉得好用希望可以点个小星星"), font=('Yu Gothic', 14), foreground='red')
        label_star.grid(column=0, row=7, padx=10, pady=10, columnspan=2)
        # 在通用设置中添加一个选择颜色按钮
        color_button = tk.Button(tab3, text=_("选择字的颜色"), command=select_color, height=5, width=20,
                                 font=('Yu Gothic', 12))
        color_button.grid(pady=10)
        # 添加“Tesseract OCR”标签和文本框
        tesseract_msg = tk.Label(tab1, text=_("本软件ocr(文字识别)基于Tesseract OCR，必须安装该软件才可使用"),
                                 foreground='red', font=('Yu Gothic', 14), wraplength=450)
        tesseract_msg.grid(column=0, row=4, padx=10, pady=10, columnspan=5)

        # 添加Tesseract下载页面文本框和超链接
        tesseract_info = tk.Label(tab1, text=_('Tesseract OCR下载网站'),
                                  foreground='blue', font='TkDefaultFont 14 underline', cursor='hand2')
        tesseract_info.grid(column=0, row=5, padx=10, pady=5, columnspan=5)
        tesseract_info.bind('<Button-1>',
                            lambda event: webbrowser.open_new(
                                'https://github.com/UB-Mannheim/tesseract/wiki'))
        # 添加Tesseract下载直链
        tesseract_download = tk.Label(tab1, text=_('Tesseract OCR,64位系统下载直链'),
                                      foreground='blue', font='TkDefaultFont 14 underline', cursor='hand2')
        tesseract_download.grid(column=0, row=6, padx=10, pady=10, columnspan=5)
        tesseract_download.bind('<Button-1>',
                                lambda event: webbrowser.open_new(
                                    'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1'
                                    '.20230401.exe'))

        # 添加软件语言选择
        # 创建 label
        label_UI_language = tk.Label(tab1, text='UI Language/表示言語/页面语言:', font=('Yu Gothic', 11))
        label_UI_language.grid(column=0, row=0, padx=10, pady=10)

        # 创建选项按钮
        button_cn = tk.Button(tab1, text='CN', font=('Yu Gothic', 11),
                              command=lambda: reboot_soft(next_language='zh_CN'))
        button_jp = tk.Button(tab1, text='JP', font=('Yu Gothic', 11),
                              command=lambda: reboot_soft(next_language='ja_JP'))
        button_en = tk.Button(tab1, text='EN', font=('Yu Gothic', 11),
                              command=lambda: reboot_soft(next_language='en_US'))

        # 将选项按钮与 label 放在同一行
        button_cn.grid(column=1, row=0, padx=10, pady=10)
        button_jp.grid(column=2, row=0, padx=10, pady=10)
        button_en.grid(column=3, row=0, padx=10, pady=10)

        # 启动主循环
        self.root.mainloop()

    # 显示翻译内容的窗口
    def open_new_window(self, select_area, recognize_language, translate_language, translator_engine, refresh_time,
                        font_size, user_api, select_color):
        # 创建新窗口
        new_window = tk.Toplevel()
        print('recognize_language:' + recognize_language)
        print('translate_language' + translate_language)
        # 获取屏幕尺寸
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        # 计算图片位置
        x = (screen_width - 600) // 2
        y = (screen_height - 200) * 3 // 4
        new_window.geometry(f"600x200+{x}+{y}")
        try:
            new_window.iconbitmap("./Image/icon.ico")
        except Exception:
            pass

        def on_close():
            new_window.destroy()
            self.root.deiconify()

        new_window.protocol("WM_DELETE_WINDOW", on_close)
        new_window.title(_("正在使用的翻译工具为：{}").format(translator_engine))
        new_window.geometry("600x200")
        new_window.option_add("*Font", ("Helvetica", font_size))
        # 设置前景色
        new_window.option_add("*foreground", select_color)
        # 将窗口始终显示在最前面
        new_window.wm_attributes('-topmost', 'True')

        self.past_img = Image.open('./Image/twitter.png')
        self.past_text = ''
        self.past_translated = ''

        # 显示翻译内容
        def update_translate():
            translate_object = screenshot_process.ScreenshotProcess(select_area=select_area,
                                                                    recognize_language=recognize_language,
                                                                    translate_language=translate_language,
                                                                    translator_engine=translator_engine,
                                                                    refresh_time=refresh_time,
                                                                    font_size=font_size,
                                                                    user_api=user_api)
            temp_img = translate_object.screenshot()
            # 图片不一样
            if temp_img and temp_img.mode != self.past_img.mode or temp_img.size != self.past_img.size or \
                    temp_img.tobytes() != self.past_img.tobytes():
                translate_object.screenshot_file = temp_img
                self.past_img = temp_img
                temp_text = translate_object.ocr()
                # OCR文字不一样
                if temp_text and temp_text != self.past_text:
                    self.past_text = temp_text
                    translate_object.new_ocr_result = temp_text
                    temp_translated = translate_object.translate()
                    if temp_translated and temp_translated != self.past_translated:
                        self.past_translated = temp_translated
                        translate_label.config(text=self.past_translated)
                    else:
                        pass

                else:
                    pass

            else:
                pass
            translate_label.after(int(float(refresh_time) * 1000), update_translate)

        translate_label = tk.Label(new_window, text=(_("正在使用的翻译工具为：{}").format(translator_engine)),
                                   font=('Yu Gothic', font_size))
        translate_label.pack(pady=5)
        update_translate()


class SelectRange(QMainWindow):
    def __init__(self):
        super().__init__()
        # Snipクラスを呼び出すよ。後で作るよ
        self.cur_pos = None
        self.snip = Snip()

    def start(self):
        # クリックされたらsnipクラスを画面全体で動かすよ
        self.snip.showFullScreen()

    def get_pos(self):
        self.snip.close()
        self.cur_pos = self.snip.rect_coordinates
        self.close()



class Snip(QWidget):
    startPos = QPoint(0, 0)
    endPos = QPoint(0, 0)

    def __init__(self):
        super().__init__()
        self.rect_coordinates = None
        self.btn = None
        screen = QApplication.primaryScreen()
        self.snipScreen = screen.grabWindow(
            QApplication.desktop().winId()
        )
        self.initUI()
        self.confirmBtn = QPushButton("OK", self)
        self.confirmBtn.clicked.connect(self.print_pos)
        self.confirmBtn.hide()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("snip")

    def paintEvent(self, event):
        # 今回は絵を描く場所じゃないよ
        painter = QPainter(self)
        # NoPenにすると線を描画しないよ。便利だね
        painter.setPen(Qt.NoPen)
        # 切り抜く場所の大きさを決めるよ。今回はデスクトップだね
        rectSize = QApplication.desktop().screenGeometry()
        # ペイントの時に使ったdrawImageと同じだね
        # rectSizeで指定した部分にsnipScreenを描画するよ
        painter.drawPixmap(rectSize, self.snipScreen)
        # どこを指定したかを覚えておくために使うよ
        painterPath = QPainterPath()
        # 指定した位置の左上の位置を覚えておくよ
        painterPath.addRect(QRectF(rectSize))
        # 切り取ろうとしている部分を表示するよ
        # どこを切り取ろうとしているか見えないと困るよね。
        painterPath.addRoundedRect(QRectF(self.startPos, self.endPos), 0, 0)
        # 切り取ることができる範囲を塗りつぶすよ。今回はデスクトップ全体のことだね
        painter.setBrush(QBrush(QColor(0, 0, 100, 100)))
        # 切り取ろうとしている場所を表示するよ。
        painter.drawPath(painterPath)

    def mousePressEvent(self, event):
        # クリックした位置を覚えておくよ
        self.startPos = event.pos()

    def mouseMoveEvent(self, event):
        self.endPos = event.pos()
        # 選択されている範囲が変わってもこれで安心だよ
        self.repaint()

    def mouseReleaseEvent(self, event):
        # 左クリックを離した位置を覚えておくよ
        self.endPos = event.pos()

        # 计算确认按钮的位置
        screenGeometry = QApplication.desktop().availableGeometry()
        confirmBtnRect = QRect(self.endPos, QSize(50, 25)).normalized()
        if confirmBtnRect.bottom() > screenGeometry.bottom():
            # 如果确认按钮在屏幕下方，则将其移动到屏幕上方
            confirmBtnRect.moveBottom(self.endPos.y())
        if confirmBtnRect.right() > screenGeometry.right():
            # 如果确认按钮在屏幕右侧，则将其移动到屏幕左侧
            confirmBtnRect.moveRight(self.endPos.x() - confirmBtnRect.width())

        # 设置确认按钮的位置
        self.confirmBtn.setGeometry(confirmBtnRect)

        # 将确认按钮移动到其新位置
        self.confirmBtn.move(confirmBtnRect.topLeft())

        # 確認ボタンを表示する
        self.confirmBtn.show()

    def print_pos(self):
        self.rect_qrect = QRect(self.startPos, self.endPos)
        self.rect_coordinates = [self.startPos.x(), self.startPos.y(), self.endPos.x(), self.endPos.y()]
        print(self.rect_qrect)
        print(type(self.rect_coordinates))
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.main()
    sys.exit(app.exec_())
