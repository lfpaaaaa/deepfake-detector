# 🎯 DeepfakeBench V2.0 快速参考

## 🚀 一行命令快速开始

### 单视频（带完整可视化）
```bash
python tools/predict_frames.py --input video.mp4 --model xception --fps 3 --save-vis
```

### 批量处理（2个并行）
```bash
python tools/batch_predict.py --input-dir data/videos --model xception --workers 2
```

### 生成汇总报告
```bash
python tools/aggregate_runs.py
```

## 📁 输出文件一览

```
runs/image_infer/<model>/<video>/
├── scores.csv       # 逐帧分数
├── timeline.json    # 可疑片段
├── plot.png        # 📊 概率图表
├── segments.srt    # 📝 SRT 字幕
├── vis.mp4        # 🎬 可视化视频
└── meta.txt       # 📄 元数据
```

## 🎬 可视化视频说明

### 画面布局
```
┌─────────────────────────────────────┐
│ p_fake=0.xxx  t=mm:ss    MODEL  0.6 │ ← 文字信息
│                                     │
│         原视频内容（960×540）        │
│                                     │
├─────────────────────────────────────┤
│ [████████████████░░░░░░░░░░░░░] │ | │ ← 概率条
│  └── sparkline 曲线 ──┘        ↑   │
└─────────────────────────────────────┘
                                阈值线
```

### 颜色说明
- **绿色**: 低概率（可能真实）
- **橙色**: 中等概率
- **红色**: 高概率（可疑）
- **红框**: 当前帧超过阈值

## 🔧 常用命令模板

### 快速筛查（轻量模型）
```bash
python tools/batch_predict.py \
  --input-dir data/videos \
  --model meso4 \
  --fps 2 \
  --workers 4
```

### 高精度检测（强力模型）
```bash
python tools/batch_predict.py \
  --input-dir data/videos \
  --model xception \
  --fps 5 \
  --threshold 0.6 \
  --workers 2 \
  --save-vis
```

### 多 GPU 加速
```bash
python tools/batch_predict.py \
  --input-dir data/videos \
  --model xception \
  --gpus 0,1,2,3 \
  --workers 8
```

### 断点续跑（跳过已完成）
```bash
python tools/batch_predict.py \
  --input-dir data/videos \
  --model xception \
  --workers 3
  # 自动跳过已有 timeline.json 的视频
```

### 强制重新处理
```bash
python tools/batch_predict.py \
  --input-dir data/videos \
  --model xception \
  --workers 3 \
  --overwrite
```

### 模式过滤（只处理匹配的文件）
```bash
python tools/batch_predict.py \
  --input-dir data/videos \
  --pattern "suspect" \
  --model xception \
  --workers 2
```

## 📊 汇总报告

### 基本用法
```bash
python tools/aggregate_runs.py
# 输出: runs/summary.csv
```

### 自定义输出路径
```bash
python tools/aggregate_runs.py \
  --root runs/image_infer \
  --out my_report.csv
```

### 详细模式
```bash
python tools/aggregate_runs.py --verbose
```

### CSV 列说明
| 列名 | 说明 |
|------|------|
| model | 模型名称 |
| video | 视频名称 |
| overall_score | 最高分数 |
| average_score | 平均分数 |
| segments | 可疑片段数 |
| flagged_sec | 标记总时长（秒） |
| total_frames | 总帧数 |
| fps | 采样率 |
| threshold | 检测阈值 |
| dir | 输出目录 |

## 🎯 典型工作流

### 流程 1: 快速批量筛查
```bash
# 1. 批量处理
python tools/batch_predict.py \
  --input-dir data/videos \
  --model meso4 \
  --workers 4

# 2. 生成汇总
python tools/aggregate_runs.py

# 3. 查看 runs/summary.csv
# 4. 筛选 overall_score > 0.7 的视频
# 5. 对可疑视频用强力模型重新分析
```

### 流程 2: 多模型对比
```bash
# 1. 多个模型处理
python tools/batch_predict.py --input-dir data/videos --model xception --workers 2
python tools/batch_predict.py --input-dir data/videos --model f3net --workers 2
python tools/batch_predict.py --input-dir data/videos --model recce --workers 2

# 2. 汇总所有结果
python tools/aggregate_runs.py --out runs/multi_model.csv

# 3. 对比单个视频
python tools/quick_compare.py \
  --results_dir runs/image_infer \
  --video video_name
```

