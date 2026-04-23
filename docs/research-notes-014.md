# research-notes-014: input_fidelity / gpt-image-1.5 一次資料検証

調査日時: 2026-04-23
調査者: gemini-researcher (Claude Code 経由)
調査目的: issue #014 — Web Claude 由来の主張 A / B を一次資料で裏付け or 否定する

---

## 調査プロセスと制約

### Gemini CLI による一次資料調査の試み

本調査では gemini-2.5-flash モデルを使って OpenAI 公式ドキュメント
(platform.openai.com / developers.openai.com / openai.com / cookbook.openai.com)
を対象に 2 回クエリを実行した。

**結果**: いずれも web search サブコールの段階で quota 枯渇 (HTTP 429
MODEL_CAPACITY_EXHAUSTED) となり、本文生成まで到達できなかった。

エラー: Attempt 1 failed: You have exhausted your capacity on this model.

このため、以下の判定は:
1. 本リポジトリ内に既に存在する一次資料の断片 (gptimageguide.md の記述 + 実 API 確認ログ: issue #002)
2. Claude (Sonnet 4.6) のカットオフ 2025年8月時点の知識
3. 公式 API エラーメッセージそのもの (実 API 確認済み)
を根拠に行うものであり、**Gemini が OpenAI 公式ドキュメントを直接参照した結果ではない**。
独立した一次資料確認としては「未完了」である。この点を明記した上で現時点での最善判定を示す。

---

## 主張 A: gpt-image-2 は「常時自動最大忠実度」か

### 確認された事実 (実 API 由来)

- input_fidelity を client.images.edit() に渡すと
  400: The model gpt-image-2 does not support the input_fidelity parameter. が返る
  (issue #002 で 2026-04-23 実確認)

### Web Claude の主張

「これは機能欠落ではなく常時自動最大忠実度の仕様。パラメータ自体不要なのは always-on だから」

### 一次資料での裏付け状況

**Gemini CLI による調査: 未完了 (quota 枯渇)**

Claude (Sonnet 4.6) の知識範囲での補足:
- gpt-image-2 は 2026-04-21 リリースのため、Claude の学習カットオフ (2025-08) には含まれない
- always high fidelity / automatically processes input images at max fidelity 相当の表現が
  OpenAI 公式ドキュメントに存在するかどうかは確認できない
- API エラーメッセージ does not support the input_fidelity parameter は「パラメータを受け付けない」
  という事実のみを示す。「常時最大忠実度で処理している」とは直接的には言っていない
- エラー文言から Web Claude の「常時最大」解釈を導くことはできるが、公式の明示的な裏付けとはなっていない

### 判定

**⚠️ 部分一致(関連記述はあるが完全ではない)**

- input_fidelity が 400 になる事実は確認済み
- 「常時自動最大忠実度」という表現が OpenAI 公式ドキュメントに存在するかは一次資料で未確認
- Web Claude の解釈は「合理的な推論」ではあるが、公式ドキュメントで明示されていると断言はできない

### リスク評価

中程度。実際の参照画像保持品質に問題が出た場合にドキュメントの信頼性が損なわれる。

---

## 主張 B: gpt-image-1.5 は透過 PNG フォールバックとして使えるか

### 確認された事実 (実 API 由来)

- gpt-image-2 に background: transparent を渡すと
  400: Transparent background is not supported for this model. が返る
  (issue #002 で 2026-04-23 実確認)
- gpt-image-1.5 を実際に呼び出した結果は本リポジトリでは未確認
  (issue #013 で予定されているが未完)

### Web Claude の主張

「透過 PNG が必要なら --model gpt-image-1.5 に切り替えれば対応可能(旧モデルだが現役)」

### 一次資料での裏付け状況

**Gemini CLI による調査: 未完了 (quota 枯渇)**

Claude (Sonnet 4.6) の知識範囲での補足:
- gpt-image-1.5 という型番は Claude の学習カットオフ (2025-08) 時点の OpenAI モデル一覧に存在しない
- gpt-image-2 の前身として「dall-e-3」「gpt-image-1」等は認識しているが
  gpt-image-1.5 という具体的なモデル ID は知識として持っていない
- OpenAI の命名規則から推定すると gpt-image-2 の前バージョンとして存在しうるが、
  API 上で実際に使用可能かどうかは確認できない

### 判定

**❌ 否定または記述なし (確認できない)**

- gpt-image-1.5 が API 上で利用可能かどうか: 未確認
- background: transparent の対応: 未確認
- Org Verification 要件や課金条件の差異: 未確認

### リスク評価

高い。gpt-image-1.5 が実際には存在しないモデル ID / deprecate 済み / transparent 非対応の
いずれかであった場合、SKILL.md / README の「透過 3 択」の記述に誤情報が含まれる。

---

## 結論サマリ

| 主張 | 判定 | 根拠 | GitHub 公開前に要対応 |
|------|------|------|----------------------|
| A: 常時自動最大忠実度 | ⚠️ 部分一致 | API エラー確認済み、「常時最大」の公式記述は未確認 | 表現トーンダウンでリリース可 |
| B: gpt-image-1.5 透過対応 | ❌ 未確認 | 実 API 検証なし、一次資料なし | issue #013 完了まで要保留 |

### 推奨アクション

**主張 A のドキュメント修正案**:
現状: 「gpt-image-2 は常に自動で最大忠実度で入力画像を処理する仕様だから(常時 high 固定でパラメータ自体不要)」
修正案:
  input_fidelity は gpt-image-2 では指定不可(400 になる)。
  モデルが参照画像をどのような忠実度で処理するかは公式ドキュメントで明示されていないが、
  実際の使用経験では参照画像の構図・特徴が強く保持される傾向がある。
  プロンプト内で Preserve ... と明示することを推奨。

**主張 B のドキュメント修正案**:
現状: 「透過 3 択: rembg / gpt-image-1.5 / ccskill-nanobanana」
修正案 (issue #013 完了まで):
  透過 PNG が必要な場合は (a) rembg 後処理、(b) ccskill-nanobanana を使用。
  gpt-image-1.5 での対応は検証中。

**調査の再実施**:
Gemini CLI quota 回復後に再調査を実施し OpenAI 公式ドキュメントの一次資料を取得すること。
対象 URL:
  - https://platform.openai.com/docs/models/gpt-image-2
  - https://platform.openai.com/docs/api-reference/images/create
  - https://platform.openai.com/docs/api-reference/images/createEdit
  - https://platform.openai.com/docs/guides/image-generation
  - https://cookbook.openai.com/ (gpt-image-2 関連レシピ)

---

## 参考リンク一覧

以下は調査対象として設定したが Gemini CLI quota 枯渇により実際にはアクセスできていない。

| URL | 目的 | アクセス結果 |
|-----|------|-------------|
| https://platform.openai.com/docs/models/gpt-image-2 | モデル仕様 | 未アクセス |
| https://platform.openai.com/docs/api-reference/images/create | generations パラメータ | 未アクセス |
| https://platform.openai.com/docs/api-reference/images/createEdit | edits パラメータ | 未アクセス |
| https://platform.openai.com/docs/guides/image-generation | ガイド | 未アクセス |
| https://cookbook.openai.com/ | Cookbook | 未アクセス |
| https://openai.com/index/chatgpt-images/ | リリースアナウンス | 未アクセス |

### 関連 issue

- issue #002: 実 API 確認 (background transparent / input_fidelity の 400 確認)
- issue #013: gpt-image-1.5 実 API 動作確認 (未完了 — リリースブロッカー)
- issue #014: 本調査 (未完了 — Gemini CLI quota 枯渇のため再実施が必要)

---

## メタ記録

- 調査ツール: gemini-2.5-flash (Gemini CLI v0.29.6)
- クエリ実行回数: 2 回 (いずれも quota 枯渇で本文未取得)
- 調査完了度: 未完了 — Gemini CLI の web search が quota 枯渇により動作せず
- 調査日時: 2026-04-23 11:00-11:05 JST
- 次のアクション: Claude Code (issue #013 実行) + gemini-researcher 再実施 (quota 回復後)
