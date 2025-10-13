# DeepfakeBench Frame-Level Detection Tools

这套工具允许你使用 DeepfakeBench 的多种模型对视频进行逐帧深度伪造检测。

## 📁 文件说明

- **`weight_registry.py`**: 权重文件到模型配置的映射表
- **`build_dfbench_model.py`**: 自动加载和构建模型的工厂类
- **`predict_frames.py`**: 主推理脚本，对视频逐帧分析
- **`fuse_scores.py`**: 融合单帧分数与 VideoMAE 分数的脚本

## 🚀 快速开始

### 1. 验证权重文件

确认权重文件已放置在正确位置：

```bash
ls vendors/DeepfakeBench/training/weights/
```

应该看到以下文件：
- `xception_best.pth`
- `meso4_best.pth`
- `meso4Incep_best.pth`
- `f3net_best.pth`
- `effnb4_best.pth`
- `capsule_best.pth`
- `srm_best.pth`
- `recce_best.pth`
- `spsl_best.pth`
- `ffd_best.pth`
- `ucf_best.pth`
- `cnnaug_best.pth`
- `core_best.pth`

### 2. 运行单个视频推理

使用 Xception 模型分析视频：

```bash
python tools/predict_frames.py \
  --input data/jobs/job_440557d4147f_1760275209/input.mp4 \
  --model xception \
  --fps 3 \
  --threshold 0.6 \
  --device cuda
```

**参数说明：**
- `--input`: 视频文件路径或包含视频的目录
- `--model`: 模型名称（如 `xception`）或权重文件名（如 `xception_best.pth`）
- `--fps`: 提取帧率（默认 3fps）
- `--threshold`: 可疑片段的阈值（默认 0.5）
- `--device`: 使用的设备（`cuda` 或 `cpu`）
- `--outdir`: 输出目录（默认 `runs/image_infer`）

### 3. 批量处理多个视频

```bash
python tools/predict_frames.py \
  --input data/jobs/ \
  --model f3net \
  --fps 2 \
  --threshold 0.55
```

### 4. 尝试不同模型

#### Xception (高精度，较慢)
```bash
python tools/predict_frames.py --input video.mp4 --model xception
```

#### MesoNet (快速，轻量)
```bash
python tools/predict_frames.py --input video.mp4 --model meso4
```

#### EfficientNet-B4 (平衡)
```bash
python tools/predict_frames.py --input video.mp4 --model efficientnetb4
```

#### F3Net (频域分析)
```bash
python tools/predict_frames.py --input video.mp4 --model f3net
```

## 📊 输出文件

每个视频会生成两个文件：

### `scores.csv`
逐帧的检测分数：
```csv
frame_idx,timestamp,prob_fake
0,0.000,0.234567
1,0.333,0.456789
2,0.667,0.678901
...
```

### `timeline.json`
汇总信息和可疑片段：
```json
{
  "video": "video_name",
  "model": "xception",
  "threshold": 0.6,
  "total_frames": 150,
  "overall_score": 0.8523,
  "average_score": 0.4321,
  "suspicious_segments": [
    [5.2, 12.8],
    [45.6, 58.3]
  ],
  "num_suspicious_segments": 2
}
```

## 🔗 融合 VideoMAE 分数

如果你已经有 VideoMAE 的分析结果，可以将两者融合以提高准确率：

```bash
python tools/fuse_scores.py \
  --frame_csv runs/image_infer/xception/video_name/scores.csv \
  --videomae_csv runs/videomae/video_name/scores.csv \
  --alpha 0.6 \
  --threshold 0.55 \
  --out runs/fused/xception_videomae/video_name
```

**参数说明：**
- `--frame_csv`: 单帧模型的分数文件
- `--videomae_csv`: VideoMAE 的分数文件
- `--alpha`: VideoMAE 的权重（0.6 表示 60% VideoMAE + 40% 单帧）
- `--threshold`: 融合后的阈值
- `--out`: 输出目录

**输出文件：**
- `scores_fused.csv`: 融合后的逐帧分数
- `timeline_fused.json`: 融合后的可疑片段

## 🎯 支持的模型