### 流程 3: 高质量完整分析
```bash
# 1. 高 FPS + 可视化
python tools/predict_frames.py \
  --input important_video.mp4 \
  --model xception \
  --fps 5 \
  --threshold 0.6 \
  --save-vis

# 2. 查看输出
# - plot.png: 查看概率曲线
# - vis.mp4: 观看可视化视频
# - segments.srt: 加载到播放器
# - timeline.json: 查看检测结果
```

## 📝 SRT 字幕使用

### VLC Player
1. 将 `segments.srt` 重命名为与视频同名
2. 放在同一目录
3. 打开视频即可看到字幕

### MPV Player
```bash
mpv video.mp4 --sub-file=segments.srt
```

### 浏览器
```html
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track src="segments.srt" kind="subtitles" default>
</video>
```

## 🔍 结果分析

### 查看单个视频结果
```bash
# 所有文件在这里
cd runs/image_infer/xception/video_name/

# 查看元数据
cat meta.txt

# 查看时间线
cat timeline.json

# 查看图表
open plot.png  # Mac
start plot.png # Windows

# 观看可视化
vlc vis.mp4
```

### 查看批量汇总
```bash
# 用 Excel/LibreOffice 打开
# 或用命令行查看
cat runs/summary.csv | column -t -s,

# Python 查看
python -c "
import pandas as pd
df = pd.read_csv('runs/summary.csv')
print(df.describe())
print(df[df['overall_score'] > 0.7])
"
```

## 🚨 常见问题速查

### 问题：可视化视频无法生成
```bash
# 确认参数
--save-vis  # 必须加这个参数

# 检查 OpenCV
python -c "import cv2; print(cv2.__version__)"
```

### 问题：批量处理卡住
```bash
# 减少 workers
--workers 2  # 降到 2

# 检查 GPU 内存
nvidia-smi

# 不生成可视化（节省资源）
# 移除 --save-vis
```

### 问题：没有 plot.png
```bash
# 安装 matplotlib
pip install matplotlib
```

### 问题：所有视频都被跳过
```bash
# 使用 --overwrite 强制重新处理
--overwrite
```

## ⚡ 性能参考

### 单视频处理时间（参考）
| 模型 | CPU (2fps) | GPU (3fps) | GPU (5fps) |
|------|-----------|-----------|-----------|
| meso4 | ~8s | ~3s | ~5s |
| capsule_net | ~10s | ~4s | ~6s |
| f3net | ~15s | ~5s | ~8s |
| xception | ~30s | ~8s | ~12s |
| recce | ~20s | ~6s | ~10s |

### 批量处理吞吐量（100 个视频）
| 配置 | 时间 | 速度 |
|------|------|------|
| 串行 | ~500s | 1 视频/5s |
| 2 workers | ~250s | 1 视频/2.5s |
| 4 workers | ~125s | 1 视频/1.25s |
| 8 workers (多GPU) | ~62s | 1 视频/0.6s |

## 📚 更多文档

- **快速开始**: `QUICK_START.md`
- **完整文档**: `FRAME_INFERENCE_SETUP.md`
- **批量处理**: `BATCH_PROCESSING_GUIDE.md`
- **升级说明**: `UPGRADE_SUMMARY_V2.md`
- **工具文档**: `tools/README.md`

## 💡 专家提示

1. **先快后慢**: 用轻量模型快速筛查，再用强力模型精确分析
2. **合理并行**: workers 数不要超过 CPU 核心数
3. **断点续跑**: 大批量任务记得定期检查，中断后可直接继续
4. **保存可视化**: 重要视频务必用 `--save-vis`，方便后续审查
5. **多模型验证**: 可疑视频用多个模型交叉验证，提高准确率

## 🎉 开始使用

```bash
# 1. 测试系统
test_inference.bat

# 2. 批量处理你的视频
python tools/batch_predict.py \
  --input-dir your_videos \
  --model xception \
  --workers 2 \
  --save-vis

# 3. 查看结果
python tools/aggregate_runs.py
```

祝你使用愉快！🚀

