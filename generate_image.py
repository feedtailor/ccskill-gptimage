#!/usr/bin/env python3
"""ccskill-gptimage 画像生成スクリプト

OpenAI gpt-image-2 (ChatGPT Images 2.0) を使用して画像を生成・編集する。

使用例:
    python generate_image.py "a minimalist fox logo, flat vector, navy and gold"
    python generate_image.py "背景を夕焼けに" --reference original.png --input-fidelity high
    python generate_image.py "gift basket on white" --background transparent --output-format png

環境変数:
    OPENAI_API_KEY: OpenAI API キー(.env でも可)
"""

import argparse
import base64
import contextlib
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

_script_dir = Path(__file__).parent
load_dotenv(_script_dir / ".env")

DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1024x1024"
DEFAULT_QUALITY = "auto"
DEFAULT_OUTPUT_FORMAT = "png"
DEFAULT_OUTPUT_DIR = "./generated_images"
DEFAULT_BACKGROUND = "auto"
DEFAULT_MODERATION = "auto"

OUTPUT_FORMAT_TO_EXT = {
    "png": ".png",
    "jpeg": ".jpg",
    "webp": ".webp",
}

SIZE_CHOICES = ["auto", "1024x1024", "1024x1536", "1536x1024"]
QUALITY_CHOICES = ["auto", "low", "medium", "high"]
BACKGROUND_CHOICES = ["auto", "transparent", "opaque"]
OUTPUT_FORMAT_CHOICES = ["png", "jpeg", "webp"]
MODERATION_CHOICES = ["auto", "low"]
INPUT_FIDELITY_CHOICES = ["high", "low"]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OpenAI gpt-image-2 で画像を生成・編集します"
    )
    parser.add_argument("prompt", type=str, help="画像生成のプロンプト")
    parser.add_argument(
        "--size",
        type=str,
        default=DEFAULT_SIZE,
        choices=SIZE_CHOICES,
        help=f"出力サイズ (デフォルト: {DEFAULT_SIZE})",
    )
    parser.add_argument(
        "--quality",
        type=str,
        default=DEFAULT_QUALITY,
        choices=QUALITY_CHOICES,
        help=f"品質 (デフォルト: {DEFAULT_QUALITY})",
    )
    parser.add_argument(
        "--background",
        type=str,
        default=DEFAULT_BACKGROUND,
        choices=BACKGROUND_CHOICES,
        help=(
            f"背景 (デフォルト: {DEFAULT_BACKGROUND})。"
            " 注意: gpt-image-2 は transparent 非対応(400 になります)。"
            " 透過 PNG が必要な場合は ccskill-nanobanana を使ってください。"
        ),
    )
    parser.add_argument(
        "--output-format",
        dest="output_format",
        type=str,
        default=DEFAULT_OUTPUT_FORMAT,
        choices=OUTPUT_FORMAT_CHOICES,
        help=f"出力形式 (デフォルト: {DEFAULT_OUTPUT_FORMAT})",
    )
    parser.add_argument(
        "--output-compression",
        dest="output_compression",
        type=int,
        default=None,
        help="出力圧縮率 (jpeg/webp 時、0-100)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f"出力ディレクトリ (デフォルト: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--reference",
        type=str,
        action="append",
        default=[],
        help="参照画像のパス (複数指定可)。指定すると edits API に切替",
    )
    parser.add_argument(
        "--mask",
        type=str,
        default=None,
        help="マスク画像 (透明部分が編集対象。--reference 必須)",
    )
    parser.add_argument(
        "--input-fidelity",
        dest="input_fidelity",
        type=str,
        default=None,
        choices=INPUT_FIDELITY_CHOICES,
        help=(
            "参照画像の保持忠実度。"
            " 注意: gpt-image-2 は **常に自動で最大忠実度** で入力画像を処理するため、"
            " 本パラメータの指定は不要です(指定すると 400 エラー)。"
            " 旧モデル `gpt-image-1.5` を `--model` で指定する場合は high/low が指定可能です。"
        ),
    )
    parser.add_argument(
        "--moderation",
        type=str,
        default=DEFAULT_MODERATION,
        choices=MODERATION_CHOICES,
        help=f"モデレーション (デフォルト: {DEFAULT_MODERATION})",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"モデル ID (デフォルト: {DEFAULT_MODEL})",
    )
    return parser.parse_args(argv)


def get_output_path(output_dir: str, output_format: str = DEFAULT_OUTPUT_FORMAT) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = OUTPUT_FORMAT_TO_EXT.get(output_format, ".png")
    return out / f"{timestamp}{ext}"


def _build_generate_kwargs(
    *,
    model: str,
    prompt: str,
    size: str,
    quality: str,
    background: str,
    output_format: str,
    output_compression: int | None,
    moderation: str,
) -> dict:
    """Image API /generations 用のパラメータを組み立てる。auto は省略する。"""
    kwargs: dict = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "output_format": output_format,
        "n": 1,
    }
    if background and background != "auto":
        kwargs["background"] = background
    if moderation and moderation != "auto":
        kwargs["moderation"] = moderation
    if output_compression is not None and output_format in ("jpeg", "webp"):
        kwargs["output_compression"] = output_compression
    return kwargs


