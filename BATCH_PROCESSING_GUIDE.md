# 🚀 批量处理与高级可视化指南

## 📋 新功能概览

本次升级为 DeepfakeBench 单帧推理系统添加了以下高级功能：

### ✨ 增强的可视化
- **📊 实时概率条**: 视频底部显示当前帧的伪造概率
- **📈 Sparkline 曲线**: 显示最近 5 秒的概率波动趋势
- **🎯 阈值指示线**: 清晰标记检测阈值
- **⚠️ 可疑帧高亮**: 超过阈值的帧用红框标注
- **📊 概率-时间图表**: PNG 格式的完整分析图表
- **📝 SRT 字幕**: 可在播放器中显示可疑时间段

### 🔄 批量处理
- **⚡ 并行处理**: 多进程同时处理多个视频
- **🎮 多 GPU 支持**: 轮询分配 GPU 资源
- **💾 断点续跑**: 自动跳过已完成的视频
- **📊 进度跟踪**: 实时显示处理进度

### 📈 汇总报告
- **📋 CSV 汇总**: 所有结果汇总到一个表格
- **📊 统计分析**: 自动计算各种统计指标
- **🔍 快速筛查**: 快速定位可疑视频

## 🎬 输出文件说明

每个视频处理后会生成以下文件：

```
runs/image_infer/<model>/<video_name>/
├── scores.csv          # 逐帧分数（frame_idx, timestamp, prob_fake）
├── timeline.json       # 可疑片段汇总（含元信息）
├── plot.png           # 📊 概率-时间曲线图
├── segments.srt       # 📝 SRT 字幕文件
├── vis.mp4           # 🎬 可视化视频（带概率条和曲线）
└── meta.txt          # 📄 元数据（模型、参数、统计信息）
```

### 各文件详解

#### 📊 `plot.png` - 概率曲线图
- X 轴：时间（秒）
- Y 轴：伪造概率（0-1）
- 红色虚线：检测阈值
- 红色阴影：可疑时间段

#### 🎬 `vis.mp4` - 可视化视频
- **主画面**: 原视频内容（缩放到 960x540）
- **底部概率条**:
  - 绿色→红色渐变：表示概率从低到高
  - 白色竖线：阈值位置
  - 白色曲线：最近 5 秒的概率 sparkline
- **左上角文字**: `p_fake=0.xxx  t=mm:ss`
- **右上角文字**: 模型名称和阈值
- **红框**: 超过阈值时显示

#### 📝 `segments.srt` - 字幕文件
```srt
1
00:00:05,200 --> 00:00:12,800
SUSPECT

2
00:00:45,600 --> 00:00:58,300
SUSPECT
```

**使用方法**: 将 `segments.srt` 与原视频放在同一目录（同名），视频播放器会自动加载字幕，在可疑时间段显示 "SUSPECT"。

#### 📄 `meta.txt` - 元数据
```
model=xception
ckpt=vendors/DeepfakeBench/training/weights/xception_best.pth
input_size=299
fps=3.0
threshold=0.6
frames=150
device=cuda
processing_time=45.23s
```

## 🚀 使用方法

### 1️⃣ 单视频推理（带可视化）

```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model xception \
  --fps 3 \
  --threshold 0.6 \
  --save-vis
```

**输出**: 生成所有 6 个文件（包括 `vis.mp4`）

### 2️⃣ 批量处理（多个视频）

```bash
# 基本用法：单 GPU，2 个并行进程
python tools/batch_predict.py \
  --input-dir /path/to/videos \
  --model xception \
  --fps 3 \
  --threshold 0.6 \
  --workers 2 \
  --save-vis

# 多 GPU：GPU 0 和 1 轮询
python tools/batch_predict.py \
  --input-dir /path/to/videos \
  --model f3net \
  --gpus 0,1 \
  --workers 4 \
  --save-vis

# 断点续跑（跳过已完成）
python tools/batch_predict.py \
  --input-dir /path/to/videos \
  --model xception \
  --workers 3

# 强制重新处理所有视频
python tools/batch_predict.py \
  --input-dir /path/to/videos \
  --model xception \
  --workers 3 \
  --overwrite

# 只处理文件名包含特定字符的视频
python tools/batch_predict.py \
  --input-dir /path/to/videos \
  --model xception \
  --pattern "suspect" \
  --workers 2
```

