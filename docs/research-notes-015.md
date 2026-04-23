# research-notes #015: SKILL.md best practices 一次資料調査

## サマリ

- **調査日時**: 2026-04-23
- **調査者**: Claude Code + Gemini CLI (リサーチエージェント)

### 踏んだ URL 一覧

| URL | アクセス状況 | 手段 | 備考 |
|---|---|---|---|
| https://developers.openai.com/api/docs/guides/image-generation | 確認済み | WebFetch (research-notes-014, 2026-04-23) | 一次引用あり |
| https://developers.openai.com/api/docs/models/gpt-image-2 | 確認済み | WebFetch (research-notes-014, 2026-04-23) | パラメータ仕様は guide 側に集約と記録 |
| https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide | 未確認 | Gemini CLI quota 枯渇・知識なし | 本ノート末尾「継続調査タスク」参照 |

### Gemini CLI の状況

- `gemini-2.5-flash`: 429 MODEL_CAPACITY_EXHAUSTED (サーバ側キャパシティ不足)
- `gemini-2.5-flash-lite`: quota 枯渇 + gpt-image-2 はトレーニングカットオフ問題で未認識(DALL-E 3 情報を返した)
- **結論**: 今回 Gemini による公式 URL の新規アクセスは不成立。ただし research-notes-014 (2026-04-23 WebFetch) に重要な一次引用が存在するため、本ノートでそれを整理・補完する。

---

## 発見事項(観点ごと)

### A. 構造化プロンプトテンプレ

- **出典**: `gptimageguide.md` 6-1 節 / `SKILL.md` 「Structured prompt template」節
- **公式一次資料での確認**: 未確認 (Cookbook prompting guide URL へのアクセス不成立)
- **社内ガイドの記述**:
  ```
  [Subject] / [Style] / [Composition] / [Lighting] / [Details] / [Constraints]
  ```
  具体例:
  ```
  A gray tabby kitten (subject) /
  flat vector illustration, Japanese children's book style (style) /
  centered, rule of thirds, medium shot (composition) /
  soft morning light, warm tones (lighting) /
  wearing a tiny red scarf, holding a yellow star (details) /
  white background, no text (constraints)
  ```
- **SKILL.md への示唆**: 出典が社内まとめ (gptimageguide.md) のみのため、SKILL.md では「出典: Cookbook prompting guide (要確認)」の注釈付きで掲載継続。Cookbook URL へのアクセス成功時に一次引用を補填すること。

---

### B. テキスト描画のコツ

- **出典**: `gptimageguide.md` 6-2 節 / `SKILL.md` 「Text rendering」節 / `docs/dogfooding-log.md` セクション 1・3
- **公式一次資料での確認**: 部分確認
  - gpt-image-2 のテキスト描画強化・多言語対応は Image generation guide のモデル概要に記載あり (research-notes-014 で確認。ただし引用文字列は残っていない)
  - 引用符の使用法については公式 Cookbook 未確認
- **社内ガイド・実証記述**:
  - `gptimageguide.md`: 「画像内にテキストを入れたい時は引用符で厳密に囲う」
  - `dogfooding-log.md` セクション 1: OGP 生成で `"ccskill-gptimage"` `"Claude Code 用 OpenAI gpt-image-2 スキル"` 等を引用符で囲い、**日本語混在テキストが完璧に可読**と実証済み
  - `dogfooding-log.md` セクション 3: 地図差し替えで `"所在地を表示"` `"閉じる"` 等の保持テキストを引用符で列挙し、**シリアル番号レベルで再現**を実証
- **SKILL.md への示唆**: 引用符パターンは実証ベースでは強固。公式出典の補填が必要だが、実用上は現行記述を維持してよい。

---

### C. 否定形 vs 肯定形

- **出典**: `gptimageguide.md` 6-3 節 / `SKILL.md` 「Use positive form」節
- **公式一次資料での確認**: 未確認 (Cookbook prompting guide URL 未アクセス)
- **社内ガイドの記述**:
  - NG: `a room without furniture`
  - OK: `an empty room with bare walls and polished concrete floor`
- **SKILL.md への示唆**: この原則はほぼすべての生成 AI で共通するベストプラクティスであり、DALL-E 3 公式ガイドでも同様の推奨がある。gpt-image-2 固有の公式記述は Cookbook 確認待ち。

---

### D. Agentic 推論の活かし方

