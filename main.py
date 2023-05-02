import tkinter as tk
import webbrowser

import screenshot_process
from PIL import Image
from tkinter import ttk, messagebox, colorchooser


class Main:

    def __init__(self):
        self.past_translated = None
        self.past_text = None
        self.past_img = None
        self.root = None
        self.select_color = None
        self.select_area = None

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
                font_size = 12

            user_api = font_API.get()
            if translator_engine == 'DeeplTranslator' and user_api == '':
                translator_engine = "MyMemoryTranslator"

            selected_region = self.select_area
            if selected_region:
                self.root.iconify()
                self.open_new_window(self.select_area, recognize_language, translate_language, translator_engine,
                                     refresh_time,
                                     font_size, user_api, self.select_color)
            else:
                messagebox.showerror("Error", "请先选择区域")

        def select_region():
            select_region_window = SelectRegionWindow()
            select_region_window.wait_window()
            selection = select_region_window.get_selection()
            self.select_area = selection
            print(self.select_area)
            print(type(self.select_area[0]))
            return selection

        def select_color():
            # 弹出颜色选择器对话框
            select_color_temp = colorchooser.askcolor()[1]
            self.select_color = select_color_temp
            return select_color_temp

        self.select_area = ''
        self.select_color = '#000000'
        # 创建主窗口
        self.root = tk.Tk()
        self.root.geometry('500x500')
        self.root.title('My Software')

        # 创建一个标签控件并添加到主窗口
        tabControl = ttk.Notebook(self.root)
        tabControl.pack(expand=1, fill="both")

        # 创建4个标签页
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='主页面')

        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='翻译设置')

        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3, text='通用设置')

        tab4 = ttk.Frame(tabControl)
        tabControl.add(tab4, text='关于本软件')

        # 添加“识别语言”下拉菜单
        label_recognize = ttk.Label(tab1, text="识别语言：")
        label_recognize.grid(column=0, row=0, padx=10, pady=10)

        combo_recognize = ttk.Combobox(tab1, width=15, values=["中文", "日语", "英语", "韩语"], state="readonly")
        combo_recognize.grid(column=1, row=0, padx=10, pady=10)
        combo_recognize.current(0)

        # 添加“翻译语言”下拉菜单
        label_translate = ttk.Label(tab1, text="翻译语言：")
        label_translate.grid(column=0, row=1, padx=10, pady=10)

        combo_translate = ttk.Combobox(tab1, width=15, values=["中文", "日语", "英语", "韩语"], state="readonly")
        combo_translate.grid(column=1, row=1, padx=10, pady=10)
        combo_translate.current(0)

        # 创建“选择区域”按钮
        button_select_region = ttk.Button(tab1, text="选择区域", command=select_region)
        button_select_region.grid(column=0, row=2, padx=10, pady=10)

        button_start = ttk.Button(tab1, text="开始", command=start_translation)
        button_start.grid(column=1, row=2, padx=10, pady=10)

        # 添加“翻译工具”下拉菜单
        label_translator_engine = ttk.Label(tab2, text="翻译工具：")
        label_translator_engine.grid(column=0, row=0, padx=10, pady=10)

        combo_translator_engine = ttk.Combobox(tab2, width=30,
                                               values=["DeeplTranslator", "GoogleTranslator", "PonsTranslator",
                                                       "LingueeTranslator", "MyMemoryTranslator"], state="readonly")
        combo_translator_engine.grid(column=1, row=0, padx=10, pady=10)
        combo_translator_engine.current(0)

        # 添加“刷新时间”下拉菜单
        label_refresh_time = ttk.Label(tab3, text="刷新时间： 秒")
        label_refresh_time.grid(column=0, row=1, padx=10, pady=10)

        combo_refresh_time = ttk.Combobox(tab3, width=15, values=["0.5", "1", "2", "3", "4", "5"], state="readonly")
        combo_refresh_time.grid(column=1, row=1, padx=10, pady=10)
        combo_refresh_time.current(0)

        # 添加“字体大小”标签和文本框
        label_font_size = ttk.Label(tab3, text="字体大小： 输入半角数字")
        label_font_size.grid(column=0, row=2, padx=10, pady=10)

        font_size_entry = ttk.Entry(tab3, width=10)
        font_size_entry.grid(column=1, row=2, padx=10, pady=10)

        # 添加“API”标签和文本框
        label_API = ttk.Label(tab2, text="当你使用Deepl时，请输入你的API：（可以免费注册）")
        label_API.grid(column=1, row=2, padx=10, pady=10)

        font_API = ttk.Entry(tab2, width=50)
        font_API.grid(column=1, row=3, padx=10, pady=10)

        # # 在翻译设置中添加一个标签
        # label1 = ttk.Label(tab2, text='免费获取Deepl API（Deepl官网）')
        # label1.grid(column=1, row=4, padx=10, pady=10)
        # 在翻译设置中添加一个超链接
        label2 = ttk.Label(tab2, text='免费获取Deepl API（Deepl官网）', foreground='blue', font='TkDefaultFont 10 underline', cursor='hand2')
        label2.grid(column=1, row=5, padx=10, pady=10)
        label2.bind('<Button-1>', lambda event: webbrowser.open_new('https://www.deepl.com/zh/pro-api?cta=header-pro-api/'))



        # 在通用设置中添加一个选择颜色按钮
        color_button = ttk.Button(tab3, text="选择颜色", command=select_color)
        color_button.grid(pady=10)
        # 启动主循环
        self.root.mainloop()

    # 显示翻译内容的窗口
    def open_new_window(self, select_area, recognize_language, translate_language, translator_engine, refresh_time,
                        font_size, user_api, select_color):
        # 创建新窗口
        new_window = tk.Toplevel()

        def on_close():
            new_window.destroy()
            self.root.deiconify()

        new_window.protocol("WM_DELETE_WINDOW", on_close)
        new_window.title(f"正在使用的翻译工具为：{translator_engine}")
        new_window.geometry("600x200")
        new_window.option_add("*Font", ("Helvetica", font_size))
        # 设置前景色
        new_window.option_add("*foreground", select_color)
        # 将窗口始终显示在最前面
        new_window.wm_attributes('-topmost', 'True')

        self.past_img = Image.open('test.png')
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

        # # 显示时间
        # def update_time():
        #     current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        #     time_label.config(text=f"Current Time: {current_time}")
        #     time_label.after(1000, update_time)

        translate_label = tk.Label(new_window, text=f"正在使用的翻译工具为：{translator_engine}",
                                   font=('Yu Gothic', font_size))
        translate_label.pack(pady=5)
        update_translate()


# 选择区域类
class SelectRegionWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        self.geometry("+{}+{}".format(0, 0))
        self.attributes("-fullscreen", True)  # 窗口全屏显示
        self.attributes("-topmost", True)  # 窗口置于顶层
        self.attributes('-alpha', 0.1)
        self.overrideredirect(True)  # 隐藏标题栏、边框等
        self.bind("<Escape>", lambda e: self.close_window())
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rectangle = None
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def on_mouse_down(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if self.rectangle:
            self.canvas.delete(self.rectangle)

        self.rectangle = None

    def on_mouse_move(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

        if self.rectangle:
            self.canvas.delete(self.rectangle)

        self.rectangle = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y,
                                                      outline="red")

    def on_mouse_up(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.close_window()

    def close_window(self):
        self.destroy()

    def get_selection(self):
        if self.start_x is None or self.start_y is None or self.end_x is None or self.end_y is None:
            return None
        return self.start_x, self.start_y, self.end_x, self.end_y


if __name__ == '__main__':
    main = Main()
    main.main()
