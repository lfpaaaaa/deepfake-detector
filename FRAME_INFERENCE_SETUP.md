# DeepfakeBench 单帧模型推理 - 设置完成

## ✅ 已完成的工作

### 1. 核心文件创建

已创建以下工具文件：

- **`tools/weight_registry.py`** - 权重文件映射表
- **`tools/build_dfbench_model.py`** - 模型加载工厂
- **`tools/predict_frames.py`** - 主推理脚本
- **`tools/fuse_scores.py`** - 分数融合脚本
- **`tools/test_setup.py`** - 系统测试脚本
- **`tools/__init__.py`** - Python 包初始化文件

### 2. 支持的模型

已配置 13 个 DeepfakeBench 模型：

| 模型 | 权重文件 | 输入尺寸 | 状态 |
|------|---------|---------|------|
| Xception | xception_best.pth | 299x299 | ✅ 已就绪 |
| MesoNet-4 | meso4_best.pth | 256x256 | ✅ 已就绪 |
| MesoNet-4 Inception | meso4Incep_best.pth | 256x256 | ✅ 已就绪 |
| F3Net | f3net_best.pth | 224x224 | ✅ 已就绪 |
| EfficientNet-B4 | effnb4_best.pth | 380x380 | ✅ 已就绪 |
| Capsule Net | capsule_best.pth | 128x128 | ✅ 已就绪 |
| SRM | srm_best.pth | 299x299 | ✅ 已就绪 |
| RECCE | recce_best.pth | 224x224 | ✅ 已就绪 |
| SPSL | spsl_best.pth | 224x224 | ✅ 已就绪 |
| FFD | ffd_best.pth | 224x224 | ✅ 已就绪 |
| UCF | ucf_best.pth | 224x224 | ✅ 已就绪 |
| CNN-AUG | cnnaug_best.pth | 224x224 | ✅ 已就绪 |
| CORE | core_best.pth | 224x224 | ✅ 已就绪 |

所有权重文件已放置在: `vendors/DeepfakeBench/training/weights/`

### 3. 功能特性

✅ **逐帧分析**: 可设置任意 FPS 提取帧率
✅ **多模型支持**: 支持 13 种不同的检测模型
✅ **批量处理**: 可处理单个视频或整个目录
✅ **时间线生成**: 自动识别可疑时间段
✅ **分数融合**: 可与 VideoMAE 结果融合
✅ **灵活配置**: 可调整阈值、FPS 等参数
✅ **设备选择**: 支持 GPU (CUDA) 和 CPU 推理

## 🚀 快速开始

### 方式 1: 使用批处理脚本（推荐）

运行提供的测试脚本：

```batch
test_inference.bat
```

### 方式 2: 命令行运行

```bash
# 单个视频推理
python tools/predict_frames.py \
  --input data/jobs/job_440557d4147f_1760275209/input.mp4 \
  --model xception \
  --fps 3 \
  --threshold 0.6 \
  --device cuda

# 批量处理
python tools/predict_frames.py \
  --input data/jobs/ \
  --model meso4 \
  --fps 2 \
  --threshold 0.5 \
  --device cpu
```

## 📊 输出说明

每个视频会在输出目录生成：

### 1. `scores.csv` - 逐帧分数
```csv
frame_idx,timestamp,prob_fake
0,0.000,0.234567
1,0.500,0.456789
2,1.000,0.678901
...
```

### 2. `timeline.json` - 可疑片段汇总
```json
{
  "video": "input",
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

## 🔧 常用命令示例

### 快速筛查（低 FPS + 轻量模型）
```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model meso4 \
  --fps 2 \
  --threshold 0.5
```

### 高精度检测（高 FPS + 强力模型）
```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model xception \
  --fps 5 \
  --threshold 0.6 \
  --device cuda
```

### 批量处理目录
```bash
python tools/predict_frames.py \
  --input data/jobs/ \
  --model f3net \
  --fps 3 \
  --threshold 0.55
```

### CPU 模式（无 GPU 时）
```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model capsule_net \
  --fps 2 \
  --device cpu