**参数说明**:
- `--input-dir`: 包含视频的目录（会递归搜索）
- `--model`: 模型名称或权重文件
- `--workers`: 并行进程数（建议 2-4）
- `--gpus`: GPU ID 列表（如 `0,1,2`）
- `--pattern`: 文件名过滤（只处理匹配的视频）
- `--overwrite`: 强制重新处理（默认跳过已完成）
- `--save-vis`: 生成可视化视频

### 3️⃣ 汇总结果

```bash
# 生成汇总 CSV
python tools/aggregate_runs.py \
  --root runs/image_infer \
  --out runs/summary.csv

# 详细模式（显示处理进度）
python tools/aggregate_runs.py \
  --root runs/image_infer \
  --out runs/summary.csv \
  --verbose
```

**输出 CSV 格式**:
```csv
model,video,overall_score,average_score,segments,flagged_sec,total_frames,fps,threshold,dir
xception,video1,0.856234,0.423456,2,15.60,150,3.0,0.6,runs/image_infer/xception/video1
f3net,video1,0.789123,0.398765,1,8.20,150,3.0,0.6,runs/image_infer/f3net/video1
```

## 📊 完整工作流程示例

### 场景 1: 快速批量筛查

```bash
# 步骤 1: 使用快速模型批量处理
python tools/batch_predict.py \
  --input-dir data/videos \
  --model meso4 \
  --fps 2 \
  --threshold 0.5 \
  --workers 4

# 步骤 2: 生成汇总报告
python tools/aggregate_runs.py \
  --root runs/image_infer \
  --out runs/quick_scan_summary.csv

# 步骤 3: 查看汇总表，找出高分视频
# 打开 runs/quick_scan_summary.csv
# 筛选 overall_score > 0.7 的视频

# 步骤 4: 对可疑视频用强力模型重新分析
python tools/predict_frames.py \
  --input suspect_video.mp4 \
  --model xception \
  --fps 5 \
  --threshold 0.6 \
  --save-vis
```

### 场景 2: 多模型对比分析

```bash
# 步骤 1: 用多个模型处理同一批视频
python tools/batch_predict.py --input-dir data/videos --model xception --workers 2 --save-vis
python tools/batch_predict.py --input-dir data/videos --model f3net --workers 2 --save-vis
python tools/batch_predict.py --input-dir data/videos --model recce --workers 2 --save-vis

# 步骤 2: 生成汇总报告
python tools/aggregate_runs.py --out runs/multi_model_summary.csv

# 步骤 3: 对比单个视频的多模型结果
python tools/quick_compare.py \
  --results_dir runs/image_infer \
  --video video_name

# 步骤 4: 查看各模型的可视化视频
# runs/image_infer/xception/video_name/vis.mp4
# runs/image_infer/f3net/video_name/vis.mp4
# runs/image_infer/recce/video_name/vis.mp4
```

### 场景 3: 多 GPU 高效处理

```bash
# 使用 4 个 GPU，每个 GPU 运行 2 个进程（总共 8 个并行任务）
python tools/batch_predict.py \
  --input-dir data/large_dataset \
  --model xception \
  --gpus 0,1,2,3 \
  --workers 8 \
  --fps 3 \
  --save-vis

# 实时监控进度（另开终端）
watch -n 5 'find runs/image_infer -name "timeline.json" | wc -l'

# 处理完成后汇总
python tools/aggregate_runs.py --out runs/large_dataset_summary.csv --verbose
```

## 🎯 性能优化建议

### CPU 模式
```bash
# 轻量模型 + 低 FPS + 多进程
python tools/batch_predict.py \
  --input-dir videos \
  --model meso4 \
  --fps 2 \
  --workers 4 \
  --device cpu
```
**预期速度**: ~5-10 秒/视频（取决于 CPU）

### 单 GPU 模式
```bash
# 平衡模型 + 中等 FPS + 适度并行
python tools/batch_predict.py \
  --input-dir videos \
  --model f3net \
  --fps 3 \
  --workers 2
```
**预期速度**: ~3-5 秒/视频

### 多 GPU 模式
```bash
# 强力模型 + 高 FPS + 高并行
python tools/batch_predict.py \
  --input-dir videos \
  --model xception \
  --fps 5 \
  --gpus 0,1 \
  --workers 4 \
  --save-vis
```
**预期速度**: ~2-3 秒/视频

## 📝 字幕使用说明

### 在播放器中使用 SRT

1. **VLC Player**:
   - 将 `segments.srt` 与视频放在同一目录
   - 重命名为与视频相同的文件名（如 `video.mp4` → `video.srt`）
   - 在 VLC 中打开视频，字幕会自动加载
   - 或: 字幕 → 添加字幕文件