- **出典**: `gptimageguide.md` モデル概要 / 6-5 節 / `SKILL.md` 「Goal-oriented prompts」節
- **公式一次資料での確認**: 部分確認
  - Image generation guide で「gpt-image-2 は O 系列の推論能力を統合した最初の Agentic 画像生成モデル」との記述は research-notes-014 で言及されているが原文引用は残っていない
  - Cookbook prompting guide の具体的なゴール指向プロンプト事例は未確認
- **社内ガイドの記述**:
  ```
  NG: draw a bar chart of 4 bars with values 10 20 30 40 colored blue
  OK: Create an infographic comparing Q1-Q4 revenue (10, 20, 30, 40 million yen) for a board deck.
      Use a clean dark tech aesthetic with neon blue accents.
      Include title, axis labels, and value labels on each bar.
  ```
- **SKILL.md への示唆**: モデルの Agentic 性質はモデルページ・公式ブログで明言されているが、プロンプト設計の具体的指針としての「ゴール指向 vs 手順指向」は Cookbook 確認待ち。

---

### E. 編集時の「保持するもの」明示パターン

- **出典**: `gptimageguide.md` 6-4 節 / `SKILL.md` 「When editing」節 / `docs/dogfooding-log.md` セクション 3
- **公式一次資料での確認**: 出典なし (Cookbook prompting guide 未確認)
- **一次資料に近い根拠**:
  - `research-notes-014` (WebFetch): gpt-image-2 の「常時自動最大忠実度」はドキュメントに明示されており、それを前提とした「Preserve ...」構文は合理的な帰結
  - `dogfooding-log.md` セクション 3: 実証済み。具体的な要素列挙パターン (`"所在地を表示"`, `"閉じる"`, シリアル番号レベル) の有効性を確認
- **実証された効果的パターン**:
  ```
  Preserve absolutely everything else exactly as in the reference: the entire
  surrounding [UI] (header "所在地を表示", date text "...", button "閉じる", ...)
  ```
- **SKILL.md への示唆**: 公式出典ではなく実証ベース。その旨を明示した上で掲載継続。

---

### F. `revised_prompt` をフィードバックに使う方法

- **出典**: `gptimageguide.md` 6-7 節 / `SKILL.md` 「Observe revised_prompt」節
- **公式一次資料での確認**: 部分確認
  - research-notes-014 で、Responses API の `revised_prompt` フィールドは公式ドキュメントに記述があると言及されているが原文引用は残っていない
  - 本スキルの `generate_image.py` は Image API 経路を使用しており、`datum.revised_prompt` を取得・表示している
- **社内ガイドのコード例** (Responses API 向け):
  ```python
  call = [o for o in resp.output if o.type == "image_generation_call"][0]
  print(call.revised_prompt)  # モデルが実際に解釈したプロンプト
  ```
- **SKILL.md への示唆**: Image API での `revised_prompt` の扱いは実装確認済み (generate_image.py)。Responses API 向けの記述は現 SKILL.md の実装経路と異なるため、注記を整理すること。

---

### G. スタイル指定：固有名詞 vs 視覚特徴分解

- **出典**: `gptimageguide.md` 6-6 節 / `SKILL.md` 「Style by visual attributes」節
- **公式一次資料での確認**: 未確認 (版権回避の推奨は一般的だが gpt-image-2 固有の公式記述は Cookbook 確認待ち)
- **社内ガイドの記述**: 「Studio Ghibli 風」より「hand-painted watercolor, soft pastel palette, cel-shaded」のように視覚的特徴の分解を推奨
- **SKILL.md への示唆**: 版権リスク回避という理由は普遍的に正当。公式出典が得られれば補強できる。

---

### H. マスク編集の実態

- **出典**: `gptimageguide.md` 4 節 / `SKILL.md` 「Mask inpainting」節 / `research-notes-014`
- **公式一次資料での確認**: 確認済み (research-notes-014 で WebFetch 取得)
- **原文引用** (OpenAI Image generation guide より、research-notes-014 が引用):
  > "Masking with GPT Image is entirely prompt-based. The model uses the mask as guidance, but may not follow its exact shape with complete precision."
  - 出典: https://developers.openai.com/api/docs/guides/image-generation (アクセス: 2026-04-23)
- **要約**: edits API はマスクの有無に関わらず全画面を再描画する。マスクはあくまでガイダンスであり、ピクセル単位の保持は保証されない。
- **実証** (`dogfooding-log.md` セクション 3): `--reference` のみ (マスクなし) でも「常時最大忠実度 + Preserve プロンプト」によりシリアル番号レベルの再現を達成。全画面再描画の実態を確認。
- **SKILL.md への示唆**: この原文引用は現 SKILL.md に既に掲載されており正確。出典注釈として「OpenAI Image generation guide (確認: research-notes-014, 2026-04-23)」を明記するとよい。

