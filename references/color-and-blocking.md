# 商业色彩搭配、色块组合与图形原语规范

本规范综合了 **Pinterest 商业广告实战样本** 与 **27 张中文商业私藏视觉标杆库** 的系统拆解，是 `scripts/poster_engine.py` 配色与图形原语的底层设计依据。

---

## 一、5 大商业色彩搭配公式（65% 主色域 : 25% 主体/辅块 : 10% 尖锐跳色）

1. **高饱和彩底 + 极简高反差大字**
   - `mustard_pop`：明芥末黄 `#E8BC1C` + 深碳黑 `#12100E` + 莓红 `#C02622` + 奶油白 `#F7F2E6`（水果、小吃、炸物、烘焙）
   - `loft_tangerine`：亮橘 `#EE8426` + 纯黑 `#0E0F10` + 奶油格 `#FAF5EA`（零售选品、潮玩、快闪）
   - `cobalt_citrus`：电光钴蓝 `#0F4AA0` + 纯白 `#FFFDF7` + 鲜橙 `#EE7A22`（冰饮、果茶、夏日清新）
2. **暖燕麦/骨白纸底 + 深饱和食欲色字**
   - `pistils_botanical`：骨白 `#F3EFE3` + 森林绿 `#1C3E22` + 赤陶 `#BA482A`（鲜花、生鲜、有机食材、生活方式）
   - `oxblood_cream`：暖燕麦 `#EDE6DA` + 深牛血红 `#6C1418` + 焦糖驼 `#CEA27A`（精品咖啡、烘培、红酒、草莓樱桃）
3. **东方祖母绿 / 暖宣纸 + 朱砂点睛**
   - `emerald_oriental`：深祖母绿 `#0C5244` + 玉白 `#F9F5EA` + 朱砂红 `#CE3026`（中式餐饮、茶饮、节气礼盒）
   - `rice_paper`：暖宣纸 `#F5F1E6` + 墨黑 `#181A18` + 朱砂方章 `#C42C22`（东方竖排海报）
4. **满幅摄影 + 智能主色锁定（Photo-Harmonic Accent）**
   - 不对整张图做简单平均（否则红草莓会被竹篮中和成土棕色），而是取照片高饱和度前 20% 区域（Top-Quartile Saturation）的中位数作为强调色，自动锁住商品最鲜活的本色（如红颜酒红、抹茶翠绿、焦糖琥珀）。
5. **潮流荧光高光系统（Neon Highlighter）**
   - 白底/暗黑满幅图 + 12px 荧光绿 `#36E822` / 酸柠黄 `#D6FA18` / 电光朱红 `#F44226` 外框与高亮色块，色块内严格配纯黑 `#0A0C0E` 保证 >12:1 极高可读性。

---

## 二、6 大商业图形转化原语

| 原语 | 实现函数 | 使用时机 |
|---|---|---|
| **20 齿锯齿波浪价格贴纸** | `_draw_starburst_sticker` | `color_block_diagonal` 及强促销爆款价，替代呆板圆角小框 |
| **双段式优惠券胶囊** | `_draw_split_coupon` | `color_block_chromatic`（左权益词 \| 右粗数字价，如 `周末特惠 \| 29.9元/盒`） |
| **±5° 倾斜高亮贴纸** | `_draw_tilted_sticker` | `social_sticker_zine`（主标题四角点缀社交短句与价格，严禁截断半句话） |
| **四角取景框括号** | `_draw_viewfinder_brackets` | `social_sticker_zine`（锁住视觉中心与社交金句） |
| **真实矢量条形码 & 2 行棋盘格** | `_draw_barcode` / `_draw_checkerboard` | `social_sticker_zine` / `neon_highlighter_poster`（拉满潮流与设计展质感） |
| **东方朱砂方章 & 竖排宋体** | `_draw_vertical_cjk` | `oriental_vertical_frame`（自上而下、从右至左两列排布，精准停在商品主体上方） |

---

## 三、WCAG 对比度与防脏画面铁律

- **标题对比度**：所有色块、纸底、光学渐变遮罩必须经 `_enforce_contrast()` 校验，确保 `titleContrast >= 7.0:1`，`bodyContrast >= 4.5:1`。
- **满幅防遮挡**：满幅摄影一律通过 `_quiet_vertical_anchor()` 计算图像上下梯度能量 + 饱和度，自动锁定低熵负空间排字；底部或顶部只做 Smoothstep 丝滑渐隐，严禁在主体上盖不透明黑块或高斯模糊拉边。
- **价格零冗余**：独立价格徽章/贴纸/价格格启用时，自动从副标题中剥离同一价格字串，整张图价格仅出现一次。