2. **MPV Player**:
   ```bash
   mpv video.mp4 --sub-file=segments.srt
   ```

3. **浏览器（HTML5 Video）**:
   ```html
   <video controls>
     <source src="video.mp4" type="video/mp4">
     <track src="segments.srt" kind="subtitles" srclang="en" label="Suspect Segments">
   </video>
   ```

### 自定义字幕样式

SRT 文件可以手动编辑添加样式：
```srt
1
00:00:05,200 --> 00:00:12,800
<font color="red"><b>⚠️ SUSPECT</b></font>
```

## 🔧 故障排查

### 问题：可视化视频无法生成

**症状**: 其他文件都生成了，但没有 `vis.mp4`

**解决方案**:
1. 确认使用了 `--save-vis` 参数
2. 检查 OpenCV 是否正确安装：
   ```bash
   python -c "import cv2; print(cv2.__version__)"
   ```
3. 尝试不同的编码器（修改代码中的 fourcc）

### 问题：批量处理卡住

**症状**: 进程启动后长时间无响应

**解决方案**:
1. 减少 `--workers` 数量
2. 检查 GPU 内存是否充足：`nvidia-smi`
3. 移除 `--save-vis` 以节省资源
4. 使用更轻量的模型

### 问题：汇总报告为空

**症状**: `summary.csv` 只有表头

**解决方案**:
1. 确认推理已完成（存在 `timeline.json`）
2. 检查路径是否正确
3. 使用 `--verbose` 查看详细信息

### 问题：Plot 图表无法生成

**症状**: 警告 "Failed to generate plot"

**解决方案**:
```bash
pip install matplotlib
```

## 📚 依赖要求

新功能需要以下额外依赖：

```bash
pip install matplotlib  # 用于生成图表
```

已有的依赖：
- torch
- torchvision  
- opencv-python
- numpy
- pyyaml

## 🎓 高级技巧

### 1. 自动处理新视频

创建监视脚本（Linux/Mac）:
```bash
#!/bin/bash
# watch_and_process.sh

INPUT_DIR="data/incoming"
MODEL="xception"

while true; do
    python tools/batch_predict.py \
        --input-dir "$INPUT_DIR" \
        --model "$MODEL" \
        --workers 2 \
        --save-vis
    
    python tools/aggregate_runs.py \
        --out runs/latest_summary.csv
    
    sleep 300  # 每 5 分钟检查一次
done
```

### 2. 结合 VideoMAE 分数

```bash
# 1. 单帧推理
python tools/predict_frames.py --input video.mp4 --model xception --fps 3

# 2. VideoMAE 推理（如果已有）
# ...

# 3. 融合
python tools/fuse_scores.py \
  --frame_csv runs/image_infer/xception/video/scores.csv \
  --videomae_csv runs/videomae/video/scores.csv \
  --alpha 0.6 \
  --out runs/fused/video
```

### 3. 导出为报告

```bash
# 生成汇总后，用 Python 转换为 HTML 报告
python -c "
import pandas as pd
df = pd.read_csv('runs/summary.csv')
df.to_html('runs/report.html', index=False)
"
```

## 📊 输出示例

### Timeline JSON
```json
{
  "video": "test_video",
  "model": "xception",
  "threshold": 0.6,
  "total_frames": 150,
  "fps": 3.0,
  "overall_score": 0.8523,
  "average_score": 0.4321,
  "suspicious_segments": [
    [5.2, 12.8],
    [45.6, 58.3]
  ],
  "num_suspicious_segments": 2
}
```

### Meta TXT
```
model=xception
ckpt=vendors/DeepfakeBench/training/weights/xception_best.pth
input_size=299
fps=3.0
threshold=0.6
frames=150
device=cuda
processing_time=45.23s
```

### Summary CSV (部分)
```
model,video,overall_score,average_score,segments,flagged_sec,total_frames,fps,threshold
xception,video1,0.856234,0.423456,2,15.60,150,3.0,0.6
xception,video2,0.234567,0.123456,0,0.00,180,3.0,0.6
f3net,video1,0.789123,0.398765,1,8.20,150,3.0,0.6
```

---

## 🎉 总结

新增的批量处理和可视化功能大大提升了系统的易用性和效率：

- ✅ **更直观**: 可视化视频和图表让结果一目了然
- ✅ **更高效**: 批量处理和多 GPU 支持大幅提升处理速度
- ✅ **更灵活**: 断点续跑和自动汇总节省时间
- ✅ **更专业**: SRT 字幕和元数据满足专业需求

开始使用吧！🚀

