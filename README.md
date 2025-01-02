## 更新履歴

### v1.1
- 各種エラーが出る時に、適切なエラーメッセージが出るようにしました。
- 翻訳文表示とapiから翻訳文取得を非同期にした。これで翻訳文取得している間に文字表示欄が反応なしになる問題を修正した。
- Tesseract OCRへのリンクを更新し、起動時Tesseract OCRがインストールされているかどうかを判断するようにした。
- apiは使いにくいのが多い為、現在deepl(api必要)とgoogle翻訳(api不要)だけにした。
- 文字表示ウィンドウのサイズ変更時の表示を改善

### v1.0
- 初回リリース

## [フルな説明ドキュメントはNoteにて](https://note.com/zbhzbh979377524/n/n81e97ae967b5)
# 使い方

1. [Realtime-OCR-Translator_1_0.zip](https://github.com/zbhzbh979377524/Realtime-OCR-Translator/releases/download/v1.0/Realtime-OCR-Translator_1_0.zip)を解凍して、解凍したフォルダーにあるmain.exeを実行します。

2. メインページの一番上のJPをクリックすればソフトが再起動して日本語版になります。

3. [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)のページにアクセスして、自分のOSに相応しいバージョンのをダウンロードしてインストールします。（本ソフトのメインページの下部から入ることもできます）ここで一番普及してるOS(Windows, 64bit)のバージョンのリンクを貼ります。([tesseract-ocr-w64-setup-5.5.0.20241111.exe](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe) (64 bit))

4. Deeplの個人用翻訳API(Key)を申請します([https://www.deepl.com/ja/pro-api?cta=header-pro-api/](https://www.deepl.com/ja/pro-api?cta=header-pro-api/))。ここでDeepl申請しなくても他のパブリックAPIを使えますが、Deeplの質が一番良いと思うからDeepl申請おすすめです。無料で一ヶ月50万文字まで翻訳できるからほとんど使い切れないです。

5. 本ソフトの翻訳設定で翻訳メソッドとAPIを入力します。（Deepl以外ならAPI入力が不要、今後他のAPIを追加する予定、Deeplを選択してもAPI入力しなければ他のメソッドになる）

6. 認識言語（OCRでどの言語として認識するか）や翻訳言語（どの言語に翻訳するか）を指定して、翻訳範囲指定で認識する範囲（字幕の範囲）を指定して、他の設定でリフレッシュ時間や文字の大きさと色を選択して、スタートをクリックすれば翻訳が開始します。