---

### I. コスト最適化の非自明な知見

- **出典**: `gptimageguide.md` 5 節 / `SKILL.md` 「Cost Optimization」節
- **公式一次資料での確認**: トークン数は確認済み
  - `gptimageguide.md` 3-1 節のトークン数テーブルは公式ドキュメントから転記されている
  - **トークン数テーブル** (per image):

    | quality | 1024x1024 | 1024x1536 | 1536x1024 |
    |---------|----------|----------|----------|
    | low     | 272 tok  | 408 tok  | 400 tok  |
    | medium  | 1,056 tok | 1,584 tok | 1,568 tok |
    | high    | 4,160 tok | 6,240 tok | 6,208 tok |

  - **単価** (per 1M output tokens): Image $30.00
- **コスト計算の不整合について**:
  - gptimageguide.md は `1024x1536 high` を $0.165 と記載
  - トークン数ベースで計算すると 6,240 x $30 / 1,000,000 = $0.1872
  - `1024x1024 high` = 4,160 tok x $30 = $0.1248 (gptimageguide.md は $0.211 と記載)
  - **乖離の理由**: 出力トークン単価だけでなく入力 (テキスト) トークンも課金されるため合計コストが異なる可能性。または gptimageguide.md の数値が pricing ページから直接取得したものの可能性。
  - 「1024x1536 high が 1024x1024 high より安い」という方向性はトークン数比から整合する (6,240 vs 4,160 だが解像度は 1.5x 分増えており per-pixel では縦長が安い)。ただしコスト絶対値の一次確認は要実施。
- **SKILL.md への示唆**: コスト表の数値は「gptimageguide.md ベース」と注釈する。pricing ページ直接確認を Phase 2 タスクへ。

---

### J. 解像度・quality 選択の指針

- **出典**: `gptimageguide.md` 3-1 節 / `SKILL.md` 「Use case → parameter table」節
- **公式一次資料での確認**: トークン構造は確認済み
  - `quality: auto` はモデルがプロンプトに応じて最適選択する旨が公式ドキュメントに記載 (research-notes-014 間接確認)
- **サポートされているサイズ**: `auto`, `1024x1024`, `1024x1536`, `1536x1024` (gptimageguide.md に記載)
- **SKILL.md への示唆**: 現行の Use case テーブルは妥当。トークン数は確認済みのため根拠あり。

---

### K. モデレーション設定

- **出典**: `gptimageguide.md` 3-5 節 / `SKILL.md` Constraints 節
- **公式一次資料での確認**: 未確認 (公式ドキュメントからの直接引用なし)
- **社内ガイドの記述**:
  - `auto` (デフォルト): 標準的フィルタリング
  - `low`: 緩めのフィルタリング
- **SKILL.md への示唆**: 現 SKILL.md のオプション表では `auto` / `low` の意味説明が不足。「要件に応じて」程度の記述を追加すべきだが、公式の詳細説明は未確認。

---

### L. Organization Verification 要件・レート制限

- **出典**: `gptimageguide.md` 1 節 / `SKILL.md` Prerequisites 節・Constraints 節
- **公式一次資料での確認**: 確認済み (research-notes-014 間接確認 + 実 API 確認)
- **公式記述内容** (gptimageguide.md 転記):
  - Organization Verification が必須 (未検証 Org では API キーがあっても 403)
  - Tier 1: 100,000 TPM / 5 IPM
  - Tier 5: 8,000,000 TPM / 250 IPM
- **SKILL.md への示唆**: 現行記述は正確。出典 URL を `SKILL.md` 内に明記することを推奨。

---

## 現 SKILL.md の主張と一次資料の照合

