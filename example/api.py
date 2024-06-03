import torch
from flask import Flask, request, send_file
from flask_cors import CORS
from io import BytesIO
import numpy as np
from pydub import AudioSegment
import ChatTTS
import queue
import time

# 配置 PyTorch
torch._dynamo.config.cache_size_limit = 64
torch._dynamo.config.suppress_errors = True
torch.set_float32_matmul_precision('high')

# 配置接口
port = 7006
host = '0.0.0.0'
route_path = '/app/tts'

# 加载 ChatTTS 模型
chat = ChatTTS.Chat()
# 示例中使用本地模型
chat.load_models(source='local', local_path='/path/to/model')

# 设置随机扬声器
rand_spk = chat.sample_random_speaker()

# 定义推理参数
params_infer_code = {
    'spk_emb': rand_spk,
    'temperature': .3,
    'top_P': 0.7,
    'top_K': 20,
}

params_refine_text = {
    'prompt': '[oral_2][laugh_0][break_4]'
}

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)  # 启用 CORS

# 初始化任务队列，限制并行任务数量
task_queue = queue.Queue(maxsize=2)

def process_tts_task(text):
    # 核心逻辑
    texts = [text]
    wavs = chat.infer(texts, use_decoder=True, skip_refine_text=True, params_refine_text=params_refine_text, params_infer_code=params_infer_code)

    # 确保音频数据在 -1.0 到 1.0 范围内，并转换为 16-bit PCM 格式
    wav_data = np.array(wavs[0])
    wav_data = np.int16(np.clip(wav_data, -1.0, 1.0) * 32767)

    # 创建 pydub 的 AudioSegment 对象
    audio_segment = AudioSegment(
        data=wav_data.tobytes(),
        sample_width=wav_data.dtype.itemsize,
        frame_rate=24000,
        channels=1
    )

    # 将音频数据导出为 MP3 格式
    audio_buffer = BytesIO()
    audio_segment.export(audio_buffer, format='mp3')
    audio_buffer.seek(0)

    return audio_buffer

@app.route(route_path, methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text', '')

    if not text or len(text) < 6:
        return {'error': 'Text too short, must be at least 6 characters.'}, 400

    # 添加任务到队列
    task_queue.put(text)
    while not task_queue.empty():
        try:
            # 从队列中获取任务并处理
            task = task_queue.get()
            audio_buffer = process_tts_task(task)
            task_queue.task_done()
            
            return send_file(audio_buffer, mimetype='audio/mpeg', as_attachment=True, download_name='output.mp3')
        except queue.Full:
            time.sleep(1)  # 等待队列有空位

if __name__ == '__main__':
    app.run(debug=False, host=host, port=port)
