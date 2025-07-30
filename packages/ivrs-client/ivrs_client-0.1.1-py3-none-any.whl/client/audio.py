import pyaudio
import wave
import os
import numpy as np
import requests
from pydub import AudioSegment
from pydub.playback import play

class Audio:
    """负责录音、发送录音到服务器并将返回的语音保存在本地和播放音频"""
    def __init__(self, url, audio_folder = "./audios", silence_duration=1.5, max_record_seconds=10):
        self.url = url
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.silence_threshold = 200
        # 用户可以自行指定静音的检测时长和录音的最大时长
        self.silence_duration = silence_duration
        self.max_record_seconds = max_record_seconds
        self.channels = 1
        self.format = pyaudio.paInt16
        self.audio_folder = audio_folder
        # 检查存放录音的文件夹是否存在，不存在则创建
        if not os.path.exists(self.audio_folder):
            os.makedirs(self.audio_folder)

    # 参数是录音文件的存储路径
    def record(self, file_name="input.wav"):
        """录音并自动检测静音提前结束，保存为 WAV 文件"""
        # 拼接路径
        file_path = self.audio_folder + f"/{file_name}"

        # 录音
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                        channels=self.channels,
                        rate=self.sample_rate,
                        input=True,
                        frames_per_buffer=self.chunk_size)

        print("[录音] 开始录音，请开始说话...")

        frames = []
        silence_chunk_limit = int(self.silence_duration / (self.chunk_size / self.sample_rate))
        silence_count = 0
        total_chunks = int(self.sample_rate / self.chunk_size * self.max_record_seconds)

        for _ in range(total_chunks):
            data = stream.read(self.chunk_size)
            frames.append(data)

            # 静音检测
            audio_np = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(audio_np).mean()
            if volume < self.silence_threshold:
                silence_count += 1
            else:
                silence_count = 0

            if silence_count >= silence_chunk_limit:
                print(f"[录音] 检测到持续静音 {self.silence_duration}s，提前结束录音")
                break

        print("[录音] 结束录音，正在保存文件...")

        stream.stop_stream()
        stream.close()
        p.terminate()

        # 保存为 wav 格式
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(p.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))

        print(f"[完成] 音频已保存至：{file_path}")

        # 返回路径供后续使用
        return file_name

    # 参数是代播放的音频文件的路径
    def play(self, file_name):
        """播放任意格式音频文件"""
        file_path = self.audio_folder + f"/{file_name}"
        print(f"[播放] 正在播放：{file_path}")
        audio = AudioSegment.from_file(file_path)
        play(audio)
        print("[播放] 播放完成")

    # 参数依次是待发送的文件路径和服务器URL
    def send_to_server(self, input_file_name = "input.wav", output_file_name = "reply.mp3"):
        """发送音频文件到后端服务器，接收合成结果"""
        input_file_path = self.audio_folder + f"/{input_file_name}"
        output_file_path = self.audio_folder + f"/{output_file_name}"

        server_url = self.url + "/upload_audio"
        with open(input_file_path, "rb") as f:
            files = {
                "audio": (input_file_path, f, "audio/mpeg")
            }

            try:
                print("[*] 正在发送音频文件...")
                response = requests.post(server_url, files=files)

                if response.status_code == 200:
                    with open(output_file_path, "wb") as out:
                        out.write(response.content)
                    print(f"[+] 成功接收合成音频，已保存为：{output_file_path}")
                    return output_file_name
                else:
                    print(f"[!] 请求失败，状态码: {response.status_code}")
                    print("响应内容：", response.text)
            except Exception as e:
                print(f"[!] 请求出错：{e}")
        return None

if __name__ == "__main__":
    audio = Audio()

    # 录音
    wav_path = audio.record()

    # 播放
    audio.play(wav_path)

    # 发送给后端
    reply_path = audio.send_to_server(wav_path)

    # 播放返回结果
    if reply_path:
        audio.play(reply_path)