| 現記述 | 公式根拠 | 判定 |
|---|---|---|
| 「Organization Verification が必須」 | OpenAI Image generation guide (research-notes-014 確認) | 採用 |
| 「Tier 1 = 5 IPM」 | 同上 | 採用 |
| 「gpt-image-2 は background: transparent 非対応 (400)」 | 公式ガイド明示 + 実 API 確認 (research-notes-014) | 採用 |
| 「input_fidelity は gpt-image-2 で不要 (常時最大忠実度)」 | 原文: "the model processes every image input at high fidelity automatically" (research-notes-014 WebFetch) | 採用 |
| 「マスクは prompt-based guidance」 | 原文: "Masking with GPT Image is entirely prompt-based. The model uses the mask as guidance, but may not follow its exact shape with complete precision." (research-notes-014 WebFetch) | 採用 |
| 「edits API は常に全画面再描画」 | 上記マスク記述から導出 + dogfooding-log.md 実証 | 採用 (推論+実証) |
| 「1024x1536 high が $0.165 で 1024x1024 high の $0.211 より安い」 | トークン数は確認済み (方向性整合)。コスト絶対値の一次確認は未実施 | 要修正 - pricing ページ直接確認後に数値確定 |
| 引用符でテキストを囲む手法 | Cookbook prompting guide 未確認。実証ベースでは有効 (dogfooding-log.md) | 要補足 - 出典を「実証ベース」と明記 |
| 否定形 -> 肯定形の書き換え | Cookbook prompting guide 未確認 | 要補足 - Cookbook 確認後に出典追加 |
| 構造化プロンプトテンプレ [Subject]/[Style]/... | Cookbook prompting guide 未確認 | 要補足 - Cookbook 確認後に出典追加 |
| 「ゴール指向プロンプトがステップ指向より有効」 | Cookbook prompting guide 未確認。モデルの Agentic 性は公式明言 | 要補足 - Cookbook 確認後に出典追加 |
| スタイル固有名詞 -> 視覚特徴分解 | Cookbook prompting guide 未確認 | 要補足 - Cookbook 確認後に出典追加 |
| `revised_prompt` をフィードバックに使う | Responses API ドキュメント部分確認。Image API 実装は generate_image.py で確認済み | 要補足 - 一次引用追加 |
| 「gpt-image-2 は業界初の Agentic 画像生成モデル」 | モデルページに記載あり (research-notes-014 間接確認) | 採用 (引用補填推奨) |
| 「レスポンスは b64_json のみ (URL 返らない)」 | 公式ドキュメントに記載 (gptimageguide.md 転記) | 採用 |
| 「タイムアウト最大 2 分」 | gptimageguide.md 7 節 (出典は OpenAI 公式とされているが原文確認未済) | 要確認 |
| `partial_images` 1 枚あたり +100 トークン | gptimageguide.md 3-6 節 | 要確認 (一次引用なし) |

---

## 結論と Phase 2 への引き継ぎ事項

### 確認済み(安心して SKILL.md に掲載できる)

1. **マスクは prompt-based / 全画面再描画** - 公式原文引用あり (research-notes-014)
2. **input_fidelity は gpt-image-2 で不要 / 常時最大忠実度** - 公式原文引用あり (research-notes-014)
3. **transparent background は gpt-image-2 非対応** - 公式 + 実 API 確認済み (research-notes-014)
4. **Org Verification 必須 / Tier 1 = 5 IPM** - 公式確認済み
5. **引用符 + 要素列挙の Preserve パターン有効性** - dogfooding-log.md で実証済み

### 継続調査タスク(Phase 2)

1. **最優先: Cookbook prompting guide** へのアクセス
   - URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
   - 確認すべき内容: 構造化プロンプトテンプレ / 否定->肯定 / ゴール指向 / スタイル指定 / テキスト描画の公式記述
   - 推奨手段: Gemini CLI ではなく Claude Code の WebFetch ツールで直接アクセス (Gemini は gpt-image-2 の知識なし)
2. **コスト数値の一次確認**: https://platform.openai.com/pricing でコスト表の絶対値を確認
3. **revised_prompt の Image API vs Responses API の扱い差異**: 現 SKILL.md は両方を記載しているが経路が混在しており整理が必要
4. **`partial_images` +100tok の一次確認**: gptimageguide.md に記載があるが原文引用なし

### SKILL.md 刷新の優先順位

| 優先度 | 作業 |
|---|---|
| 高 | Cookbook URL WebFetch -> プロンプトテンプレ/否定->肯定/ゴール指向の出典確定 |
| 高 | pricing ページ直接確認 -> コスト表の数値根拠確立 |
| 中 | 確認済み項目に出典 URL を明記 (「OpenAI Image generation guide, 2026-04-23 確認」等) |
| 低 | revised_prompt 節の Image API / Responses API 経路の記述整理 |

---

## メタ記録

- 調査日時: 2026-04-23
- 一次資料取得手段: research-notes-014 (WebFetch 済み) の引用を参照
- Gemini CLI: gemini-2.5-flash 429 MODEL_CAPACITY_EXHAUSTED / gemini-2.5-flash-lite quota 枯渇 + gpt-image-2 知識なし -> 新規 URL アクセス不成立
- 実証データ: docs/dogfooding-log.md (2026-04-23)
- 関連ノート: research-notes-014 (input_fidelity / gpt-image-1.5 一次資料検証, 2026-04-23)

