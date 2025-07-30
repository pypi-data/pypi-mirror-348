# 智能语音应答系统客户端
## 简介
这是一个基于`asr`（语音转文字）、`llm`（大语言模型）和`tts`（文字转语音）的智能语音应答系统的客户端辅助代码包(`PyPI`上的名称为`ivrs_client`)，能够帮助用户快速在本地搭建一个能够连接本智能语音应答系统的环境。

### `Audio`
`Audio`类封装了本地录音，发送录音到服务器端并接收服务器返回的语音，以及播放本地录音的功能。包含以下方法
* `__init__`：参数依次为：
  * `url`（必填），即服务器正确的URL；
  * `audio_folder`：储存音频的文件夹（可选，默认为`./audios`）；
  * `silence_duration`：静音检测时长（即超过多长时间的静音会自动停止录音，可选，单位为秒，默认1.5s）；
  * `max_record_seconds`：最长录音时长（单位为秒，默认10s）。
* `record`：本地录音，参数为录音文件保存的名称，可选，默认为`input.wav`，返回值为保存音频的名称
* `send_to_server`:将本地录音发送到服务器，参数依次为:
  * 待上传音频的名称，可选，默认为`input.wav`，可选择使用`record`的返回值；
  * 服务端返回的回答音频的保存名称，可选，默认为`reply.mp3`，返回值为音频保存的名称。

### `Executor`
`Executor`类封装了获取llm的函数调用指令，注册（创建一个函数名到函数对象的映射）指定文件夹下的所有函数，根据llm结果执行函数等功能。包含以下方法：
* `__init__`：参数依次为：
  * `url`（必填），即服务器正确的URL；
  * `functions_folder`：存储函数的文件夹
* `_regeister`：这个不需要用户主动调用，可以认为是`private`的(注：Python中没有真正的私有方法)
* `_add_path`：添加存储函数的文件夹到搜索路径
* `modify_prompt`：根据本地函数信息生成新的`prompt`发送至服务器,本地服务重启前必须调用
* `run`：根据llm的结果调用对应函数
* `get_last_call`：获取最近一次函数调用结果，这个是本地的记录

## 快速开始
### Windows
下载相关依赖`pip -r requirements.txt`，然后`ffmpeg`会在导入包时自动下载，如果下载失败可以尝试手动下载`https://pan.baidu.com/s/1WE4zDeo7h964jy-FP66bBQ?pwd=cvyd`，提取码`cvyd`（这是Windows的exe，其它系统不要下这个）。

### MacOS
相比`Windows`除了`ffmpeg`本身还需要下载一些依赖，本包的`__init__.py`只会检查环境中有没有`ffmpeg`，而不会检查是否安装了相关依赖。
``` bash
brew update
brew install ffmpeg --with-fdk-aac --with-libvpx --with-libass --with-opencore-amr --with-openh264 --with-libtheora --with-libvorbis
```

### Linux
以`Ubuntu`为例，相比`Windows`除了`ffmpeg`本身还需要下载一些依赖，本包的`__init__.py`只会检查环境中有没有`ffmpeg`，而不会检查是否安装了相关依赖。
``` bash
sudo apt update
sudo apt install ffmpeg libx264 libmp3lame libfdk-aac
```

## demo
```py
from client import audio
from client import executor

# 构造函数请填写正确的 URL
client_audio = audio.Audio("http://192.168.106.1:5000","./audios")
client_executor = executor.Executor("http://192.168.106.1:5000","./functions")

# 更新 prompt，这个是必须的
client_executor.modify_prompt()

# 运行循环，函数定义和调用的权限留给用户，包括可以设置退出口令
exit = False
while(not exit):
    # 录音
    wav_path = client_audio.record()
    # 发送
    reply_path = client_audio.send_to_server(wav_path)
    # 播放
    if reply_path:
        client_audio.play(reply_path)
    
    # 函数执行，可选
    client_executor.run()
    # 上一次函数调用的运行时信息，这个是本地的信息
    print(client_executor.last_call_entry)
```