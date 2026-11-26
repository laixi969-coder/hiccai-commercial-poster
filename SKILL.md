---
name: hiccai-commercial-poster
description: >-
  商业广告海报全案设计与可执行出图 Skill（融合 hiccai-wenan v4.4.0 真社交货币文案闭环 +
  Pinterest 商业撞色色块 + Artlook 现代网格 + 中文满幅商业大片 24 大参数化版式引擎）。
  适用于商家促销海报、新品主视觉 KV、餐饮生鲜茶饮海报、门店开业/活动海报、小红书/朋友圈单图获客、
  多画幅（3:4 / 9:16 / 1:1 / 16:9）一键出图与视觉审美升级。
  触发词：做海报、商业海报、促销海报、海报设计、视觉设计、换版式、多版式海报、
  商品广告图、朋友圈海报、小红书海报、满幅海报、色块海报、hiccai-commercial-poster。
license: MIT
metadata:
  author: hiccai
  version: 1.0.0
compatibility: >-
  Works with Antigravity, Claude Code, Codex CLI, Cursor, Windsurf, Gemini CLI,
  and any Agent Skills Open Standard compatible runtime. Python 3.10+ with Pillow,
  NumPy, and fontTools required for local rendering scripts.
---

# /hiccai-commercial-poster — 商业广告海报设计与 24 家族参数化出图

交付**顾客一眼想拍给朋友看、商家一眼能核对交易条件、手机小屏一秒读清**的可商用广告海报——彻底终结“老板单向叫卖文案”与“白纸中间贴方框照片的 PPT 模板感”。

## 核心铁律（不可违背）

1. **先写「真社交货币」再排字**：严禁老板单向广播口号（如“下班路过带一盒”“周末特惠等你来”“品质有底气”）。主标题必须把商品的一条真实特性写进**两个人之间的对话、嘴替或动作**里，同时用副标题与行动句完成商业转化闭环。细则见 [references/social-copy-playbook.md](references/social-copy-playbook.md)。
2. **满幅摄影优先（65% 权重）× 零 PPT 贴图感**：顶级中文商业海报绝大多数是 **100% 满幅摄影大片**，把大字、取景框、荧光高光块、倾斜贴纸、竖排宋体与价格转化带直接做在满幅画面上，并自动检测原图低熵负空间避开商品主体。
3. **色彩与对比度硬门槛**：标题对比度 `>= 7.0:1`，正文/副标题 `>= 4.5:1`；整张海报价格**只出现一次**（出现独立价格贴纸/双段券/价格框时自动从副标题剥离重复价格）。
4. **商家实拍原图零破坏**：当用户上传真实门店/商品实拍且需要 100% 保留完整包装/轮廓时，必须启用 `--protect-subject` 锁定非裁切安全家族，绝不切掉商品核心像素。

---

## 标准 4 步执行流程

### Step 1：提取简报与视觉观察
从用户对话与原图中安静提取核心要素（缺关键交易信息才只问缺失项，不发长问卷）：
- **品牌/店名**（`brand`）、**核心商品与真实卖点**（`product / facts`）、**已确认价格与条件**（`offer / terms`，无则留空，严禁编造折扣/限时/包邮/私信接单）
- **投放画幅**：默认 `3:4`（小红书/朋友圈/门店海报）；支持 `9:16`（竖屏/快拍）、`1:1`（方图/商品卡）、`16:9`（横幅/电视屏）
- **原图评估**：有实拍图时，先目检主体位置、主色与最安静的留白区；无实拍图时，先用图像模型生成**无文字、留出呼吸负空间、食欲/质感极强的高清商业底图**，再进入本 Skill 排版合成。

### Step 2：创作四级闭环社交货币文案（先给 3 组不同切口）
按 [references/social-copy-playbook.md](references/social-copy-playbook.md) 产出 3 组真正不同角度的候选文案供确认（除非用户已锁定原话标题）：
- **切口 ① 关系嘴替**：替顾客向伴侣/闺蜜/家人/同事说出带点俏皮或体贴的话（把商品特性与人际关系双关到一起，禁用“比初恋还……”旧套路）
- **切口 ② 两人动作与分工**：把商品特点写进两个人立刻能发生的小动作或抢食/分享默契（如水果店「一人吃一半，别抢中间那颗」）
- **切口 ③ 老客验货 / 生活反差**：像熟客私下拍给朋友看的实在真话（如「洗过就蔫，没洗才敢送人」）