def _call_image_generations(client: OpenAI, **kwargs):
    """Image API 経路: テキスト→画像生成"""
    return client.images.generate(**kwargs)


def _call_image_edits(client: OpenAI, **kwargs):
    """Image API 経路: 参照画像/マスクありの編集"""
    return client.images.edit(**kwargs)


def _save_metadata(image_path: Path, meta: dict) -> Path:
    meta_path = image_path.with_suffix(image_path.suffix + ".json")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    return meta_path


def generate_image(
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    size: str = DEFAULT_SIZE,
    quality: str = DEFAULT_QUALITY,
    background: str = DEFAULT_BACKGROUND,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
    output_compression: int | None = None,
    moderation: str = DEFAULT_MODERATION,
    reference_images: list[str] | None = None,
    mask: str | None = None,
    input_fidelity: str | None = None,
) -> str | None:
    """gpt-image-2 で画像を生成し、ファイルパスを返す。失敗時は None。"""
    if reference_images:
        for p in reference_images:
            if not Path(p).exists():
                print(f"[Error] 参照画像が見つかりません: {p}")
                return None
    if mask and not Path(mask).exists():
        print(f"[Error] マスク画像が見つかりません: {mask}")
        return None

    client = OpenAI()

    base_kwargs = _build_generate_kwargs(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        background=background,
        output_format=output_format,
        output_compression=output_compression,
        moderation=moderation,
    )

    if reference_images:
        with contextlib.ExitStack() as stack:
            files = [stack.enter_context(open(p, "rb")) for p in reference_images]
            edit_kwargs = dict(base_kwargs)
            edit_kwargs["image"] = files if len(files) > 1 else files[0]
            if mask:
                edit_kwargs["mask"] = stack.enter_context(open(mask, "rb"))
            if input_fidelity:
                edit_kwargs["input_fidelity"] = input_fidelity
            response = _call_image_edits(client, **edit_kwargs)
    else:
        response = _call_image_generations(client, **base_kwargs)

    data = getattr(response, "data", None) or []
    if not data:
        print("[Warning] レスポンスに画像が含まれていませんでした")
        return None

    datum = data[0]
    b64 = getattr(datum, "b64_json", None)
    if not b64:
        print("[Warning] レスポンスに b64_json が含まれていませんでした")
        return None

    revised = getattr(datum, "revised_prompt", None)
    if revised:
        print(f"[Revised] {revised}")

    output_path = get_output_path(output_dir, output_format)
    output_path.write_bytes(base64.b64decode(b64))
    print(f"[Success] 画像を保存しました: {output_path}")

    meta = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "background": background,
        "output_format": output_format,
        "moderation": moderation,
        "reference_images": reference_images or [],
        "mask": mask,
        "input_fidelity": input_fidelity,
        "revised_prompt": revised,
        "timestamp": datetime.now().isoformat(),
    }
    _save_metadata(output_path, meta)

    return str(output_path)


def main():
    args = parse_args()

    if args.mask and not args.reference:
        print("[Error] --mask は --reference と併用してください")
        sys.exit(1)
    if args.background == "transparent" and not args.model.startswith("gpt-image-1"):
        print(
            f"[Error] {args.model} は --background transparent をサポートしていません。"
            " 透過 PNG が必要な場合: (1) --model gpt-image-1.5 に切替、"
            " (2) 生成後に rembg 等で背景除去、"
            " (3) ccskill-nanobanana を使用"
        )
        sys.exit(2)
    if args.input_fidelity is not None and args.model.startswith("gpt-image-2"):
        print(
            "[Info] gpt-image-2 は常に自動で最大忠実度で入力画像を処理します。"
            " --input-fidelity の指定は不要なため省略します(API エラーを回避)"
        )
        args.input_fidelity = None

    try:
        result = generate_image(
            prompt=args.prompt,
            model=args.model,
            size=args.size,
            quality=args.quality,
            background=args.background,
            output_dir=args.output,
            output_format=args.output_format,
            output_compression=args.output_compression,
            moderation=args.moderation,
            reference_images=args.reference if args.reference else None,
            mask=args.mask,
            input_fidelity=args.input_fidelity,
        )
        if result is None:
            sys.exit(1)
    except Exception as e:
        print(f"[Error] 画像生成に失敗しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
