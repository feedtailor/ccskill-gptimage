"""ccskill-gptimage 画像生成スクリプトのテスト"""

import base64
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_image import (
    DEFAULT_BACKGROUND,
    DEFAULT_MODEL,
    DEFAULT_MODERATION,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_QUALITY,
    DEFAULT_SIZE,
    OUTPUT_FORMAT_TO_EXT,
    generate_image,
    get_output_path,
    main,
    parse_args,
)


# 1x1 透過 PNG の base64(モック用)
DUMMY_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgAAIAAAUAAeImBZsAAAAASUVORK5CYII="
)


def _make_image_response(b64: str = DUMMY_PNG_B64, revised_prompt: str | None = None) -> Mock:
    """OpenAI Images API の擬似レスポンスを作る"""
    datum = Mock()
    datum.b64_json = b64
    datum.revised_prompt = revised_prompt
    response = Mock()
    response.data = [datum]
    return response


class TestParseArgs:
    def test_prompt_only_uses_defaults(self):
        args = parse_args(["a cat playing piano"])
        assert args.prompt == "a cat playing piano"
        assert args.size == DEFAULT_SIZE
        assert args.quality == DEFAULT_QUALITY
        assert args.output == DEFAULT_OUTPUT_DIR
        assert args.output_format == DEFAULT_OUTPUT_FORMAT
        assert args.background == DEFAULT_BACKGROUND
        assert args.moderation == DEFAULT_MODERATION
        assert args.reference == []
        assert args.mask is None
        assert args.input_fidelity is None

    def test_quality_choice(self):
        args = parse_args(["p", "--quality", "high"])
        assert args.quality == "high"

    def test_size(self):
        args = parse_args(["p", "--size", "1024x1536"])
        assert args.size == "1024x1536"

    def test_background_transparent(self):
        args = parse_args(["p", "--background", "transparent"])
        assert args.background == "transparent"

    def test_output_format(self):
        args = parse_args(["p", "--output-format", "jpeg"])
        assert args.output_format == "jpeg"

    def test_output_compression(self):
        args = parse_args(["p", "--output-format", "jpeg", "--output-compression", "80"])
        assert args.output_compression == 80

    def test_reference_multiple(self):
        args = parse_args([
            "p",
            "--reference", "a.png",
            "--reference", "b.png",
        ])
        assert args.reference == ["a.png", "b.png"]

    def test_mask(self):
        args = parse_args(["p", "--reference", "src.png", "--mask", "m.png"])
        assert args.mask == "m.png"

    def test_input_fidelity(self):
        args = parse_args(["p", "--reference", "a.png", "--input-fidelity", "high"])
        assert args.input_fidelity == "high"

    def test_moderation_low(self):
        args = parse_args(["p", "--moderation", "low"])
        assert args.moderation == "low"


