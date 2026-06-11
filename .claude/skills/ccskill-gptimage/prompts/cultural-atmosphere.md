# Cultural Atmosphere — 文化圏特有の雰囲気を出す(日本語看板・街並み)

画像に「その国らしさ」を出すには、**文化圏特有のテキスト要素(看板・標識・店名)** と **街並みの言語的アイコン** をどう扱うかが鍵になる。本ガイドは、issue #015 Phase 4 効果検証で **19_urban_tokyo_rainy_night** を v2 → v3 にリライトして得た実証知見を、汎用パターンとして体系化したもの。

## 使い所

- 街並みシーン(渋谷・新宿の繁華街、アジアの夜市、ヨーロッパの旧市街など)
- 広告 / マーケビジュアルで「ローカル感」を出したいとき(`prompts/ads-and-marketing.md` 併用)
- 店内モックアップ / 商店街 / 路地裏の生活感
- 観光・インバウンド系のコンテンツ

## 核心原則 — 「読めない文字」を強制しない

文化的雰囲気を消してしまう最大の落とし穴は、**否定 Constraints の効かせすぎ**にある。実在ブランドを避けようとして「読めない文字だけ」を強制すると、文化圏のアイコン性まで失われる。

---

## セクション A: 文化圏のテキスト要素を活かす

### A-1. 否定 Constraints の罠(v2 → v3 実証)

19_urban_tokyo_rainy_night のリライトで明確に効果が出た差分:

| | Constraints の書き方 | 結果 |
|---|---|---|
| ❌ v2(弱化) | `no readable specific text on signs (kanji shapes only)` | 「読めない kanji 形状のみ」を強制した結果、店舗看板の日本語感まで失われ、**書き割りのような無国籍な街**になった |
| ✅ v3(改善) | `Japanese characters on signs should be plausible Japanese language (not English alphabet, not gibberish)` + `use generic / fictional shop names, not real brand names` | **渋谷スクランブル交差点が本物のように再現**。自然な日本語看板群が並んだ |

v3 で実際に描かれた看板の例(架空だが日本語として自然):

> `カラオケ 747` / `居酒屋 2F・3F` / `薬方 くすり・化粧品` / `牛繁 焼肉` / `コンタクトのアイシティ`

**実証画像**: [`assets/capability-survey/categories/19_urban_tokyo_rainy_night_v3.png`](../../../../assets/capability-survey/categories/19_urban_tokyo_rainy_night_v3.png)

**教訓**: 「実在を避けたい」気持ちから `no readable text` と書くと文化が死ぬ。**「読める架空の言語」を肯定形で指定する**のが正解。

### A-2. Key details で看板タイプを具体的に列挙する

「日本語の看板がある」だけでなく、**どんな種類の看板か**を列挙すると密度と真正性が上がる:

```
tategaki kanji shop signs in deep crimson, electric cyan and warm gold
karaoke / izakaya signs in stacked Japanese characters
small ramen-shop lanterns glowing on side streets
vertical neon signs stacked along narrow alleys
```

- **縦書き(tategaki)** を明示すると一気に「日本らしさ」が出る
- 色(`deep crimson, electric cyan, warm gold`)まで指定すると夜の繁華街の質感が安定
- 提灯・暖簾・自販機など**生活アイコン**を 1〜2 個混ぜる

---

## セクション B: 「実在ブランド回避」と「文化的真正性」のトレードオフ

- gpt-image-2 は **架空の日本語ブランド名を作るのが得意**。`use generic / fictional shop names` だけでも自然な看板を量産できる
- ただし `龍角散` のような **実在に近い名前が時々混入する**(モデルが知識として持っているため)
- **完全な架空性**が必要なら、追加で次を明示する:
  ```
  Do not use any real brand names that exist in Japan today. All shop names must be invented.
  ```
- ただしこれは **トレードオフ** — 縛りを強めるほど「それらしさ」も少し削れる。プロジェクトの要件で選ぶ:

| 要件 | 推奨 |
|---|---|
| 広告・LP などで真正性優先(多少の実在風混入は許容) | `use generic / fictional shop names` のみ。緩く |
| 法務・権利上、実在ブランドを 1 つも出せない | 上記 + `Do not use any real brand names ... All shop names must be invented.` を追記。出力を目視確認 |

> **重要**: 完全架空性が要件のときは、**生成後に必ず目視チェック**する。プロンプトで縛っても実在名が混じることがあるため、最終的な担保は人間の確認。

---

## gpt-image-2 固有の注意

- 文字数が多い看板群は描画ミスが出やすい。**主役看板 1〜2 枚を字義通り、背景の看板群は「雰囲気」**と割り切る
- 看板の言語的真正性は `quality=high` で明確に上がる(`medium` だと文字が崩れて gibberish 化しやすい)
- 実在ブランド混入リスクは **プロンプトだけでゼロにできない** — 完全架空が要件なら目視確認必須(セクション B)
- 関連原則: 空状態の肯定形宣言は [`photorealism.md`](photorealism.md) の「Empty / null state declaration」、コピー字義描画は [`ads-and-marketing.md`](ads-and-marketing.md) を参照

## 出典

- 実証元: issue #015 Phase 4 効果検証(19_urban_tokyo_rainy_night の v2 → v3 リライト、2026-04-24)
- Cookbook Section 2 "Text in Images" / "Constraints": https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- 取得日: 2026-04-23(Cookbook)/ 2026-04-24(実証)
