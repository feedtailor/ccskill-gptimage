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
    BACKEND_CHOICES,
    DEFAULT_BACKEND,
    DEFAULT_BACKGROUND,
    DEFAULT_MODEL,
    DEFAULT_MODERATION,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_QUALITY,
    DEFAULT_SIZE,
    OUTPUT_FORMAT_TO_EXT,
    _codex_subscription_available,
    _resolve_backend,
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


@pytest.fixture(autouse=True)
def _force_api_backend(request, monkeypatch):
    """既存テストは Codex を使わない前提に固定する。
    backend 検出ロジックそのものをテストする場合は @pytest.mark.no_force_api_backend で opt-out。"""
    if request.node.get_closest_marker("no_force_api_backend"):
        return
    monkeypatch.setattr("generate_image._codex_subscription_available", lambda: False)


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

    def test_output_name(self):
        args = parse_args(["p", "--output-name", "hero"])
        assert args.output_name == "hero"

    def test_output_name_default_none(self):
        args = parse_args(["p"])
        assert args.output_name is None


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

    def test_custom_name_overrides_timestamp(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = get_output_path(tmp, output_format="png", name="my_image")
            assert path.name == "my_image.png"

    def test_custom_name_with_jpeg(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = get_output_path(tmp, output_format="jpeg", name="cover")
            assert path.name == "cover.jpg"


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
    def test_output_name_is_used_for_file(self, mock_openai_cls):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.generate.return_value = _make_image_response()

        with tempfile.TemporaryDirectory() as tmp:
            result = generate_image(
                prompt="x",
                output_dir=tmp,
                output_format="png",
                output_name="my_hero",
            )
            assert result is not None
            assert Path(result).name == "my_hero.png"
            assert Path(result).exists()

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


# ---------------------------------------------------------------------------
# Backend detection / dispatch (Codex CLI integration, issue #017)
# ---------------------------------------------------------------------------


class TestBackendChoices:
    def test_default_backend_is_auto(self):
        assert DEFAULT_BACKEND == "auto"

    def test_backend_choices_contains_three(self):
        assert set(BACKEND_CHOICES) == {"auto", "codex", "api"}

    def test_parse_args_default_backend(self):
        args = parse_args(["p"])
        assert args.backend == DEFAULT_BACKEND

    def test_parse_args_explicit_backend(self):
        args = parse_args(["p", "--backend", "codex"])
        assert args.backend == "codex"


@pytest.mark.no_force_api_backend
class TestCodexSubscriptionAvailable:
    """`_codex_subscription_available()` 自身の挙動。
    autouse fixture を opt-out して実関数を呼ぶ。"""

    def test_returns_false_when_codex_not_in_path(self, monkeypatch):
        monkeypatch.setattr("generate_image.shutil.which", lambda name: None)
        assert _codex_subscription_available() is False

    def test_returns_false_when_auth_file_missing(self, monkeypatch, tmp_path):
        monkeypatch.setattr("generate_image.shutil.which", lambda name: "/usr/local/bin/codex")
        monkeypatch.setattr("generate_image.CODEX_AUTH_FILE", tmp_path / "missing.json")
        assert _codex_subscription_available() is False

    def test_returns_false_when_auth_file_invalid_json(self, monkeypatch, tmp_path):
        bad = tmp_path / "auth.json"
        bad.write_text("this is not json")
        monkeypatch.setattr("generate_image.shutil.which", lambda name: "/usr/local/bin/codex")
        monkeypatch.setattr("generate_image.CODEX_AUTH_FILE", bad)
        assert _codex_subscription_available() is False

    def test_returns_false_when_tokens_missing(self, monkeypatch, tmp_path):
        f = tmp_path / "auth.json"
        f.write_text(json.dumps({"OPENAI_API_KEY": "sk-foo"}))
        monkeypatch.setattr("generate_image.shutil.which", lambda name: "/usr/local/bin/codex")
        monkeypatch.setattr("generate_image.CODEX_AUTH_FILE", f)
        assert _codex_subscription_available() is False

    def test_returns_false_when_access_token_missing(self, monkeypatch, tmp_path):
        f = tmp_path / "auth.json"
        f.write_text(json.dumps({"tokens": {"refresh_token": "x"}}))
        monkeypatch.setattr("generate_image.shutil.which", lambda name: "/usr/local/bin/codex")
        monkeypatch.setattr("generate_image.CODEX_AUTH_FILE", f)
        assert _codex_subscription_available() is False

    def test_returns_true_when_chatgpt_subscription_logged_in(self, monkeypatch, tmp_path):
        f = tmp_path / "auth.json"
        f.write_text(json.dumps({"tokens": {"access_token": "ey...", "refresh_token": "rt"}}))
        monkeypatch.setattr("generate_image.shutil.which", lambda name: "/usr/local/bin/codex")
        monkeypatch.setattr("generate_image.CODEX_AUTH_FILE", f)
        assert _codex_subscription_available() is True


class TestResolveBackend:
    def test_explicit_codex_returns_codex(self):
        assert _resolve_backend("codex") == "codex"

    def test_explicit_api_returns_api(self):
        assert _resolve_backend("api") == "api"

    def test_auto_with_codex_available_returns_codex(self, monkeypatch):
        monkeypatch.setattr("generate_image._codex_subscription_available", lambda: True)
        assert _resolve_backend("auto") == "codex"

    def test_auto_without_codex_with_api_key_returns_api(self, monkeypatch):
        monkeypatch.setattr("generate_image._codex_subscription_available", lambda: False)
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        assert _resolve_backend("auto") == "api"

    def test_auto_without_codex_without_api_key_returns_api(self, monkeypatch):
        """codex も key も無い場合でも api を返し、後段の OpenAI() で native エラーに任せる"""
        monkeypatch.setattr("generate_image._codex_subscription_available", lambda: False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        assert _resolve_backend("auto") == "api"


class TestGenerateViaCodex:
    """Codex backend 経由の生成ロジック。subprocess と画像探索をモックする"""

    @patch("generate_image.subprocess.run")
    def test_codex_subprocess_args_have_prompt_before_image(
        self, mock_run, monkeypatch, tmp_path
    ):
        """`-i` は variadic で後続 positional を食う罠を回避するため、prompt は -i より前"""
        # 生成画像をでっち上げ
        fake_image = tmp_path / "ig_fake.png"
        fake_image.write_bytes(base64.b64decode(DUMMY_PNG_B64))
        monkeypatch.setattr(
            "generate_image._find_latest_codex_image",
            lambda since: fake_image,
        )
        mock_run.return_value = Mock(returncode=0, stdout="ok", stderr="")

        ref = tmp_path / "ref.png"
        ref.write_bytes(base64.b64decode(DUMMY_PNG_B64))

        out_dir = tmp_path / "out"
        result = generate_image(
            prompt="add a red beret",
            backend="codex",
            output_dir=str(out_dir),
            reference_images=[str(ref)],
        )
        assert result is not None

        cmd = mock_run.call_args[0][0]
        # prompt は positional の 1 つ、`-i` ペアより前にあること
        assert "codex" in cmd[0]
        assert "exec" in cmd
        assert "-i" in cmd
        i_idx = cmd.index("-i")
        # `-i` の直前は引数フラグ系 (--sandbox の値) or プロンプト文字列。
        # 重要なのはプロンプト文字列が `-i` より前にあること。
        # -i の引数 (ref.png 絶対パス) は -i の直後
        assert cmd[i_idx + 1] == str(ref)
        # prompt が -i より前のどこかにある
        prompt_indices = [k for k, v in enumerate(cmd) if "add a red beret" in v]
        assert prompt_indices, "prompt not found in command"
        assert max(prompt_indices) < i_idx

    @patch("generate_image.subprocess.run")
    def test_codex_includes_image_gen_directive_in_prompt(
        self, mock_run, monkeypatch, tmp_path
    ):
        """API 経由を防ぐため『image_gen を直接使え』ディレクティブを必ず含める"""
        fake = tmp_path / "ig_x.png"
        fake.write_bytes(base64.b64decode(DUMMY_PNG_B64))
        monkeypatch.setattr("generate_image._find_latest_codex_image", lambda since: fake)
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        generate_image(
            prompt="hello",
            backend="codex",
            output_dir=str(tmp_path / "out"),
        )
        cmd = mock_run.call_args[0][0]
        # cmd の中に Codex agent 向けプロンプトがあり、そこに image_gen の指示が含まれる
        joined = " ".join(cmd)
        assert "image_gen" in joined

    @patch("generate_image.subprocess.run")
    def test_codex_copies_latest_image_to_output_path(
        self, mock_run, monkeypatch, tmp_path
    ):
        fake = tmp_path / "ig_x.png"
        fake.write_bytes(base64.b64decode(DUMMY_PNG_B64))
        monkeypatch.setattr("generate_image._find_latest_codex_image", lambda since: fake)
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        out_dir = tmp_path / "out"
        result = generate_image(
            prompt="hi",
            backend="codex",
            output_dir=str(out_dir),
            output_format="png",
            output_name="hero",
        )
        assert result is not None
        copied = out_dir / "hero.png"
        assert copied.exists()
        assert copied.read_bytes() == fake.read_bytes()
        assert str(copied) == result

    @patch("generate_image.subprocess.run")
    def test_codex_metadata_records_backend_codex(
        self, mock_run, monkeypatch, tmp_path
    ):
        fake = tmp_path / "ig_x.png"
        fake.write_bytes(base64.b64decode(DUMMY_PNG_B64))
        monkeypatch.setattr("generate_image._find_latest_codex_image", lambda since: fake)
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        out_dir = tmp_path / "out"
        result = generate_image(
            prompt="x", backend="codex", output_dir=str(out_dir), output_name="z"
        )
        meta_path = Path(result + ".json")
        assert meta_path.exists()
        meta = json.loads(meta_path.read_text())
        assert meta["backend"] == "codex"
        assert meta["prompt"] == "x"

    @patch("generate_image.subprocess.run")
    def test_codex_returns_none_when_no_image_found(
        self, mock_run, monkeypatch, tmp_path
    ):
        monkeypatch.setattr("generate_image._find_latest_codex_image", lambda since: None)
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")
        result = generate_image(
            prompt="x", backend="codex", output_dir=str(tmp_path / "out")
        )
        assert result is None

    @patch("generate_image.subprocess.run")
    def test_codex_returns_none_when_subprocess_nonzero(
        self, mock_run, monkeypatch, tmp_path
    ):
        mock_run.return_value = Mock(returncode=1, stdout="", stderr="boom")
        result = generate_image(
            prompt="x", backend="codex", output_dir=str(tmp_path / "out")
        )
        assert result is None


class TestBackendDispatch:
    """auto / api / codex 切替時に正しい経路に行くか"""

    @patch("generate_image.subprocess.run")
    @patch("generate_image.OpenAI")
    def test_explicit_codex_does_not_call_openai(
        self, mock_openai_cls, mock_run, monkeypatch, tmp_path
    ):
        fake = tmp_path / "ig_x.png"
        fake.write_bytes(base64.b64decode(DUMMY_PNG_B64))
        monkeypatch.setattr("generate_image._find_latest_codex_image", lambda since: fake)
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")
        generate_image(
            prompt="x", backend="codex", output_dir=str(tmp_path / "out")
        )
        mock_openai_cls.assert_not_called()

    @patch("generate_image.subprocess.run")
    @patch("generate_image.OpenAI")
    def test_explicit_api_does_not_call_codex(
        self, mock_openai_cls, mock_run, tmp_path
    ):
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.generate.return_value = _make_image_response()
        generate_image(
            prompt="x", backend="api", output_dir=str(tmp_path / "out")
        )
        mock_run.assert_not_called()
        client.images.generate.assert_called_once()

    @patch("generate_image.subprocess.run")
    @patch("generate_image.OpenAI")
    def test_auto_with_codex_available_uses_codex_first(
        self, mock_openai_cls, mock_run, monkeypatch, tmp_path
    ):
        monkeypatch.setattr("generate_image._codex_subscription_available", lambda: True)
        fake = tmp_path / "ig_x.png"
        fake.write_bytes(base64.b64decode(DUMMY_PNG_B64))
        monkeypatch.setattr("generate_image._find_latest_codex_image", lambda since: fake)
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        generate_image(
            prompt="x", backend="auto", output_dir=str(tmp_path / "out")
        )
        mock_run.assert_called_once()
        mock_openai_cls.assert_not_called()


class TestBackendFallback:
    """Codex が失敗したら API にフォールバック(auto モードかつ key あり)"""

    @patch("generate_image.subprocess.run")
    @patch("generate_image.OpenAI")
    def test_auto_falls_back_to_api_when_codex_fails(
        self, mock_openai_cls, mock_run, monkeypatch, tmp_path, capsys
    ):
        monkeypatch.setattr("generate_image._codex_subscription_available", lambda: True)
        monkeypatch.setattr("generate_image._find_latest_codex_image", lambda since: None)
        mock_run.return_value = Mock(returncode=1, stdout="", stderr="rate limit")
        client = Mock()
        mock_openai_cls.return_value = client
        client.images.generate.return_value = _make_image_response()

        result = generate_image(
            prompt="x", backend="auto", output_dir=str(tmp_path / "out")
        )
        assert result is not None
        client.images.generate.assert_called_once()
        out = capsys.readouterr().out
        assert "fallback" in out.lower() or "フォールバック" in out

    @patch("generate_image.subprocess.run")
    @patch("generate_image.OpenAI")
    def test_explicit_codex_does_not_fallback(
        self, mock_openai_cls, mock_run, monkeypatch, tmp_path
    ):
        """`--backend codex` 明示時はフォールバックしない(意図的選択を尊重)"""
        monkeypatch.setattr("generate_image._find_latest_codex_image", lambda since: None)
        mock_run.return_value = Mock(returncode=1, stdout="", stderr="boom")
        result = generate_image(
            prompt="x", backend="codex", output_dir=str(tmp_path / "out")
        )
        assert result is None
        mock_openai_cls.assert_not_called()
