# 标注脚本配置与运行

## 配置

JSON 的所有区域均为原始图片像素坐标 `[x, y, width, height]`，不是预览坐标，也不是 `[left, top, right, bottom]`；`crop` 省略时使用整图。脚本不会缩放底图。

```json
{
  "source": "screenshot.png",
  "title": "高级布局设置",
  "context": "选中垂直布局容器；Auto spacing 当前禁用",
  "crop": [1830, 1070, 490, 705],
  "font_family": "Hiragino Sans GB, PingFang SC, Noto Sans CJK SC, sans-serif",
  "label_width": 430,
  "items": [
    {
      "box": [1842, 1420, 454, 54],
      "lines": ["内部描边是否计入布局", "Included / Excluded"]
    },
    {
      "box": [1842, 1484, 454, 53],
      "lines": ["子对象的画布堆叠顺序", "Canvas stacking"]
    },
    {
      "box": [1842, 1613, 454, 52],
      "lines": ["自动间距的分配方式", "Auto spacing（当前禁用）"]
    }
  ]
}
```

- `source` 相对于 JSON 所在目录解析，也支持绝对路径。
- `title`、`context` 可省略；context 写入 SVG 元数据，必要状态也应出现在可见说明中。
- `items` 为非空数组，按目标从上到下排列；编号由数组顺序生成。每个 `lines` 放 1～3 行显式换行的说明。
- 脚本按目标中心安排左侧卡片并向下避让，过密时可能拉长画布；复杂目标分布或交叉箭头需拆图或编辑 SVG。
- 默认 `label_width` 为 430；说明不会自动按中文断行，渲染后若溢出，拆行、缩短说明或增大卡片宽度。
- 配置中的字符串按 XML 转义；图片重编码为 PNG 并内嵌在 SVG，文件不依赖外部图片路径。

## 运行

在有 Python 3、Pillow 的环境中，使用技能目录内脚本；`SKILL_DIR` 应替换为本 skill 所在的绝对路径，配置和输出路径换成本次任务路径。

```bash
python3 "$SKILL_DIR/scripts/annotate.py" annotation.json --svg annotated.svg
```

需要 PNG 时，额外安装的 CairoSVG 必须能找到系统 Cairo 动态库：

```bash
python3 "$SKILL_DIR/scripts/annotate.py" annotation.json --svg annotated.svg --png annotated.png
```

可在已有环境中运行，也可使用 `uv run --with pillow --with cairosvg python ...`，依赖缓存应使用当前环境可写的目录；不强制改变用户的全局 Python 环境。

macOS 若已通过 Homebrew 安装 Cairo，但解释器仍找不到它，可先确认库文件实际路径，再在 Python 进程启动时设置搜索路径。例如 Apple Silicon 常见路径存在时：

```bash
uv run --with pillow --with cairosvg env DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python "$SKILL_DIR/scripts/annotate.py" annotation.json --svg annotated.svg --png annotated.png
```

若渲染器不可用，保留 SVG 并说明 PNG 尚未生成；也可使用环境中已有的 SVG 渲染工具，检查字体、完整画布和实际尺寸后交付。不把依赖失败称为标注成功。

## 检查

脚本校验来源路径、裁切边界、框是否落在裁切范围内以及已有输出文件；不校验说明语义或字体是否存在。生成后用图像查看工具实际查看 PNG，特别检查文字边界和箭头指向。

可抽查未标注区域与底图的像素一致性；这仅证明抽查区域，没有替代对整幅标注内容的检查。
