# ccskill-gptimage Gallery

OpenAI gpt-image-2 で **何が作れるか** を実物で示す作例ギャラリー。
Phase 4 効果検証(2026-04-24)で生成した **SKILL 公式一次資料ベース刷新後の v2 / 35 枚** を掲載。**35/35 すべて一発成功(再生成ゼロ)** / 合計 ¥905 ($6.04)。

19(渋谷夜景) のみは v2 で日本語感が弱まったため一度だけリライトした v3 を採用。Phase 4 全 35 枚の v1/v2 比較評価は [`docs/skill-effect-comparison.md`](skill-effect-comparison.md) 参照。

すべての画像にメタデータ JSON サイドカー(`{name}.png.json`)が付属しており、プロンプト・revised_prompt・パラメータが完全再現可能です。

---

## Part 1 — Capability Survey(26 カテゴリ × `quality: high`)

「何ができるか」の守備範囲提示。各カテゴリは構造化プロンプトで 1 発生成。

### 01. 写実ポートレート(人物)

`1024×1024 / high` — 自然光、編集系雑誌品質、被写界深度、`50mm lens look`

<img src="../assets/capability-survey/categories/v2/01_photorealistic_portrait_woman.png" width="500" alt="photorealistic portrait">

---

### 02. アニメキャラ(セルシェード)

`1024×1024 / high` — クリーンな線画、和装鎧、桜の散り

<img src="../assets/capability-survey/categories/v2/02_anime_warrior_character.png" width="500" alt="anime warrior">

---

### 03. 水彩風景

`1536×1024 / high` — 湿式技法のにじみ、東洋的構図、紙質テクスチャ

<img src="../assets/capability-survey/categories/v2/03_watercolor_mountain_landscape.png" width="700" alt="watercolor landscape">

---

### 04. アイソメトリック 3D 室内

`1024×1024 / high` — 配置・小物・配色すべてプロンプト通り

<img src="../assets/capability-survey/categories/v2/04_isometric_3d_reading_room.png" width="500" alt="isometric reading room">

---

### 05. UI モックアップ(英語ログイン)

`1024×1536 / high` — pixel-perfect、入力フィールド・ボタン・リンクすべて指定通り、タイポ階層(32pt/14pt/16pt)も忠実

<img src="../assets/capability-survey/categories/v2/05_ui_mockup_login_english.png" width="400" alt="login UI mockup">

---

### 06. UI モックアップ(日本語 iOS 設定) ⚡

`1024×1536 / high` — 「設定」「機内モード」「Wi-Fi」「FEEDTAILOR-5G」「サウンドと触覚」全完璧。SF Symbol 風のカラフルアイコンも指定通り。**iPhone 端末フレーム込みで実機モックアップとして使えるレベル**

<img src="../assets/capability-survey/categories/v2/06_ui_mockup_settings_japanese.png" width="400" alt="iOS settings UI in Japanese">

---

### 07. インフォグラフィック(棒グラフ)

`1024×1536 / high` — 数値 12/18/27/35 完全保持、軸ラベル・"+192% YoY" コラル色も verbatim 再現。Cookbook 4.10 ピッチデッキパターン適用で板書品質

<img src="../assets/capability-survey/categories/v2/07_infographic_quarterly_revenue.png" width="400" alt="infographic">

---

### 08. システム構成図(マイクロサービス)

`1024×1024 / high` — API Gateway → 3 services → 3 DBs(`auth_db`/`orders_db`/`payments_db`)、Kafka、点線矢印すべて指定通り

<img src="../assets/capability-survey/categories/v2/08_flowchart_microservices_architecture.png" width="500" alt="microservices architecture">

---

### 09. フード写真(豚骨ラーメン)

`1024×1024 / high` — 湯気、白濁スープ、煮玉子の黄身、紅生姜まで生々しい質感

<img src="../assets/capability-survey/categories/v2/09_food_photo_tonkotsu_ramen.png" width="500" alt="tonkotsu ramen">

---

### 10. 建築外観レンダ

`1536×1024 / high` — コンクリート × 木の現代住宅、リフレクションプール、ゴールデンアワー

<img src="../assets/capability-survey/categories/v2/10_architectural_render_modern_house.png" width="700" alt="modern architecture render">

---

### 11. 手描きペンスケッチ

`1024×1024 / high` — 提灯付き居酒屋、自販機、配線、自転車、アーバンスケッチャー風水彩ウォッシュ。路地の奥行きとパース感が秀逸

<img src="../assets/capability-survey/categories/v2/11_hand_drawn_pen_sketch_tokyo_alley.png" width="500" alt="urban sketch tokyo alley">

---

### 12. 4 コマ漫画(日本語) ⚡⚡

`1024×1536 / high` — **タイトル「プログラマあるある」+ 4 つの吹き出しすべて読める日本語!**「なぜか動いた…!」「なぜ動くんだろう?」「ちょっと整理しよう」「なぜ動かない…!?」が完璧再現。**眼鏡 + グレーフーディーのキャラが全 4 コマで同一**(Cookbook 6.4 キャラ一貫性パターン)

