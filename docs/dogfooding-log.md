# dogfooding-log

ccskill-gptimage を ccskill-gptimage 自身で使った記録。プレスリリース素材生成と
実用シナリオ検証(issue #003)を兼ねる。

---

## 1. プレス用 OGP メイン画像(2026-04-23)

### ユーザの依頼(意図のみ、プロンプトは書かない)

> プレスリリース用の OGP が欲しい。トーンは ccskill-nanobanana より差別化したい(あちらは写真リアル split-screen の物語性。こちらはより洗練された editorial 調で「クオリティの高さ」を象徴したい)。

### Claude が SKILL.md / 過去会話文脈から組み立てたプロンプト

```
A premium editorial magazine cover poster, dark-mode aesthetic, refined and
sophisticated. Centered large title with the exact text "ccskill-gptimage" in
elegant modern sans-serif (lowercase, slight italic accent), warm ivory white.
Below it the exact subtitle "Claude Code 用 OpenAI gpt-image-2 スキル" in
smaller refined Japanese serif font, soft gold color #c9a96a. Beneath that the
tagline "AIが計画して描く。日本語も、英語も、思い通りに。" in subtle Japanese
gothic, dim warm gray. Background: deep ink charcoal #0d1015 with very subtle
vertical gradient. A single thin horizontal gold rule above the title. A small
minimalist terminal cursor mark in the upper right corner. Generous negative
space, magazine-quality kerning and leading, no decorative illustrations,
no border. Mood: confident, restrained, premium technical publication.
```

### 出力
- ファイル: `assets/press/20260423_124322.png`(1536×1024 / quality high / png)
- コスト: 約 $0.21
- 結果: ブリーフ通り。タイトル・サブタイトル・タグラインの **日本語混在テキストが完璧に可読**。マガジン品質のレイアウト・カーニングが達成された。右上のターミナルカーソル `>_` も期待通り

### 備考
- 一発で press 用素材として採用可能なクオリティに到達(再生成不要)
- nanobanana の「写真リアル物語型」とは明確に異なる editorial / typographic 路線で差別化成功

---

## 2. ロゴ(透過 PNG、2026-04-23)

### ユーザの依頼

> プレスと LP 用のロゴが欲しい。透過 PNG。OGP と同じトンマナで。

### Claude が組み立てたプロンプト

```
A minimalist vector logo mark for the project ccskill-gptimage. Composition: a
single geometric mark combining a stylized brush stroke and a subtle curly-brace
silhouette { }, arranged so the brush stroke flows through the braces —
symbolizing "code that paints" / agentic image reasoning. Two-tone: deep navy
#0d1f3c primary and warm gold #c9a96a accent. Flat vector style, sharp clean
edges, no gradients, no text in the image, centered with even padding,
suitable for both light and dark backgrounds.
```

### 実行コマンド
```bash
generate_image.py "..." --model gpt-image-1.5 --background transparent \
  --output-format png --quality medium --output assets/press
```

### 出力
- ファイル: `assets/press/20260423_124136.png`(1024×1024 / RGBA / 透過)
- コスト: 約 $0.05
- 結果: コンセプト的中(中括弧 `{ }` を貫くゴールドのブラシストローク = "code that paints")。フラットベクター、二色構成、エッジ鋭利

### 備考
- gpt-image-2 が透過非対応のため `--model gpt-image-1.5 --background transparent` フォールバック経路を使用(issue #014 で実証済みの経路)
- `generate_image.py` のパススルーロジックがそのまま動作

---

## 3. 実用シナリオ検証 — Apple Business スクリーンショットの地図匿名化(2026-04-23)

### 課題

ユーザがブログ記事(Apple Business 端末管理機能)用に取得したスクリーンショット
(`/Users/oishi/Downloads/20260423/capture_2026-04-15T15-04-12.jpg`、2000×1305)
には Apple Business の「紛失モード — 所在地を表示」ダイアログが含まれ、その地図に
**実在の場所**(街路網、河川、国道 309 号、POI「川西米穀店」「焼肉ホルモン多喜万 松原…」)が
写り込んでおり、評価者(ユーザ)の所在地が特定可能。

→ **地図部分だけ架空に差し替え、周辺 UI は完全保持したスクリーンショット風画像が欲しい**。

### Claude のアプローチ選定

3 案を検討:
- 🅰️ `--reference` のみ(全画面再生成、Preserve プロンプトに頼る)
- 🅱️ `--reference + --mask`(マスク作成のひと手間、ただし公式ドキュメント上は edits API は常に全画面再生成)
- 🅲 Pillow で地図領域だけクロップ → 生成 → 元画像にペーストバック(ピクセル単位完全保持)

最初の試行として 🅰️ を選択(SKILL.md の "always max fidelity + Preserve …" 戦略の実証になる、コスト最小)。

### 組み立てたプロンプト

```
Edit only the map area inside the centered popup dialog. Replace the map with
an Apple Maps-style vector map of a fictional anonymous residential
neighborhood — light beige building footprints, thin gray streets in irregular
grid, a small park area in the center where the green location dot sits, a
narrow blue water feature on the left side. Replace the two POI labels with
fictional Japanese names: "架空珈琲店 ことり" with a brown coffee-shop pin icon
in the upper-right area of the map, and "ベーカリー はる" with an orange shop
pin icon in the lower-right. Remove any real road number signs.

Preserve absolutely everything else exactly as in the reference: the entire
surrounding Apple Business device management UI (left sidebar, top nav, right
device pane, list rows), the dialog box with header "所在地を表示", the date
text "これは、2026年4月15日 15:00に確認されたこのデバイスの最後の位置情報です。",
the central green location dot with its translucent circle, the bottom
"閉じる" button, the "マップ リーガル" attribution and Apple Maps logo at the
bottom-left inside the map. Do not change any layout, font, color, or text
outside the map rectangle.
```

### 実行コマンド
```bash
generate_image.py "..." \
  --reference /Users/oishi/Downloads/20260423/capture_2026-04-15T15-04-12.jpg \
  --size 1536x1024 --quality high --output-format png
```

### 出力
- ファイル: `generated_images/20260423_124525.png`(1536×1024 / png)
- コスト: 約 $0.21

### 結果(成功)

**保持された要素**(再描画されているにもかかわらず、ほぼ完全再現):
- 上部ナビ全項目(ホーム / ユーザ / デバイス / アプリとサービス / ブランド / 広告)
- 「FEEDTAILOR INC.」「大石」のヘッダ
- 左サイドバー全項目(在庫 / マネージメント / 組み込まれている管理 / ブループリント / 構成 / 管理対象アプリ / macOS パッケージ)
- 中央のデバイス一覧、デバイスアイコン、`iPhone 7` `iPhone SE (3rd generation)` `iPhone X` の機種名
- **デバイスのシリアル番号「FK1S836XHG7Y」「YC5H62LRF6」「DNPVL8B9JCLD」までほぼ正確に再現**
- ダイアログヘッダ「所在地を表示」
- 日付テキスト「これは、2026年4月15日 15:00に確認されたこのデバイスの最後の位置情報です。」
- 「閉じる」ボタン
- 中央の緑ロケーションドット(translucent な円付き)
- 「 マップ」ロゴ + 「リーガル」表記
- 右ペインの iPad 画像、「(6th Generation)」「iPadOS 26.4.1」、各機能アイコン、「概要 / 詳細 / アプリ / 構成」タブ、「割り当て: Yuichi Oishi」

**差し替えに成功した要素**(個人情報の消去):
- 街路網が架空のものに置換
- 河川・国道番号「309」を削除
- 実在 POI ラベル「川西米穀店」「焼肉ホルモン多喜万 松原…」を完全消去
- 架空 POI ラベル「架空珈琲店 ことり」「ベーカリー はる」が指定位置に出現
- Apple Maps の vector ルックを維持

### 知見

1. **edits API は公式仕様上「マスク有無に関わらず全画面再生成」**(2026-04-23 公式ドキュメント確認、`docs/research-notes-014.md` 参照)。にもかかわらず gpt-image-2 の "always max fidelity" + 強い "Preserve …" プロンプトの組み合わせは、**シリアル番号レベルの細部まで保持** する驚異的な性能を示した
2. ピクセル単位の完全同一が必要な場合(法的証拠、規制対象等)のみハイブリッド(crop → edit → paste)が必要。それ以外の用途(ブログ・ドキュメント・プレス)では `--reference --quality high` 一発で十分実用的
3. 保持要素の **列挙が効く**(具体テキストを引用符で書き並べる)。「Preserve everything else」だけでは弱く、要素名と引用テキストを具体的に並べることで保持精度が上がる
4. 出力解像度は元の解像度ではなく `--size` で指定した解像度になる(2000×1305 → 1536×1024)。ブログ用なら十分だが、Retina ディスプレイ向けに最大解像度が必要な場合はハイブリッド方式が現実解

これらの知見は `SKILL.md` / `SKILL.ja.md` の「Editing only a small region / 局所編集」節と `gptimageguide.md` のマスク節に反映済み(2026-04-23)。

---

## メタ記録

- 検証日: 2026-04-23
- 総コスト: 約 $0.47(OGP $0.21 + ロゴ $0.05 + 地図差し替え $0.21)
- 実施者: oishi@feedtailor.jp + Claude Code
- 関連 issue: #003(本タスク)、#005(プレスリリース原稿、本素材を使用)