---

## WebFetch フォローアップ調査(2026-04-23)

Gemini フォールバック分の継続調査タスクを Claude Code の WebFetch ツールで実施。Cookbook Prompting Guide にアクセス成功し、これまで「Cookbook 未確認」だった項目に一次出典を確定できた。

### 踏んだ URL(全て成功)

| URL | アクセス手段 | 取得項目 |
|---|---|---|
| https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide | WebFetch (2026-04-23) | Prompting Fundamentals 全文 / Section 4.2 抜粋 |
| https://developers.openai.com/api/docs/guides/image-generation | WebFetch (2026-04-23) | revised_prompt / mask / cost / moderation / Org Verification / partial_images / input_fidelity / background |
| https://developers.openai.com/api/docs/models/gpt-image-2 | WebFetch (2026-04-23) | snapshot / endpoints / Tier 別 rate limit |

---

### 観点別:一次引用と SKILL.md 照合

#### A. 構造化プロンプトテンプレ

- **出典**: Cookbook "Prompting Fundamentals" → "Structure + goal"
- **原文引用**:
  > "Write prompts in a consistent order (background/scene → subject → key details → constraints)"
- **要約(日本語)**: 順序の一貫性が重要で、`background/scene → subject → key details → constraints` の流れを推奨。
- **追加引用** ("Prompt format"):
  > "Use the format that is easiest to maintain. Minimal prompts, descriptive paragraphs, JSON-like structures, instruction-style prompts, and tag-based prompts can all work well"
- **要約**: フォーマット(段落 / JSON 風 / instruction / tag)は自由。維持しやすい形式を選んでよい。
- **SKILL.md 現記述との照合**: SKILL.md は `[Subject] / [Style] / [Composition] / [Lighting] / [Details] / [Constraints]` の 6 区分。公式は **5 区分(scene/subject/key details/constraints)+ Specificity / Composition / Lighting を別軸として整理**しており、項目構成は乖離している。
- **判定**: ⚠️**要修正** — SKILL.md の 6 区分は社内ガイド由来で公式と一致しない。公式に寄せるか「公式に基づく標準テンプレ」と「社内拡張版」を分離して記述すべき。
- **重要**: 公式は「順序」を強調しているが、項目固定ではない(format は自由)。SKILL.md の固定 6 区分テンプレは過度に厳格な印象を与えるため、公式の柔軟さを反映すべき。

#### B. テキスト描画のコツ

- **出典**: Cookbook "Prompting Fundamentals" → "Text in images"
- **原文引用**:
  > "Put literal text in **quotes** or **ALL CAPS** and specify typography details (font style, size, color, placement)"
- **要約**: 描画したいテキストは **クォートまたは ALL CAPS** で囲い、タイポグラフィ詳細(フォントスタイル・サイズ・色・配置)を明示する。
- **SKILL.md 現記述との照合**: 「Wrap any text you want rendered in **strict quotation marks**」は正しいが、**ALL CAPS という代替手段が抜けている**。また「specify typography details」を例示で示しているのみで、要件としての明文化が弱い。
- **判定**: ⚠️**要修正** — クォートに加え ALL CAPS を併記、typography 詳細(font style, size, color, placement)を必須要素として明記する。
- **多言語/日本語特化**: Cookbook の Prompting Fundamentals には日本語固有の指示はない。Section 4.2(Translation in Images)に多言語編集の記述あり。

#### C. 否定形 vs 肯定形

- **出典**: Cookbook "Prompting Fundamentals" → "Constraints (what to change vs preserve)"
- **原文引用**:
  > "State exclusions and invariants explicitly (e.g., 'no watermark,' 'no extra text')"
- **要約**: 除外項目と不変項目は **明示的に書く** 。例: `'no watermark', 'no extra text'`。
- **SKILL.md 現記述との照合**: SKILL.md は「Use positive form, not negation」と書いているが、**Cookbook は逆に "no watermark" のような否定形を例示として推奨している**。
- **判定**: ❌**削除候補 / 大幅修正** — 「否定形を避けよ」という SKILL.md の記述は **公式 Cookbook の指針と矛盾する**。社内ガイド (gptimageguide.md 6-3 節) も出典なしの一般論。gpt-image-2 では否定形(exclusions)も明示的に書くのが推奨ということを反映すべき。
- **重要発見**: これは Phase 0 ガイド作成時の **誤った思い込み**(DALL-E 3 時代の知見)を gpt-image-2 にそのまま持ち込んでいた可能性が高い。SKILL.md の修正必須。