每组必须输出完整四级结构并自检退稿线（如果假想接收人只能回“广告不错/看着好吃/在哪买”，立刻重写）：
- `title`（一级主标题，8–18 字，社交钩子）
- `body`（二级副标题，≤ 20 字，用店名/商品名/真实卖点/价格接住主标题）
- `cta`（三级行动收口，立足顾客当前位置给唯一已确认的下一步）
- `socialPost`（四级朋友圈/小红书配文，60–120 字，含评论区接话口子）

### Step 3：匹配 24 大商业版式家族与色彩系统
按需查阅 [references/layout-families.md](references/layout-families.md) 与 [references/color-and-blocking.md](references/color-and-blocking.md)，按业务目标选定 1 个主推方向或直接批量出 4–8 联排给用户挑：

| 业务场景 | 优先推荐版式家族 | 视觉特征 |
|---|---|---|
| **爆款促销 / 商超生鲜 / 一眼看清价格** | `fresh_retail_promo` / `color_block_diagonal` / `color_block_bento` | 满幅生鲜图+底栏超大白字价、斜切撞色+20齿锯齿贴纸、顶底锚定色带 |
| **小红书 / 年轻社交 / 玩梗茶饮咖啡** | `social_sticker_zine` / `neon_highlighter_poster` / `color_block_swiss_grid` | 满幅实拍+取景框括号+倾斜贴纸+条码+棋盘格、荧光高光块、`2px` 瑞士彩格 |
| **高级感全幅大片 / 品牌 KV / 门店调性** | `full_bleed_clean` / `full_bleed_poster_type` / `full_bleed_band` / `full_bleed_editorial_edge` | 自动避开主体的呼吸全幅、Vogue/Kinfolk 杂志封面大字、半透磨砂腰封/侧栏 |
| **东方美学 / 鲜果手作 / 节气与开业** | `oriental_vertical_frame` / `monument` / `window` / `diptych_focus` | 满幅竖排宋体大字+朱砂方章、建筑双线拱窗、双格自动锁定微距质感特写 |
| **商家原图绝对保真（禁裁切）** | 加 `--protect-subject` 自动限定 `editorial_split` / `gallery_inset` / `monument` / `window` | 100% 完整保留原图商品与包装像素 |

### Step 4：运行本地参数化引擎出图并目检交付
直接调用内置独立渲染脚本 `scripts/render_poster.py`（已捆绑思源黑体、思源宋体与 Barlow Condensed 商业数字体，零外部项目依赖）：

```bash
# 1. 生成单张指定版式（如满幅国潮社交贴纸风）
python3 scripts/render_poster.py \
  --photo /path/to/hero.jpg \
  --brand "果小鲜水果铺" \
  --title "一人吃一半，别抢中间那颗" \
  --subtitle "果小鲜水果铺 · 丹东红颜现摘29.9元/盒" \
  --cta "周末两天到店自取" \
  --offer "29.9元/盒" \
  --ratio 3:4 \
  --family social_sticker_zine \
  --output /path/to/out.png

# 2. 一键生成多风格联排对比图（推荐首次提案，支持 fullbleed / colorblock / curated_cn / editorial / all）
python3 scripts/render_poster.py \
  --photo /path/to/hero.jpg \
  --brand "果小鲜水果铺" \
  --title "一人吃一半，别抢中间那颗" \
  --subtitle "果小鲜水果铺 · 丹东红颜现摘29.9元/盒" \
  --cta "周末两天到店自取" \
  --offer "29.9元/盒" \
  --preset curated_cn \
  --sheet /path/to/preview_sheet.jpg \
  --output-dir /path/to/posters/

# 3. 查看全部 24 种版式家族清单
python3 scripts/render_poster.py --list-families
```

#### 交付前 6 项视觉验收清单（必须亲自看成品图）
1. **无文字压主体**：主标题、贴纸与条码是否干净落位在负空间/结构带内，没有挡住商品最诱人的核心区域？
2. **对比度过关**：手机缩略图尺寸下主标题是否一秒读清（引擎强制 `>= 7.0:1`）？
3. **价格零重复**：是否只有一个最醒目的价格锚点，没有在副标题、正文、角标里重复写两遍？
4. **无断字与孤字**：倾斜贴纸、窄栏和按钮里是否存在截断半句话或单字换行？
5. **事实零虚构**：店名、品名、价格、期限与用户给定事实是否逐字一致？
6. **多画幅就绪**：如需同时发小红书（`3:4`）、抖音/快拍（`9:16`）或横屏（`16:9`），直接切换 `--ratio` 分别导出并逐张复核。
