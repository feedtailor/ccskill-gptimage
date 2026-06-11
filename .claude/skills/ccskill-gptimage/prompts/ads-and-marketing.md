# Ads & Marketing(画像内テキスト含む)

Cookbook 4.6(Ads Generation)+ 5.5(Marketing Creatives with Real Text In-Image)を統合。**ブランド + オーディエンス + コピーを明示的にプロンプトに含める**のが共通原則。

## 使い所

- 広告クリエイティブ(Instagram、雑誌、交通広告)
- ビルボード / サイネージのモックアップ
- 製品画像にキャンペーンコピーを載せた SNS 素材
- キャンペーン予告ビジュアル

## Cookbook 原則

### 4.6 — ブリーフ形式で書く

> Ads は技術仕様ではなく**クリエイティブブリーフ**として書く。ブランド、オーディエンス、概念、構成、正確なコピーを記述し、モデルに創造的な判断を委ねる。

### 5.5 — テキストを字義通り描かせる

> "When baking marketing copy into an image, lock typography with explicit constraints: quote the exact copy, demand verbatim rendering with no extra characters, and describe placement and font style."

**書き方のコツ**:
- `Billboard text (EXACT, verbatim, no extra characters):` のように**最強の縛り**を入れる
- タイポグラフィを必ず指定: `bold sans-serif, high contrast, centered, clean kerning`
- `Ensure text appears once and is perfectly legible.` を添えて重複描画を防ぐ
- `No watermarks, no logos.` で余計なマークを排除

---

## プロンプト例 1: ブランドキャンペーン画像(Cookbook 4.6)

```
Give me a cool in culture ad / fashion shot for a brand called Thread.
It's a hip young street brand. The ad shows a group of friends hanging out together with the tagline "Yours to Create."
Make it feel like a polished campaign image for a youth streetwear audience: stylish, contemporary, energetic, and tasteful.
Use clean composition, strong color direction, natural poses, and premium fashion photography cues.
Render the tagline exactly once, clearly and legibly, integrated into the ad layout.
No extra text, no watermarks, no unrelated logos.
```

**パラメータ**: `size=1024x1536`, `quality=medium`

**CLI 例**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Give me a cool in culture ad / fashion shot for a brand called Thread. ..." \
  --size 1024x1536 --quality high \
  --output-name thread_campaign_01
```

---

## プロンプト例 2: 既存商品画像にコピーを載せたビルボード(Cookbook 5.5 / edit 経路)

```
Create a realistic billboard mockup of the shampoo on a highway scene during sunset.
Billboard text (EXACT, verbatim, no extra characters):
"Fresh and clean"
Typography: bold sans-serif, high contrast, centered, clean kerning.
Ensure text appears once and is perfectly legible.
No watermarks, no logos.
```

**パラメータ**: `size=1024x1536`, `quality=medium`, 入力画像 1 枚(シャンプーボトル)

**CLI 例**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Create a realistic billboard mockup of the shampoo on a highway scene during sunset. Billboard text (EXACT, verbatim, no extra characters): \"Fresh and clean\" Typography: bold sans-serif, high contrast, centered, clean kerning. Ensure text appears once and is perfectly legible. No watermarks, no logos." \
  --reference ./product_bottle.png --quality high
```

---

## 日本語コピー入りの広告(gpt-image-2 の強み活用)

gpt-image-2 は日本語テキストの描画精度が高いので、以下のような日本語コピー広告も 1 発で作れる。

```
Create a subway poster mockup for a Japanese matcha drink brand launching spring 2026.
Ad copy (EXACT, verbatim, in Japanese):
"一杯で、春。"
and subtitle:
"新緑シーズン限定ブレンド"
Typography: large bold Japanese serif (like Mincho) for the main copy, medium-weight Japanese sans-serif (like Gothic) for the subtitle.
Green-and-white palette, minimal layout, a single matcha drink centered.
No watermarks, no extra text, no logos.
```

**ポイント**:
- 日本語フォント指定を明示(`Mincho` / `Gothic`)
- 引用符 `"一杯で、春。"` で字義通りに囲む
- 句読点も含めて囲む(句点 `。` まで正確に再現させる)

> **関連**: 街並み・店内・ローカル感のあるビジュアルで**日本語看板や文化圏アイコン**を使う場合は [`cultural-atmosphere.md`](cultural-atmosphere.md) も参照。「読めない文字だけ」を強制して文化を消してしまう落とし穴と、その回避パターンを扱う。

---

## gpt-image-2 固有の注意

- **テキストの複数回描画バグ**を避けるため、`Ensure text appears once` は必ず入れる
- 長いコピーは描画ミスが出やすい。**10〜15 文字程度のキャッチコピーまで**が実用域
- edit 経路で商品画像を持ち込む場合、**商品の形状・ロゴは自動で保持**される(`input_fidelity` 不要)
- コスト優先なら試行は `quality=low`、納品は `quality=high`(`medium` は中途半端でテキストがぼやける)

## 出典

- Cookbook 4.6 Ads Generation / 5.5 Marketing Creatives with Real Text In-Image
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- 取得日: 2026-04-23