class TestGetOutputPath:
    def test_creates_directory_if_not_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "new_subdir"
            path = get_output_path(str(out))
            assert out.exists()
            assert path.parent == out

    def test_default_extension_is_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = get_output_path(tmp)
            assert path.suffix == ".png"

    def test_jpeg_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = get_output_path(tmp, output_format="jpeg")
            assert path.suffix == ".jpg"

    def test_webp_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = get_output_path(tmp, output_format="webp")
            assert path.suffix == ".webp"

    def test_unknown_format_falls_back_to_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = get_output_path(tmp, output_format="bmp")
            assert path.suffix == ".png"

    def test_filename_is_timestamp(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = get_output_path(tmp)
            stem = path.stem
            assert len(stem) == 15  # YYYYMMDD_HHMMSS
            assert stem.replace("_", "").isdigit()


class TestOutputFormatMapping:
    def test_png(self):
        assert OUTPUT_FORMAT_TO_EXT["png"] == ".png"

    def test_jpeg(self):
        assert OUTPUT_FORMAT_TO_EXT["jpeg"] == ".jpg"

    def test_webp(self):
        assert OUTPUT_FORMAT_TO_EXT["webp"] == ".webp"


class TestGenerateImageBasic:
    @patch("generate_image.OpenAI")
    def test_text_to_image_calls_generations(self, mock_openai_cls):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.generate.return_value = _make_image_response()

        with tempfile.TemporaryDirectory() as tmp:
            result = generate_image(
                prompt="a fox logo",
                size="1024x1024",
                quality="high",
                output_dir=tmp,
                output_format="png",
                background="auto",
            )

            assert result is not None
            assert result.endswith(".png")
            client.images.generate.assert_called_once()
            kwargs = client.images.generate.call_args.kwargs
            assert kwargs["model"] == DEFAULT_MODEL
            assert kwargs["prompt"] == "a fox logo"
            assert kwargs["size"] == "1024x1024"
            assert kwargs["quality"] == "high"
            # opaque/auto の場合は background パラメータは送らない
            assert "background" not in kwargs or kwargs["background"] != "transparent"
            # ファイルが実際に書き出されている
            assert Path(result).exists()
            assert Path(result).stat().st_size > 0

    @patch("generate_image.OpenAI")
    def test_transparent_background_passes_param(self, mock_openai_cls):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.generate.return_value = _make_image_response()

        with tempfile.TemporaryDirectory() as tmp:
            generate_image(
                prompt="logo",
                size="1024x1024",
                quality="medium",
                output_dir=tmp,
                output_format="png",
                background="transparent",
            )

        kwargs = client.images.generate.call_args.kwargs
        assert kwargs["background"] == "transparent"

    @patch("generate_image.OpenAI")
    def test_output_format_passed_through(self, mock_openai_cls):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.generate.return_value = _make_image_response()

        with tempfile.TemporaryDirectory() as tmp:
            result = generate_image(
                prompt="x",
                output_dir=tmp,
                output_format="jpeg",
                output_compression=70,
            )

        kwargs = client.images.generate.call_args.kwargs
        assert kwargs["output_format"] == "jpeg"
        assert kwargs["output_compression"] == 70
        assert result.endswith(".jpg")

    @patch("generate_image.OpenAI")
    def test_moderation_low_is_passed(self, mock_openai_cls):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.generate.return_value = _make_image_response()

        with tempfile.TemporaryDirectory() as tmp:
            generate_image(prompt="x", output_dir=tmp, moderation="low")

        assert client.images.generate.call_args.kwargs["moderation"] == "low"

    @patch("generate_image.OpenAI")
    def test_no_data_in_response_returns_none(self, mock_openai_cls):
        client = Mock()
        mock_openai_cls.return_value = client
        empty = Mock()
        empty.data = []
        client.images.generate.return_value = empty

        with tempfile.TemporaryDirectory() as tmp:
            result = generate_image(prompt="x", output_dir=tmp)

        assert result is None

    @patch("generate_image.OpenAI")
    def test_api_exception_propagates(self, mock_openai_cls):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.generate.side_effect = RuntimeError("boom")

        with tempfile.TemporaryDirectory() as tmp:
            with pytest.raises(RuntimeError, match="boom"):
                generate_image(prompt="x", output_dir=tmp)


class TestGenerateImageWithReference:
    @patch("generate_image.OpenAI")
    def test_reference_routes_to_edits(self, mock_openai_cls):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.edit.return_value = _make_image_response()

        with tempfile.TemporaryDirectory() as tmp:
            ref = Path(tmp) / "ref.png"
            ref.write_bytes(base64.b64decode(DUMMY_PNG_B64))
            result = generate_image(
                prompt="change background to sunset",
                output_dir=tmp,
                reference_images=[str(ref)],
                input_fidelity="high",
            )

        assert result is not None
        client.images.edit.assert_called_once()
        client.images.generate.assert_not_called()
        kwargs = client.images.edit.call_args.kwargs
        assert kwargs["model"] == DEFAULT_MODEL
        assert kwargs["prompt"] == "change background to sunset"
        assert kwargs["input_fidelity"] == "high"
        # image は file-like のリスト or 単体
        assert "image" in kwargs

    @patch("generate_image.OpenAI")
    def test_multiple_references(self, mock_openai_cls):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.edit.return_value = _make_image_response()

        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for name in ("a.png", "b.png", "c.png"):
                p = Path(tmp) / name
                p.write_bytes(base64.b64decode(DUMMY_PNG_B64))
                paths.append(str(p))
            generate_image(
                prompt="combine",
                output_dir=tmp,
                reference_images=paths,
            )

        kwargs = client.images.edit.call_args.kwargs
        # 複数枚はリストで渡す
        assert isinstance(kwargs["image"], list)
        assert len(kwargs["image"]) == 3

    @patch("generate_image.OpenAI")
    def test_mask_is_passed(self, mock_openai_cls):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.edit.return_value = _make_image_response()

        with tempfile.TemporaryDirectory() as tmp:
            ref = Path(tmp) / "ref.png"
            ref.write_bytes(base64.b64decode(DUMMY_PNG_B64))
            mask = Path(tmp) / "mask.png"
            mask.write_bytes(base64.b64decode(DUMMY_PNG_B64))
            generate_image(
                prompt="inpaint",
                output_dir=tmp,
                reference_images=[str(ref)],
                mask=str(mask),
            )

        assert "mask" in client.images.edit.call_args.kwargs

    def test_nonexistent_reference_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = generate_image(
                prompt="x",
                output_dir=tmp,
                reference_images=["/no/such/file.png"],
            )
            assert result is None

    def test_nonexistent_reference_prints_error(self, capsys):
        with tempfile.TemporaryDirectory() as tmp:
            generate_image(
                prompt="x",
                output_dir=tmp,
                reference_images=["/no/such/file.png"],
            )
        captured = capsys.readouterr()
        assert "[Error]" in captured.out
        assert "参照画像が見つかりません" in captured.out


class TestRevisedPromptAndMetadata:
    @patch("generate_image.OpenAI")
    def test_revised_prompt_is_printed(self, mock_openai_cls, capsys):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.generate.return_value = _make_image_response(
            revised_prompt="A cinematic neon Tokyo street at night, ..."
        )

        with tempfile.TemporaryDirectory() as tmp:
            generate_image(prompt="tokyo", output_dir=tmp)

        captured = capsys.readouterr()
        assert "[Revised]" in captured.out
        assert "cinematic neon Tokyo" in captured.out

    @patch("generate_image.OpenAI")
    def test_metadata_sidecar_is_written(self, mock_openai_cls):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.generate.return_value = _make_image_response(
            revised_prompt="rev"
        )

        with tempfile.TemporaryDirectory() as tmp:
            result = generate_image(
                prompt="x",
                size="1024x1024",
                quality="medium",
                output_dir=tmp,
            )

            meta_path = Path(result).with_suffix(Path(result).suffix + ".json")
            assert meta_path.exists()
            meta = json.loads(meta_path.read_text())
            assert meta["prompt"] == "x"
            assert meta["size"] == "1024x1024"
            assert meta["quality"] == "medium"
            assert meta["model"] == DEFAULT_MODEL
            assert meta["revised_prompt"] == "rev"
            assert "timestamp" in meta


class TestDefaults:
    def test_default_model_is_gpt_image_2(self):
        assert DEFAULT_MODEL == "gpt-image-2"

    def test_default_size(self):
        assert DEFAULT_SIZE == "1024x1024"

    def test_default_quality(self):
        assert DEFAULT_QUALITY == "auto"

    def test_default_output_format(self):
        assert DEFAULT_OUTPUT_FORMAT == "png"

    def test_default_output_dir(self):
        assert DEFAULT_OUTPUT_DIR == "./generated_images"

    def test_default_background(self):
        assert DEFAULT_BACKGROUND == "auto"

    def test_default_moderation(self):
        assert DEFAULT_MODERATION == "auto"


class TestMainValidation:
    def _run_main(self, argv: list[str]) -> int | None:
        with patch.object(sys, "argv", ["generate_image.py", *argv]):
            try:
                main()
            except SystemExit as e:
                return e.code
        return None

    def test_transparent_with_gpt_image_2_exits(self, capsys):
        code = self._run_main(["p", "--background", "transparent"])
        assert code == 2
        out = capsys.readouterr().out
        assert "transparent" in out
        assert "gpt-image-1.5" in out

    def test_transparent_with_unknown_model_exits(self, capsys):
        code = self._run_main(["p", "--background", "transparent", "--model", "dall-e-3"])
        assert code == 2
        assert "transparent" in capsys.readouterr().out

    @patch("generate_image.generate_image")
    def test_transparent_with_gpt_image_1_5_passes_through(self, mock_gen):
        mock_gen.return_value = "/tmp/fake.png"
        code = self._run_main([
            "p",
            "--background", "transparent",
            "--model", "gpt-image-1.5",
        ])
        assert code is None
        mock_gen.assert_called_once()
        assert mock_gen.call_args.kwargs["background"] == "transparent"
        assert mock_gen.call_args.kwargs["model"] == "gpt-image-1.5"

    @patch("generate_image.generate_image")
    def test_transparent_with_gpt_image_1_passes_through(self, mock_gen):
        mock_gen.return_value = "/tmp/fake.png"
        code = self._run_main([
            "p",
            "--background", "transparent",
            "--model", "gpt-image-1",
        ])
        assert code is None
        mock_gen.assert_called_once()

    def test_input_fidelity_with_gpt_image_2_is_dropped(self, capsys):
        with patch("generate_image.generate_image") as mock_gen:
            mock_gen.return_value = "/tmp/fake.png"
            self._run_main(["p", "--reference", "ref.png", "--input-fidelity", "high"])
            assert mock_gen.call_args.kwargs["input_fidelity"] is None
        assert "[Info]" in capsys.readouterr().out