<img src="../assets/capability-survey/categories/v2/12_comic_4koma_japanese_programmer.png" width="400" alt="Japanese 4-koma manga">

---

### 13. ロゴ(VECTRA、抽象マーク)

`1024×1024 / high` — 1 本の連続線で矢印→円のループ、アンバードット、"VECTRA" 字間美しい

<img src="../assets/capability-survey/categories/v2/13_logo_abstract_mark_vectra.png" width="500" alt="VECTRA logo">

---

### 14. 日本語縦書きポスター(縦組) ⚡⚡

`1024×1536 / high` — **「未来は描かれるものではない、計画されるものだ。」が縦書き(tategaki)で完璧!** 句読点も縦中横で正しく配置。英語サブと金線も指定通り。これは gpt-image-1 系では不可能だった領域

<img src="../assets/capability-survey/categories/v2/14_japanese_poster_vertical_tategaki.png" width="400" alt="Japanese vertical poster">

---

### 15. 抽象アート

`1024×1024 / high` — 流動するコーラル/ピーチ/ラベンダー/金のリボン、液体水銀風、ギャラリー品質

<img src="../assets/capability-survey/categories/v2/15_abstract_generative_ribbons.png" width="500" alt="abstract generative art">

---

### 16. 日常スナップ(モーニングキッチン)

`1024×1024 / high` — ドリップコーヒーを淹れる手元、桃・ノート・銅鍋、35mm フィルム調

<img src="../assets/capability-survey/categories/v2/16_daily_morning_kitchen.png" width="500" alt="morning kitchen snapshot">

---

### 17. 自然風景(霧の原生林)

`1536×1024 / high` — 巨大な杉、God-rays、シダ・苔、ナショジオクラス

<img src="../assets/capability-survey/categories/v2/17_nature_misty_cedar_forest.png" width="700" alt="misty cedar forest">

---

### 18. 自然風景(海岸の夜明け)

`1536×1024 / high` — 火山岩海岸、シルクの波(長時間露光)、孤独の糸杉、パステルの空

<img src="../assets/capability-survey/categories/v2/18_nature_volcanic_coast_dawn.png" width="700" alt="volcanic coast at dawn">

---

### 19. 都市夜景(雨後の渋谷スクランブル) ⚡

