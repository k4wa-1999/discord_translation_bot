<h1>ディスコード翻訳ボット</h1>

## 目次

- [環境](#environment)
- [使用ライブラリ](#library)
- [BOT招待URL](#invitation)
- [ボット設定](#setting)
- [使用方法](#usage)
- [コマンド実行](#com)
- [翻訳方法](#translation)

<h2 id="environment">環境</h2>

<p> windows10 </p>

<p>Python 3.9.5 </p>

<p> discord.py 2.1.0 </p>

<h2 id="library">使用ライブラリ</h2>
<p>discrd.py</p>
<p>googletrans</p>

<h3>パッケージインストール</h3>

```python
python.exe -m pip install --upgrade pip
```

↑↑↑　しなくても大丈夫です。 ↑↑↑</p>

```python
pip install --upgrade discord
```

```python
pip install --upgrade googletrans
```

<h2 id="invitation">ボット招待URL</h2>

[ボット招待](https://discord.com/api/oauth2/authorize?client_id=1050799173013868555&permissions=8&scope=bot)

<p>(このBOTには管理者権限が付与されます。)</p>

<h2 id="setting">設定</h2>
<p>discord_bot\config\bot.ini の bot_token にあなたのBOTのトークンを入れてください。</p>
<img alt="トークンセット" src="img/setting.png" />

<h2 id="usage">使用方法</h2>
<p id = "com">/ch_creation を実行するとチャンネル作成することができます。</p>
<img alt="チャンネル作成コマンド" src="img/createcommand1.png" />
<p>追加したい言語のリアクションを押します。(追加したら最後にOKを押します。)</p>
<img alt="チャンネル作成コマンド" src="img/createcommand2.png" />
<p>OKを押した後チャンネルとロールが作成されます。</p>
<img alt="チャンネル作成コマンド" src="img/translation1.png" />
<img alt="チャンネル作成コマンド" src="img/authority2.png" />

<h2 id="translation">翻訳方法</h2>
<p>任意のチャンネルで発言すると、それぞれの言語用チャットに翻訳されたメッセージが送信されます。</p>

- 日本語チャンネル

<img alt="翻訳jp" src="img/translation1.png" />

- 英語チャンネル

<img alt="翻訳en" src="img/translation2.png" />

- 中国語チャンネル

<img alt="翻訳cn" src="img/translation3.png" />

<p>(日本語・英語・中国語・韓国語・タイ語・インドネシア語)を用意しています</p>

<h2 id="authority">権限設定</h2>
<p>通知が多くなることを避けるために権限による閲覧制限をしています。</p>
<p>(権限設定はチャンネル作成時にBOTが自動で行います。)</p>
<img alt="権限1" src="img/authority1.png" />
<img alt="権限2" src="img/authority2.png" />
<p>対象のロールを付与することで見える言語チャンネルを変えることができます。</p>