```

## 🔗 分数融合（与 VideoMAE 结合）

如果已有 VideoMAE 的分析结果：

```bash
python tools/fuse_scores.py \
  --frame_csv runs/image_infer/xception/video/scores.csv \
  --videomae_csv runs/videomae/video/scores.csv \
  --alpha 0.6 \
  --threshold 0.55 \
  --out runs/fused/video
```

**参数说明：**
- `--alpha`: VideoMAE 的权重（0.6 = 60% VideoMAE + 40% 单帧）
- `--threshold`: 融合后的检测阈值

**输出文件：**
- `scores_fused.csv`: 融合后的逐帧分数
- `timeline_fused.json`: 融合后的可疑片段

## 📈 性能建议

### 速度优先
- 模型: `meso4` 或 `capsule_net`
- FPS: 2
- 设备: GPU (如果可用)

### 精度优先
- 模型: `xception` 或 `efficientnetb4`
- FPS: 5
- 融合: 与 VideoMAE 结合

### 平衡选择
- 模型: `f3net` 或 `recce`
- FPS: 3
- 设备: GPU

## 📁 文件结构

```
deepfake-detector/
├── tools/
│   ├── __init__.py
│   ├── weight_registry.py          # 权重映射
│   ├── build_dfbench_model.py      # 模型构建
│   ├── predict_frames.py           # 主推理脚本
│   ├── fuse_scores.py              # 分数融合
│   ├── test_setup.py               # 测试脚本
│   └── README.md                   # 详细文档
│
├── vendors/DeepfakeBench/
│   └── training/
│       ├── detectors/              # 模型定义
│       ├── config/detector/        # 模型配置
│       └── weights/                # 权重文件 (13个 .pth)
│
├── runs/                           # 推理结果输出
│   ├── image_infer/                # 单帧推理结果
│   │   └── <model_name>/
│   │       └── <video_name>/
│   │           ├── scores.csv
│   │           └── timeline.json
│   └── fused/                      # 融合结果
│       └── <video_name>/
│           ├── scores_fused.csv
│           └── timeline_fused.json
│
├── test_inference.bat              # Windows 快速测试
└── FRAME_INFERENCE_SETUP.md        # 本文档
```

## 🐛 故障排查

### 问题: 找不到模型

**解决方案:**
1. 检查模型名称是否正确（参考支持的模型表）
2. 运行 `python tools/test_setup.py` 检查系统状态

### 问题: CUDA 内存不足

**解决方案:**
```bash
# 降低 FPS
python tools/predict_frames.py --input video.mp4 --model meso4 --fps 2

# 或使用 CPU
python tools/predict_frames.py --input video.mp4 --model meso4 --device cpu
```

### 问题: 权重加载失败

**解决方案:**
1. 确认权重文件存在: `dir vendors\DeepfakeBench\training\weights\`
2. 检查文件大小是否正常（不应该是 0 KB）
3. 如有问题，重新下载对应权重

### 问题: PowerShell 显示异常

这是 PowerShell 控制台的已知问题，不影响实际运行。可以：
1. 使用批处理脚本运行
2. 直接检查输出目录查看结果
3. 或使用标准 CMD 而非 PowerShell

## 📚 更多信息

- **详细使用文档**: `tools/README.md`
- **DeepfakeBench 官方**: https://github.com/SCLBD/DeepfakeBench
- **模型配置**: `vendors/DeepfakeBench/training/config/detector/`

## ✨ 后续扩展

可以进一步添加的功能：

1. **可视化输出**: 在视频上叠加分数曲线
2. **集成检测**: 多个模型投票融合
3. **Web API**: REST API 接口
4. **实时推理**: 摄像头实时检测
5. **报告生成**: 自动生成 PDF/HTML 报告

## 📝 版本信息

- **创建日期**: 2025-10-12
- **支持模型**: 13 个 DeepfakeBench 图像检测器
- **Python 版本**: 3.8+
- **PyTorch 版本**: 1.9+

---

## ⚡ 下一步操作

现在系统已完全配置好，您可以：

1. **运行测试**: 执行 `test_inference.bat` 验证系统
2. **处理视频**: 使用 `tools/predict_frames.py` 分析视频
3. **查看结果**: 检查 `runs/test_infer/` 目录
4. **阅读文档**: 查看 `tools/README.md` 了解更多功能

祝您使用愉快！🎉