`1536×1024 / high` — 対角線スクランブル交差点、雨に濡れた路面のネオン反射、傘さす人混みのモーションブラー、縦書き巨大日本語看板群(`カラオケ 747` `居酒屋 2F・3F` `薬方` `牛繁 焼肉` `コンタクトのアイシティ` 等)が自発描画。シネマティック teal-orange。Phase 4 で SKILL 刷新後にリライト・最良結果を選定 — 詳細は [`docs/skill-effect-comparison.md`](skill-effect-comparison.md#19-urban_tokyo_rainy_nightv3-リライト追加) 参照

<img src="../assets/capability-survey/categories/v2/19_urban_tokyo_rainy_night_v3.png" width="700" alt="Tokyo Shibuya scramble crossing at rainy night">

---

### 20. 乗り物(ヴィンテージカフェレーサー)

`1536×1024 / high` — 英国緑のカフェレーサー、ブラウンレザーシート、磨きこまれたクロームエキゾースト、夕日の石畳。Constraints `no brand logos on the bike` 完全遵守

<img src="../assets/capability-survey/categories/v2/20_vehicle_cafe_racer_motorcycle.png" width="700" alt="vintage cafe racer motorcycle">

---

### 21. スポーツ動的瞬間(ボルダリング)

`1024×1536 / high` ⭐(コスト有利) — オーバーハングを登るクライマー全身、夕陽の岩肌、ピーク瞬間捕捉

<img src="../assets/capability-survey/categories/v2/21_sports_rock_climbing_action.png" width="400" alt="rock climbing action">

---

### 22. ペット(柴犬の秋)

`1024×1024 / high` — 笑顔の柴犬全身、紅葉、ボケ味の温かい光

<img src="../assets/capability-survey/categories/v2/22_pet_shiba_inu_autumn.png" width="500" alt="Shiba Inu in autumn park">

---

### 23. 野生動物(雪原の狐)

`1024×1024 / high` — 警戒の眼差し、雪上の毛皮、ワイルドライフフォト品質

<img src="../assets/capability-survey/categories/v2/23_wildlife_red_fox_snow.png" width="500" alt="red fox in snow">

---

### 24. 線画(ファッション技法)

`1024×1024 / high` — 単一ウェイトのクリーンな黒線、流れるドレス、ヒール、Hermès 級ファッションスケッチ

<img src="../assets/capability-survey/categories/v2/24_line_drawing_fashion_sketch.png" width="500" alt="fashion line drawing">

---

### 25. 水墨画(伝統)

`1536×1024 / high` — 濃墨の鷺、淡墨の水面と霧、和紙の風合い、朱印 1 つ(Constraints 通り)、東洋画の正統

<img src="../assets/capability-survey/categories/v2/25_sumi_e_heron_ink_wash.png" width="700" alt="sumi-e heron ink wash">

---

### 26. 子供の落書き(クレヨン)

`1024×1024 / high` — 不器用な線、家族 + 家 + 太陽 + 猫、皺のある紙、本物のチャイルドアート再現

<img src="../assets/capability-survey/categories/v2/26_kids_crayon_doodle_family.png" width="500" alt="kid's crayon doodle">

---

## Part 2 — Resolution × Quality Grid(同一プロンプト 9 セル)

同じプロンプトを 3 サイズ × 3 品質 = 9 セル全部で生成し、コスト対品質を可視化。
**プロンプト**: 編集系ポートレートポスター、日本語タイトル「本と珈琲」+ 英語サブ「Tokyo, Spring 2026」

### コスト一覧

| | 1024×1024 | 1024×1536 | 1536×1024 |
|---|---|---|---|
| **low** | $0.006 (¥1) | $0.011 (¥2) | $0.011 (¥2) |
| **medium** | $0.053 (¥8) | $0.080 (¥12) | $0.079 (¥12) |
| **high** | $0.211 (¥32) | **$0.165 ⭐ (¥25)** | $0.210 (¥32) |

⭐ = 同じ `high` でも縦長(1024×1536)が正方形(1024×1024)より **安い**

### 9 セル比較

<table>
<tr>
  <th></th>
  <th>1024×1024</th>
  <th>1024×1536</th>
  <th>1536×1024</th>
</tr>
<tr>
  <th align="right">low<br><sub>¥1〜2</sub></th>
  <td><img src="../assets/capability-survey/grid/v2/grid_book_coffee_1024x1024_low.png" width="200" alt="1024x1024 low"></td>
  <td><img src="../assets/capability-survey/grid/v2/grid_book_coffee_1024x1536_low.png" width="160" alt="1024x1536 low"></td>
  <td><img src="../assets/capability-survey/grid/v2/grid_book_coffee_1536x1024_low.png" width="240" alt="1536x1024 low"></td>
</tr>
<tr>
  <th align="right">medium<br><sub>¥8〜12</sub></th>
  <td><img src="../assets/capability-survey/grid/v2/grid_book_coffee_1024x1024_medium.png" width="200" alt="1024x1024 medium"></td>
  <td><img src="../assets/capability-survey/grid/v2/grid_book_coffee_1024x1536_medium.png" width="160" alt="1024x1536 medium"></td>
  <td><img src="../assets/capability-survey/grid/v2/grid_book_coffee_1536x1024_medium.png" width="240" alt="1536x1024 medium"></td>
</tr>
<tr>
  <th align="right">high<br><sub>¥25〜32</sub></th>
  <td><img src="../assets/capability-survey/grid/v2/grid_book_coffee_1024x1024_high.png" width="200" alt="1024x1024 high"></td>
  <td><img src="../assets/capability-survey/grid/v2/grid_book_coffee_1024x1536_high.png" width="160" alt="1024x1536 high ⭐"></td>
  <td><img src="../assets/capability-survey/grid/v2/grid_book_coffee_1536x1024_high.png" width="240" alt="1536x1024 high"></td>
</tr>
</table>

### 観察される事実

1. **低品質でも日本語テキストはほぼ完璧に描画される**(本と珈琲 / Tokyo, Spring 2026)。テキスト描画の信頼性は **品質パラメータに依存しない**
2. **品質の効果はディテール(肌質感、ボケ味、生地の織り目、環境細部)に集中**。構図・色味・主要要素は low でもほぼ固まる
3. **1024×1536 high が「予算と質のスイートスポット」** を実物で証明。$0.165 で得られる出力は、$0.211 の正方 high と互角〜上回る場合あり
4. **コスト最適化の鉄則(実証済み)**:
   - **アイデア出し / プロトタイピング**: `1024×1024 low`(¥1)で十分構図検討可能
   - **ブログヒーロー / SNS バナー**: `1024×1536 medium`(¥12)が現実的
   - **プレス・LP・印刷**: `1024×1536 high`(¥25)でフル品質
   - **正方が必要なときだけ** `1024×1024 high`(¥32)

---

## メタ記録

- 実施日: 2026-04-24(Phase 4 効果検証で SKILL 公式一次資料ベース刷新後に再生成)
- 総枚数: **35 枚**(成功率 35/35 = **100%**、再生成ゼロ。19 のみ Constraints 調整のため 1 度リライト → v3 採用)
- 総コスト: 約 **$6.04 ≈ ¥905**(同一回の再生成、Phase 4 一括)
- すべての画像は **ユーザがプロンプトを書かない** ワークフロー(意図のみ伝達 → Claude が SKILL.md と過去文脈から組み立て)で生成
- v1(Phase 0 当初の 35 枚)は `assets/capability-survey/categories/*.png` に保管済み。Phase 4 v1/v2 全比較は `docs/skill-effect-comparison.md`
- 関連: `docs/dogfooding-log.md`(プレス用素材生成過程)、`docs/research-notes-014.md`(input_fidelity / 透過の一次資料検証)、`docs/research-notes-015.md` / `docs/research-notes-015-cookbook.md`(SKILL 刷新の一次資料調査)
