# Photorealism / 歴史・文脈のある場面

Cookbook 4.3 と 4.4 を統合。**「本物の写真のような自然さ」** と **「時代・場所のコンテキスト再現」** が共通課題。

## 使い所

- ポートレート / キャンディッド写真 / 広告用の人物撮影(スタジオ臭を避けたい)
- 特定の時代・歴史的イベントを背景にした場面(モデルの world knowledge を活用)
- 記録写真ふうのビジュアル(ジャーナリズム、ドキュメンタリー)

## 共通設計原則(Cookbook 引用)

> "To get believable photorealism, prompt the model as if a real photo is being captured in the moment. Use photography language (lens, lighting, framing) and explicitly ask for real texture (pores, wrinkles, fabric wear, imperfections). Avoid words that imply studio polish or staging. When detail matters, set quality='high'."
> — [Cookbook 4.3](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)

**書き方のコツ**:
- **`photorealistic` を明示的にプロンプトに入れる**(Cookbook が公式推奨、photorealistic mode を強く呼び起こす)
- 写真用語を使う: 焦点距離(`50mm lens`)、構図(`medium close-up at eye level`)、フィルム粒子(`subtle film grain`)、被写界深度(`shallow depth of field`)
- テクスチャを具体化: `pores, wrinkles, fabric wear, imperfections`
- スタジオ臭を避けるフレーズ: `No glamorization, no heavy retouching. honest and unposed.`

---

## プロンプト例 1: キャンディッドなポートレート(Cookbook 4.3)

```
Create a photorealistic candid photograph of an elderly sailor standing on a small fishing boat.
He has weathered skin with visible wrinkles, pores, and sun texture, and a few faded traditional sailor tattoos on his arms.
He is calmly adjusting a net while his dog sits nearby on the deck. Shot like a 35mm film photograph, medium close-up at eye level, using a 50mm lens.
Soft coastal daylight, shallow depth of field, subtle film grain, natural color balance.
The image should feel honest and unposed, with real skin texture, worn materials, and everyday detail. No glamorization, no heavy retouching.
```

**パラメータ**: `size=1024x1536`, `quality=medium` — 近接ポートレートで顔のディテール優先なら `high` に上げる

**CLI 例**:
```bash
$CCSKILL_GPTIMAGE_DIR/venv/bin/python $CCSKILL_GPTIMAGE_DIR/generate_image.py \
  "Create a photorealistic candid photograph of an elderly sailor ..." \
  --size 1024x1536 --quality high
```

---

## プロンプト例 2: 歴史的文脈を活用(Cookbook 4.4)

モデルの world knowledge で、明示的に "Woodstock" と言わなくても日付と場所から推論して文化的に正しい場面を描く。

```
Create a realistic outdoor crowd scene in Bethel, New York on August 16, 1969.
Photorealistic, period-accurate clothing, staging, and environment.
```

**パラメータ**: `size=1024x1536`, `quality=medium`

**応用例**(日本文脈): モデルは日本の文化イベントにも world knowledge が効く。

```
Create a photorealistic wide street scene in Tokyo's Shibuya on the night of 1999-12-31.
Period-accurate signage, fashion, and crowd atmosphere. No modern smartphones.
```

---

## 設計パターン(Cookbook Section 2 の人物・ポーズ原則を反映)

Cookbook Section 2 "People, Pose, and Action" 原文:

> "For people in scenes, describe scale, body framing, gaze, and object interactions. Examples: 'full body visible, feet included,' 'child-sized relative to the table,' 'looking down at the open book, not at the camera.'"

具体化すべき要素:
- **Scale**: 被写体の画面内での大きさ(例: `full body visible, feet included`)
- **Body framing**: フレーミング(例: `medium close-up`)
- **Gaze**: 視線の向き(例: `looking down at the open book, not at the camera`)
- **Object interactions**: 何をしているか(例: `calmly adjusting a net`)

---

## Empty / null state declaration(空状態の肯定形宣言)

gpt-image-2 は「空っぽ」を放置すると**勝手に中身を補完する**傾向がある(モデルが「マグ=飲み物」「部屋=人」を補う)。実証(2026-04-24 dogfooding): 空の Thermos マグを描かせたら茶色の液体が勝手に入った。`mug is empty, no liquid visible inside` と明示したら正しく空になった。

**コツ — null 状態は否定形でなく肯定形で書く**:

- ❌ `do not show people in the room`(否定形は効きが弱い)
- ✅ `the room is empty, no people present, only furniture visible`(肯定形で「空である状態」を宣言)

応用例: `empty plate`, `empty glass`, `blank canvas`, `unoccupied bench` なども「何が無いか」ではなく「空という状態である」と書く。文化圏雰囲気を出すシーンで「無人の街角」を描く場合も同様([`cultural-atmosphere.md`](cultural-atmosphere.md) 参照)。

---

## gpt-image-2 固有の注意

- フォトリアルで顔・肌の近接描写があるなら `quality=high` 推奨(`medium` だと肌の質感がやや CG っぽくなることがある)
- 参照写真を持ち込む場合は、**人物の同一性は自動で最大忠実度で保持**される(`input_fidelity` の指定不要)
- 歴史場面を描くとき、**日付・場所・イベント名の特定が重要**。曖昧だと「それっぽいが間違った」出力になりがち

## 出典

- Cookbook 4.3 Photorealistic / 4.4 World knowledge
- URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- 取得日: 2026-04-23