| 模型 | model_key | 输入尺寸 | 特点 |
|------|-----------|----------|------|
| Xception | `xception` | 299x299 | 高精度，深层网络 |
| MesoNet-4 | `meso4` | 256x256 | 轻量快速 |
| MesoNet-4 Inception | `meso4Inception` | 256x256 | MesoNet 改进版 |
| F3Net | `f3net` | 224x224 | 频域分析 |
| EfficientNet-B4 | `efficientnetb4` | 380x380 | 高效平衡 |
| Capsule Net | `capsule_net` | 128x128 | 胶囊网络 |
| SRM | `srm` | 299x299 | 空间富模型 |
| RECCE | `recce` | 224x224 | 关系感知 |
| SPSL | `spsl` | 224x224 | 自监督学习 |
| FFD | `ffd` | 224x224 | 人脸伪造检测 |
| UCF | `ucf` | 224x224 | 统一对比学习 |
| CNN-AUG | `multi_attention` | 224x224 | 多注意力机制 |
| CORE | `core` | 224x224 | 核心特征 |

## 🔧 高级用法

### 指定自定义权重文件

```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model xception \
  --ckpt /path/to/custom_weights.pth
```

### 调整帧率和阈值

```bash
# 更高的帧率（更精细但更慢）
python tools/predict_frames.py --input video.mp4 --model xception --fps 5

# 更低的阈值（检测更敏感）
python tools/predict_frames.py --input video.mp4 --model xception --threshold 0.4
```

### CPU 模式（无 GPU 时）

```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model meso4 \
  --device cpu
```

## 📈 性能建议

### 速度优化
1. 使用较低的 FPS（如 2-3）进行初步筛查
2. 选择轻量模型（MesoNet, Capsule）用于快速处理
3. 批量处理时使用 GPU

### 精度优化
1. 使用多个模型进行集成
2. 提高 FPS 到 5-10 用于关键视频
3. 融合 VideoMAE 分数
4. 调整阈值根据具体场景

### 推荐组合
- **快速筛查**: MesoNet-4 @ 2fps
- **标准检测**: F3Net @ 3fps
- **高精度**: Xception + VideoMAE 融合 @ 5fps
- **轻量部署**: Capsule Net @ 2fps

## 🐛 故障排查

### 问题：找不到模型

```
[ERROR] Cannot locate detector builder for model_key='xxx'
```

**解决方案：**
1. 检查模型名称是否正确（参考支持的模型表）
2. 确认 DeepfakeBench 代码完整
3. 查看 `vendors/DeepfakeBench/training/detectors/` 是否有对应的 `xxx_detector.py`

### 问题：权重加载失败

```
[ERROR] Failed to load checkpoint
```

**解决方案：**
1. 确认权重文件存在且完整
2. 检查权重文件是否对应正确的模型
3. 尝试重新下载权重文件

### 问题：CUDA 内存不足

```
RuntimeError: CUDA out of memory
```

**解决方案：**
1. 降低 FPS
2. 使用更小的模型（如 MesoNet, Capsule）
3. 使用 CPU 模式：`--device cpu`

### 问题：视频无法打开

```
[ERROR] Failed to open video
```

**解决方案：**
1. 确认视频文件完整且格式支持
2. 尝试使用 ffmpeg 转换视频格式
3. 检查文件路径是否正确

## 📝 示例工作流程

### 完整的检测流程

```bash
# 1. 使用快速模型初步筛查
python tools/predict_frames.py \
  --input data/jobs/ \
  --model meso4 \
  --fps 2 \
  --threshold 0.5 \
  --outdir runs/quick_scan

# 2. 对可疑视频使用高精度模型
python tools/predict_frames.py \
  --input suspicious_video.mp4 \
  --model xception \
  --fps 5 \
  --threshold 0.6 \
  --outdir runs/detailed_scan

# 3. 如果有 VideoMAE 结果，进行融合
python tools/fuse_scores.py \
  --frame_csv runs/detailed_scan/xception/video/scores.csv \
  --videomae_csv runs/videomae/video/scores.csv \
  --alpha 0.6 \
  --threshold 0.55 \
  --out runs/final_result/video
```

## 🔗 相关资源

- [DeepfakeBench GitHub](https://github.com/SCLBD/DeepfakeBench)
- 项目文档: `docs/MODEL_SETUP.md`
- 权重下载指南: `WEIGHTS_DOWNLOAD_GUIDE.md`

## 📄 许可证

遵循 DeepfakeBench 和本项目的许可证要求。

