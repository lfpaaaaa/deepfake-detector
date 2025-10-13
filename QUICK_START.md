# 🚀 DeepfakeBench 单帧推理 - 快速开始

## ⚡ 3 步开始使用

### 1️⃣ 查看可用模型

```bash
python tools/list_models.py
```

### 2️⃣ 运行第一个推理

```batch
# Windows
test_inference.bat

# 或手动运行
python tools/predict_frames.py --input data/jobs/job_440557d4147f_1760275209/input.mp4 --model meso4 --fps 2
```

### 3️⃣ 查看结果

检查输出目录：
- `runs/test_infer/meso4/input/scores.csv` - 逐帧分数
- `runs/test_infer/meso4/input/timeline.json` - 可疑时间段

## 📋 常用命令

### 单个视频分析
```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model xception \
  --fps 3 \
  --threshold 0.6
```

### 批量处理
```bash
python tools/predict_frames.py \
  --input data/jobs/ \
  --model f3net \
  --fps 2
```

### 多模型对比
```batch
# 测试 5 个不同模型
test_all_models.bat

# 对比结果
python tools/quick_compare.py --results_dir runs/model_comparison --video input
```

### 融合 VideoMAE 分数
```bash
python tools/fuse_scores.py \
  --frame_csv runs/image_infer/xception/video/scores.csv \
  --videomae_csv runs/videomae/video/scores.csv \
  --alpha 0.6 \
  --out runs/fused/video
```

## 🎯 推荐模型选择

| 场景 | 模型 | FPS | 特点 |
|------|------|-----|------|
| 快速筛查 | `meso4` | 2 | 轻量快速 |
| 标准检测 | `f3net` | 3 | 平衡性能 |
| 高精度 | `xception` | 5 | 最高精度 |
| 实时处理 | `capsule_net` | 2 | 超快速度 |

## 📊 参数说明

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--input` | 视频文件或目录 | 必填 | `video.mp4` |
| `--model` | 模型名称 | 必填 | `xception` |
| `--fps` | 提取帧率 | 3.0 | `2`, `5` |
| `--threshold` | 检测阈值 | 0.5 | `0.6` |
| `--device` | 计算设备 | `cuda` | `cpu` |
| `--outdir` | 输出目录 | `runs/image_infer` | 自定义路径 |

## 🔍 输出文件说明

### scores.csv
```csv
frame_idx,timestamp,prob_fake
0,0.000,0.234567
1,0.333,0.456789
```

### timeline.json
```json
{
  "overall_score": 0.8523,
  "suspicious_segments": [
    [5.2, 12.8],
    [45.6, 58.3]
  ]
}
```

## 📚 更多信息

- **完整文档**: `FRAME_INFERENCE_SETUP.md`
- **详细教程**: `tools/README.md`
- **支持的模型**: 13 个 DeepfakeBench 检测器

## 💡 提示

1. 首次运行会较慢（模型加载）
2. GPU 推理速度约是 CPU 的 10-20 倍
3. FPS 越高越精确，但处理时间也越长
4. 可同时运行多个模型进行对比

## 🐛 问题？

查看 `FRAME_INFERENCE_SETUP.md` 的故障排查部分