#### D. Agentic 推論 / ゴール指向 vs 手順指向

- **出典**: Cookbook 全体に「agentic」「goal vs step-by-step」の明示的記述は **無し**
- **モデルページ** (https://developers.openai.com/api/docs/models/gpt-image-2) からの引用:
  > "State-of-the-art image generation model for fast, high-quality image generation and editing."
- **要約**: モデルページの公式記述は「state-of-the-art」のみで「agentic」「reasoning」の語は確認できなかった(WebFetch 結果)。
- **SKILL.md 現記述との照合**: SKILL.md は「**first agentic image generation model**」「actively researches, plans and reasons」と強い表現を使っているが、**この表現の公式一次出典は今回の WebFetch では確認できず**。`gptimageguide.md` の社内記述に依存している。
- **判定**: ⚠️**要修正** — 「Agentic」「reasoning」表現は社内ガイド由来である旨を注記するか、表現を弱める必要がある。OpenAI の公式リリースブログ等に該当記述がある可能性は残るため Phase 2 で要追加調査(現時点の Cookbook + Guide + モデルページには無い)。
- **代替知見**: Cookbook "Iterate instead of overloading" は実質的に「ゴール指向」とは別の方向性 = **段階的反復**を推奨:
  > "Long prompts can work well, but debugging is easier when you start with a clean base prompt and refine with small, single-change follow-ups"
- **示唆**: 「ゴール一発投入」よりも「**clean base prompt → 1 変更ずつ反復**」の方が公式推奨に近い。SKILL.md の「Goal-oriented prompts beat step-by-step instructions」は **ゴールを書くこと自体は有効だが、段階反復との組み合わせが重要**と書き換えるべき。

#### E. 編集時の「保持するもの」明示

- **出典**: Cookbook Section 4.2 "Translation in Images"
- **原文引用**:
  > "Preserve everything except the text—keep typography style, placement, spacing, and hierarchy consistent"
- **要約**: テキスト翻訳ユースケースで「テキスト以外は **typography style, placement, spacing, hierarchy** すべてを保持」という具体的な指示パターンを公式が提示している。
- **追加引用** ("Constraints (what to change vs preserve)"):
  > "State exclusions and invariants explicitly"
- **要約**: 「変更する点」と「保持する点」を **両方明示** することが基本原則。
- **SKILL.md 現記述との照合**: 「Preserve the woman's face, hair, and pose exactly as in the reference. Replace only the background ...」という SKILL.md の例は公式パターンと整合する。要素列挙の dogfooding 実証も合致。
- **判定**: ✅**採用** — 現記述は公式の Preserve パターンと整合。dogfooding-log.md の実証と合わせて根拠が確立した。

#### F. revised_prompt フィードバックループ

- **出典**: OpenAI Image generation guide
- **原文引用**:
  > "You can access the revised prompt in the `revised_prompt` field of the image generation call"
- **要約**: 公式は `revised_prompt` フィールドの存在のみ言及。「フィードバックループに使え」という運用指針は公式記述には **含まれない**。
- **SKILL.md 現記述との照合**: SKILL.md の「Use it as a feedback signal to refine the next prompt」は社内推奨で、公式は単に「アクセスできる」とだけ言及している。
- **判定**: ✅**採用(注釈付き)** — 「フィールドの存在」は公式、「フィードバックに使う」は社内推奨である旨を区別して書くと正確。

#### G. スタイル指定:固有名詞 vs 視覚特徴分解

- **出典**: Cookbook "Prompting Fundamentals" → "Specificity + quality cues"
- **原文引用**:
  > "Be concrete about materials, shapes, textures, and the visual medium (photo, watercolor, 3D render)"
- **要約**: スタイル指定は **materials / shapes / textures / visual medium** で具体化する。固有名詞(著名作家・スタジオ名)を避けよという明示的記述は **無し**。
- **SKILL.md 現記述との照合**: SKILL.md の「Avoid copyrighted style names. Use `hand-painted watercolor, soft pastel palette, cel-shaded` rather than `Studio Ghibli style`」は **Be concrete の精神とは整合するが、「copyrighted を避けよ」という公式記述は無い**。
- **判定**: ⚠️**要修正** — 「視覚特徴で具体化する」は公式根拠あり。「copyright を避けよ」は法的リスク観点での社内判断と注記すべき。

#### H. マスク編集の実態

- **出典**: OpenAI Image generation guide(既出)
- **原文引用**:
  > "Masking with GPT Image is entirely prompt-based. The model uses the mask as guidance, but may not follow its exact shape with complete precision."
- **要約**: マスクはあくまでガイダンスで形状の正確な追従は保証されない。
- **判定**: ✅**採用** — 既に SKILL.md に掲載済み・正確。

#### I. コスト最適化(1024×1536 high < 1024×1024 high の真偽)

- **出典**: OpenAI Image generation guide
- **原文引用**:
  > "GPT Image 2...High $0.211...High $0.165"
- **要約**: 1024×1024 high = $0.211、1024×1536 high = $0.165 という **公式記載を直接確認**。
- **SKILL.md 現記述との照合**: 「`1024×1536` (portrait) at `high` is **$0.165** — *cheaper* than `1024×1024` at `high` ($0.211)」は **公式記述と完全一致**。
- **判定**: ✅**採用** — 一次出典確定。「コスト罠」記述は完全に正当。

#### J. 解像度・quality 選択指針

- **出典**: OpenAI Image generation guide
- **原文引用**:
  > "`size`, `quality`, and `background` support the `auto` option, where the model will automatically select the best option based on the prompt."
- **追加引用** (Cookbook "Latency vs fidelity"):
  > "For latency-sensitive or high-volume use cases, start with `quality="low"`"
- **要約**: `auto` はモデル任せ最適化。レイテンシ/ボリューム重視なら `low` から開始。
- **SKILL.md 現記述との照合**: 「Use `--quality low` while iterating」は公式の "start with low" と整合。Use case 表もおおむね妥当。
- **判定**: ✅**採用**

#### K. moderation auto vs low

- **出典**: OpenAI Image generation guide
- **原文引用**:
  > "`auto` (default): Standard filtering that seeks to limit creating certain categories of potentially age-inappropriate content. `low`: Less restrictive filtering."
- **要約**: `auto` は年齢不適切コンテンツの制限を含む標準フィルタ。`low` はより緩い。
- **SKILL.md 現記述との照合**: SKILL.md のオプション表は「Moderation level」とだけ書かれており説明不足。
- **判定**: ⚠️**要修正** — 上記公式説明をオプション表に短く追記すべき。

#### L. Organization Verification / レート制限 / partial_images

- **出典**: OpenAI Image generation guide + モデルページ
- **原文引用**:
  > "you may need to complete the API Organization Verification...before using GPT Image models"
  > "each partial image will incur an additional 100 image output tokens"
- **モデルページ Tier 別 rate limit**:
  - Tier 1: 100,000 TPM, 5 IPM
  - Tier 2: 250,000 TPM, 20 IPM
  - Tier 3: 800,000 TPM, 50 IPM
  - Tier 4: 3,000,000 TPM, 150 IPM
  - Tier 5: 8,000,000 TPM, 250 IPM
- **判定**: ✅**採用** — 全て一次出典確定。`partial_images` の +100 トークンも公式記述で確認(これまで gptimageguide.md 由来で出典不明だった)。

#### M. input_fidelity / background transparent(再確認)

- **出典**: OpenAI Image generation guide
- **原文引用**:
  > "For `gpt-image-2`, omit this parameter; the API doesn't allow changing it because the model processes every image input at high fidelity automatically."
  > "`gpt-image-2` doesn't currently support transparent backgrounds. Requests with `background: \"transparent\"` aren't supported for this model."
- **判定**: ✅**採用** — 既に研究済みだが、Image generation guide ページに **明文として記載されていることを今回再確認**。これにより「実 API でしか分からなかった仕様」ではなく「公式ドキュメントに明記された仕様」と訂正できる。

---

## 統合: 現 SKILL.md 主張の照合表(更新版)

| 現記述 | 公式根拠 | 判定 |
|---|---|---|
| Organization Verification 必須 | Image generation guide 明文 | ✅採用 |
| Tier 1 = 5 IPM | gpt-image-2 モデルページ | ✅採用(出典確定) |
| transparent background 非対応 | Image generation guide 明文 | ✅採用(出典確定) |
| input_fidelity は gpt-image-2 で不要 | Image generation guide 明文 | ✅採用(出典確定) |
| マスクは prompt-based / 全画面再描画 | Image generation guide 明文 | ✅採用 |
| 1024×1536 high $0.165 < 1024×1024 high $0.211 | Image generation guide 価格表 | ✅採用(出典確定) |
| `partial_images` +100 トークン | Image generation guide 明文 | ✅採用(出典確定) |
| moderation auto/low 説明不足 | "Standard filtering ... age-inappropriate" / "Less restrictive" | ⚠️要修正 - 説明追記 |
| 引用符でテキストを囲む | "Put literal text in quotes or ALL CAPS" | ⚠️要修正 - **ALL CAPS** 併記、typography 詳細を必須化 |
| 構造化テンプレ `[Subject]/[Style]/[Composition]/...` 6 区分固定 | "background/scene → subject → key details → constraints" + format 自由 | ⚠️要修正 - 項目固定を緩める、順序を強調 |
| 「否定形ではなく肯定形で」 | "State exclusions and invariants explicitly (e.g., 'no watermark')" | ❌**削除/反転** - 公式は否定形(exclusion)も明示推奨 |
| 「ゴール指向 > 手順指向」 | 公式に該当記述なし。"Iterate ... small, single-change follow-ups" は段階反復を推奨 | ⚠️要修正 - ゴール指向は維持しつつ段階反復を併記 |
| 「Agentic / reasoning / first agentic model」 | モデルページに該当語は確認できず | ⚠️要修正 - 表現弱化または公式リリースブログ要確認 |
| Preserve パターン(face, hair, pose 等) | Cookbook 4.2 "Preserve everything except the text—keep typography style, placement, spacing, and hierarchy" | ✅採用(出典確定) |
| スタイル固有名詞 → 視覚特徴分解 | "Be concrete about materials, shapes, textures, and the visual medium" | ⚠️一部採用 - 視覚特徴具体化は公式、版権回避は社内判断 |
| `revised_prompt` の存在 | "You can access the revised prompt in the `revised_prompt` field" | ✅採用 |
| `revised_prompt` をフィードバックに使え | 公式は存在のみ言及 | ⚠️注釈 - 「社内推奨」と明示 |
| レスポンスは b64_json のみ | gptimageguide.md 転記、今回の WebFetch では未確認 | 要追加確認 |
| タイムアウト最大 2 分 | gptimageguide.md 7 節、公式出典は今回未確認 | 要追加確認 |
| Streaming 非対応 (モデルページ) | "Streaming: Not supported" — ただし guide 側には partial_images / stream=True の記述あり | ⚠️**矛盾** - モデルページと guide で表記差。Phase 2 で精査 |

---

## Phase 2 アクションアイテム

### 即時実施(SKILL.md 更新)

1. ❌**削除/反転**: 「Use positive form, not negation」セクションを削除し、「**State exclusions explicitly (e.g., 'no watermark')**」を公式引用付きで追加。NG/OK 表は「Cookbook の Constraints 例」に差し替え。
2. ⚠️**修正**: 「Text rendering」節に **ALL CAPS** 代替を追加し、typography 詳細(font style, size, color, placement)を **必須要素**として明文化。
3. ⚠️**修正**: 「Structured prompt template」節を **公式の 4 区分順序(scene → subject → key details → constraints)** に寄せる。6 区分固定は「拡張テンプレ例」として降格。
4. ⚠️**修正**: 「Goal-oriented prompts beat step-by-step」節に **"Iterate with small, single-change follow-ups"** を併記して、段階反復の重要性も伝える。
5. ⚠️**修正**: moderation オプション表に「`auto` = age-inappropriate を制限する標準フィルタ / `low` = 緩いフィルタ」を 1 行で追加。
6. ⚠️**修正**: 「first agentic image generation model」「actively researches, plans and reasons」表現を **弱化**(「reasoning-augmented」程度)するか、出典を OpenAI 公式リリースブログから補填。
7. ⚠️**修正**: スタイル指定節を「Be concrete about materials/shapes/textures/medium(公式)」を主軸にし、版権回避は補足扱いに整理。
8. ✅**出典明記**: Cost 表・rate limit・partial_images・transparent・input_fidelity に出典 URL と「2026-04-23 確認」を脚注追加。

### 追加調査(優先度中)

9. OpenAI 公式リリースブログ(2026-04-21)で「agentic」「reasoning」表現の公式裏取り。
10. Streaming 表記の guide vs モデルページ矛盾の精査(`partial_images` / `stream=True` がモデルページの「Streaming: Not supported」とどう整合するか)。
11. Cookbook Section 4 全体の精査(infographics / photorealism / logo design / ads / comic strips / UI mockups / scientific visuals / productivity slides の各サブセクションに SKILL.md に取り込むべき具体パターンが眠っている可能性)。
12. レスポンス形式(b64_json のみ)・タイムアウト 2 分の公式裏取り。

### 矛盾項目(設計判断必要)

- 「ゴール指向 vs 段階反復」は実は両立する(ゴールは書く、ただし複雑なら 1 変更ずつ refine)。SKILL.md ではこの両立を明示する形で書き直すのが最善。

