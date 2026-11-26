# hiccai-commercial-poster

商业广告海报全案设计与 24 家族参数化出图 Skill（融合 `hiccai-wenan` v4.4.0 真社交货币闭环 + Pinterest 撞色色块 + Artlook 现代网格 + 27 张中文商业满幅标杆）。

## 目录结构

```text
hiccai-commercial-poster/
├── SKILL.md                          # Agent Skill 主指令（支持 Claude Code / Cursor / Codex / Antigravity 等）
├── README.md                         # 本说明文件
├── references/
│   ├── layout-families.md            # 24 大商业版式家族全图鉴（10 满幅 + 4 撞色色块 + 10 平面画册）
│   ├── color-and-blocking.md         # 5 大商业配色公式、6 大图形原语与 WCAG 7:1 对比度规范
│   └── social-copy-playbook.md       # 真社交货币文案铁律与四级商业闭环
├── scripts/
│   ├── poster_engine.py              # 零项目依赖的独立 24 家族参数化排版引擎
│   └── render_poster.py              # 命令行一键出单图 / 批量联排对比图 CLI
└── assets/
    └── fonts/                        # 捆绑思源黑体 / 思源宋体 / Barlow Condensed（OFL 开源商用）
```

## 环境依赖

Python 3.10+，安装基础图像与字体库即可离线独立运行：

```bash
pip install pillow numpy fonttools
```

## 快速上手

```bash
# 查看全部 24 大版式家族
python3 scripts/render_poster.py --list-families

# 生成单张满幅商业海报
python3 scripts/render_poster.py \
  --photo ./strawberry.jpg \
  --brand "果小鲜水果铺" \
  --title "一人吃一半，别抢中间那颗" \
  --subtitle "果小鲜水果铺 · 丹东红颜现摘29.9元/盒" \
  --cta "周末两天到店自取" \
  --offer "29.9元/盒" \
  --family social_sticker_zine \
  --ratio 3:4 \
  --output ./poster.png

# 批量生成 4 大满幅中文商业爆款联排对比图（支持 curated_cn / fullbleed / colorblock / editorial / all）
python3 scripts/render_poster.py \
  --photo ./strawberry.jpg \
  --brand "果小鲜水果铺" \
  --title "一人吃一半，别抢中间那颗" \
  --subtitle "果小鲜水果铺 · 丹东红颜现摘29.9元/盒" \
  --cta "周末两天到店自取" \
  --offer "29.9元/盒" \
  --preset curated_cn \
  --sheet ./poster_sheet.jpg \
  --output-dir ./posters/
```
