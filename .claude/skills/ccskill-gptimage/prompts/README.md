# prompts/ — ユースケース別プロンプト集

このディレクトリは OpenAI Cookbook [GPT Image Generation Models Prompting Guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide) の 23 ユースケースを、**近い用途で統合した 14 ファイル**に整理したもの。

## 使い方(Claude 向け)

`SKILL.md` で大まかなユースケースを特定したら、該当ファイルを Read して**完成プロンプトのテンプレート + パラメータ + gpt-image-2 固有の注意**を取り込み、ユーザーの意図に合わせて合成する。

各ファイルは progressive disclosure を前提に**必要時のみロードされる想定**なので、全部を暗記する必要はない。

## インデックス

### 生成(text → image)

| ファイル | 扱うユースケース | Cookbook 節 |
|---|---|---|
| [infographics-and-diagrams.md](infographics-and-diagrams.md) | インフォグラフィック / 概念図 / 科学・教育図 / スライド・チャート | 4.1, 4.9, 4.10 |
| [photorealism.md](photorealism.md) | ナチュラルな写真表現 / 歴史・文脈のある場面 | 4.3, 4.4 |
| [logo.md](logo.md) | ブランドロゴ / 変種生成(`n`) | 4.5 |
| [ads-and-marketing.md](ads-and-marketing.md) | 広告ビジュアル / 画像内の完全一致テキスト | 4.6, 5.5 |
| [comic-and-storyboard.md](comic-and-storyboard.md) | コミック / パネル構成 / ストーリーボード | 4.7 |
| [ui-mockups.md](ui-mockups.md) | モバイル/Web アプリ UI モックアップ | 4.8 |
| [character-and-concept.md](character-and-concept.md) | キャラクター一貫性 / ホリデーカード / 玩具パッケージ | 6.2, 6.3, 6.4 |
| [cultural-atmosphere.md](cultural-atmosphere.md) | 文化圏の雰囲気(日本語看板・街並み) | Sec.2 + 実証(#015) |

### 編集(text + image → image)

| ファイル | 扱うユースケース | Cookbook 節 |
|---|---|---|
| [image-translation.md](image-translation.md) | 画像内テキストの多言語翻訳 | 4.2 |
| [style-transfer.md](style-transfer.md) | 参照画像のスタイルを別コンテンツに適用 | 5.1 |
| [try-on.md](try-on.md) | 人物の服装変更(アイデンティティ保持) | 5.2 |
| [sketch-to-render.md](sketch-to-render.md) | 手描きスケッチ → 写真リアル | 5.3 |
| [product-mockup.md](product-mockup.md) | 商品抽出・背景除去 / インテリアの精密置換 | 5.4, 6.1 |
| [scene-transform.md](scene-transform.md) | 天候・時間帯変更 / オブジェクト削除 | 5.6, 5.7 |
| [scene-composite.md](scene-composite.md) | 人物を新シーンへ / 複数画像合成 | 5.8, 5.9 |

## すべてのファイルに共通する注意

1. **Cookbook 原文プロンプトはそのまま転記**(出典: Cookbook + 取得日 2026-04-23)。英語のまま使用可、あるいは日本語意図を混ぜても可
2. **Cookbook に `input_fidelity=high` が出現する場合がある** が、gpt-image-2 では自動最大忠実度のため**指定不可(400 エラー)**。本スキル側は `generate_image.py` の main validation で自動削除するが、プロンプト組み立て時に明示的に付けないこと
3. **`background: transparent` は gpt-image-2 非対応**。透過が必要なら (a) `--model gpt-image-1.5` に切替、(b) rembg 後処理、(c) `ccskill-nanobanana` に切替
4. **コスト罠**: `1024×1536` (縦長) の `high` は **$0.165** で、`1024×1024` の `high` ($0.211) より安い
5. 編集経路(`--reference` 指定)は**常に全画面再描画**される(マスクは guidance only、公式 Cookbook 明示)。ピクセル単位の保持が必要なら Pillow 等でクロップ → 編集 → 貼り戻しのハイブリッド

## 出典

すべてのプロンプト例は OpenAI Cookbook "GPT Image Generation Models Prompting Guide" からの引用。出典 URL は各ファイルの該当プロンプト直下に明記している。
