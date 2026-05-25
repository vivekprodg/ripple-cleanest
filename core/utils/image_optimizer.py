from __future__ import annotations

import io
import logging
import os
from dataclasses import dataclass
from typing import BinaryIO, Optional, Tuple

from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError

logger = logging.getLogger(__name__)

DEFAULT_MAX_BYTES = int(os.getenv("IMAGE_OPTIMIZER_MAX_BYTES", "1000000"))
DEFAULT_START_QUALITY = int(os.getenv("IMAGE_OPTIMIZER_START_QUALITY", "92"))
DEFAULT_MIN_QUALITY = int(os.getenv("IMAGE_OPTIMIZER_MIN_QUALITY", "45"))
DEFAULT_QUALITY_STEP = int(os.getenv("IMAGE_OPTIMIZER_QUALITY_STEP", "5"))
DEFAULT_MIN_DIMENSION = int(os.getenv("IMAGE_OPTIMIZER_MIN_DIMENSION", "640"))
DEFAULT_RESIZE_FACTOR = float(os.getenv("IMAGE_OPTIMIZER_RESIZE_FACTOR", "0.90"))

IMAGE_OPTIMIZER_READY = False


@dataclass(frozen=True)
class OptimizationResult:
    content: bytes
    filename: str
    format: str
    size_bytes: int


def initialize_image_optimizer() -> dict:
    """
    Lightweight app-start hook used by apps.py.
    """
    global IMAGE_OPTIMIZER_READY
    IMAGE_OPTIMIZER_READY = True

    return {
        "ready": IMAGE_OPTIMIZER_READY,
        "max_bytes": DEFAULT_MAX_BYTES,
        "start_quality": DEFAULT_START_QUALITY,
        "min_quality": DEFAULT_MIN_QUALITY,
        "quality_step": DEFAULT_QUALITY_STEP,
        "min_dimension": DEFAULT_MIN_DIMENSION,
        "resize_factor": DEFAULT_RESIZE_FACTOR,
    }


def _read_bytes(source: bytes | bytearray | memoryview | BinaryIO | ContentFile) -> bytes:
    if isinstance(source, (bytes, bytearray, memoryview)):
        return bytes(source)

    if hasattr(source, "read"):
        current_pos = None
        try:
            if hasattr(source, "tell"):
                current_pos = source.tell()
        except Exception:
            current_pos = None

        data = source.read()

        try:
            if current_pos is not None and hasattr(source, "seek"):
                source.seek(current_pos)
        except Exception:
            pass

        return data

    raise TypeError("Unsupported image source type.")


def _guess_extension(filename: Optional[str], image_format: str) -> str:
    if filename:
        _, ext = os.path.splitext(filename)
        if ext:
            return ext.lower()

    fmt = (image_format or "").upper()
    if fmt in {"JPEG", "JPG"}:
        return ".jpg"
    if fmt == "PNG":
        return ".png"
    if fmt == "WEBP":
        return ".webp"
    if fmt == "GIF":
        return ".gif"
    if fmt == "TIFF":
        return ".tif"
    return ".jpg"


def _guess_output_format(original_format: str, has_alpha: bool, preserve_original_format: bool) -> str:
    fmt = (original_format or "").upper()

    if preserve_original_format and fmt in {"JPEG", "JPG", "PNG", "WEBP"}:
        return "JPEG" if fmt == "JPG" else fmt

    if has_alpha:
        return "PNG"

    return "JPEG"


def _has_alpha(image: Image.Image) -> bool:
    if image.mode in ("RGBA", "LA"):
        return True
    if image.mode == "P" and "transparency" in image.info:
        return True
    return False


def _prepare_for_format(image: Image.Image, output_format: str) -> Image.Image:
    img = image.copy()

    if output_format.upper() == "JPEG":
        if img.mode not in ("RGB", "L"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                alpha = img.convert("RGBA")
                background.paste(alpha, mask=alpha.split()[-1])
                img = background
            else:
                img = img.convert("RGB")
        elif img.mode == "L":
            img = img.convert("RGB")

    elif output_format.upper() in {"PNG", "WEBP"}:
        if img.mode in {"P", "CMYK", "LA"}:
            img = img.convert("RGBA")

    return img


def _save_image_bytes(image: Image.Image, output_format: str, quality: int) -> bytes:
    buffer = io.BytesIO()
    fmt = output_format.upper()

    save_kwargs = {"optimize": True}

    if fmt == "JPEG":
        save_kwargs.update(
            quality=max(1, min(95, quality)),
            progressive=True,
        )
        image.save(buffer, format="JPEG", **save_kwargs)

    elif fmt == "WEBP":
        save_kwargs.update(
            quality=max(1, min(95, quality)),
            method=6,
        )
        image.save(buffer, format="WEBP", **save_kwargs)

    elif fmt == "PNG":
        save_kwargs.update(
            compress_level=9,
        )
        image.save(buffer, format="PNG", **save_kwargs)

    else:
        save_kwargs.update(
            quality=max(1, min(95, quality)),
        )
        image.save(buffer, format=fmt, **save_kwargs)

    return buffer.getvalue()


def _resize_image(image: Image.Image, factor: float, min_dimension: int) -> Image.Image:
    width, height = image.size
    largest_side = max(width, height)

    if largest_side <= min_dimension:
        return image.copy()

    new_width = max(min_dimension, int(width * factor))
    new_height = max(min_dimension, int(height * factor))

    resized = image.copy()
    resized.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)
    return resized


def _candidate_quality_values(start_quality: int, min_quality: int, step: int) -> list[int]:
    values = []
    q = start_quality
    while q >= min_quality:
        values.append(q)
        q -= step
    if values and values[-1] != min_quality:
        values.append(min_quality)
    elif not values:
        values.append(min_quality)
    return values


def optimize_pil_image(
    image: Image.Image,
    *,
    filename: Optional[str] = None,
    max_bytes: int = DEFAULT_MAX_BYTES,
    preserve_original_format: bool = True,
    allow_webp_fallback: bool = True,
) -> OptimizationResult:
    """
    Optimize a PIL image to stay at or below max_bytes.

    This function is defensive:
    - it never raises for typical optimization failures
    - it falls back to a safe save path
    - it preserves the upload flow by returning best-effort output
    """
    if image is None:
        raise ValueError("image is required")

    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        logger.exception("EXIF transpose failed; continuing with original image.")

    original_format = (image.format or "").upper()
    has_alpha = _has_alpha(image)
    output_format = _guess_output_format(original_format, has_alpha, preserve_original_format)

    try:
        if getattr(image, "is_animated", False) and getattr(image, "n_frames", 1) > 1:
            data = _save_image_bytes(_prepare_for_format(image, output_format), output_format, DEFAULT_START_QUALITY)
            ext = _guess_extension(filename, output_format)
            return OptimizationResult(
                content=data,
                filename=f"{os.path.splitext(filename or 'image')[0]}{ext}",
                format=output_format,
                size_bytes=len(data),
            )
    except Exception:
        logger.exception("Animated image handling failed; falling back to normal optimization.")

    candidate_formats = []
    if output_format in {"JPEG", "PNG", "WEBP"}:
        candidate_formats.append(output_format)

    if allow_webp_fallback and "WEBP" not in candidate_formats:
        candidate_formats.append("WEBP")

    if "JPEG" not in candidate_formats and not has_alpha:
        candidate_formats.append("JPEG")

    if "PNG" not in candidate_formats and has_alpha:
        candidate_formats.append("PNG")

    if not candidate_formats:
        candidate_formats = ["JPEG"]

    if original_format in {"GIF", "BMP", "TIFF"}:
        if has_alpha:
            candidate_formats = ["PNG", "WEBP"] if allow_webp_fallback else ["PNG"]
        else:
            candidate_formats = ["JPEG", "WEBP"] if allow_webp_fallback else ["JPEG"]

    quality_values = _candidate_quality_values(
        DEFAULT_START_QUALITY,
        DEFAULT_MIN_QUALITY,
        DEFAULT_QUALITY_STEP,
    )

    current = image.copy()
    best_data: Optional[bytes] = None
    best_format = candidate_formats[0]
    best_size = 0

    try:
        for fmt in candidate_formats:
            working = _prepare_for_format(current, fmt)

            while True:
                if fmt == "PNG":
                    data = _save_image_bytes(working, fmt, DEFAULT_START_QUALITY)
                    size = len(data)

                    if best_data is None or size < best_size:
                        best_data = data
                        best_format = fmt
                        best_size = size

                    if size <= max_bytes:
                        ext = _guess_extension(filename, fmt)
                        return OptimizationResult(
                            content=data,
                            filename=f"{os.path.splitext(filename or 'image')[0]}{ext}",
                            format=fmt,
                            size_bytes=size,
                        )

                    resized = _resize_image(working, DEFAULT_RESIZE_FACTOR, DEFAULT_MIN_DIMENSION)
                    if resized.size == working.size:
                        break
                    working = resized
                    continue

                for quality in quality_values:
                    data = _save_image_bytes(working, fmt, quality)
                    size = len(data)

                    if best_data is None or size < best_size:
                        best_data = data
                        best_format = fmt
                        best_size = size

                    if size <= max_bytes:
                        ext = _guess_extension(filename, fmt)
                        return OptimizationResult(
                            content=data,
                            filename=f"{os.path.splitext(filename or 'image')[0]}{ext}",
                            format=fmt,
                            size_bytes=size,
                        )

                resized = _resize_image(working, DEFAULT_RESIZE_FACTOR, DEFAULT_MIN_DIMENSION)
                if resized.size == working.size:
                    break
                working = resized

    except Exception:
        logger.exception("Image optimization failed; falling back to original bytes.")

        raw = _read_bytes(image.fp) if hasattr(image, "fp") and image.fp else b""
        if raw:
            ext = _guess_extension(filename, original_format or "JPEG")
            return OptimizationResult(
                content=raw,
                filename=f"{os.path.splitext(filename or 'image')[0]}{ext}",
                format=original_format or "JPEG",
                size_bytes=len(raw),
            )

    if best_data is None:
        try:
            fallback_fmt = candidate_formats[0]
            fallback_img = _prepare_for_format(current, fallback_fmt)
            best_data = _save_image_bytes(fallback_img, fallback_fmt, DEFAULT_MIN_QUALITY)
            best_format = fallback_fmt
            best_size = len(best_data)
        except Exception:
            logger.exception("Final optimization fallback failed; returning original bytes.")
            raw = _read_bytes(image.fp) if hasattr(image, "fp") and image.fp else b""
            ext = _guess_extension(filename, original_format or "JPEG")
            return OptimizationResult(
                content=raw,
                filename=f"{os.path.splitext(filename or 'image')[0]}{ext}",
                format=original_format or "JPEG",
                size_bytes=len(raw),
            )

    ext = _guess_extension(filename, best_format)
    return OptimizationResult(
        content=best_data,
        filename=f"{os.path.splitext(filename or 'image')[0]}{ext}",
        format=best_format,
        size_bytes=best_size,
    )


def optimize_uploaded_image(
    uploaded_file,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    preserve_original_format: bool = True,
    allow_webp_fallback: bool = True,
) -> ContentFile:
    """
    Optimize a Django/Wagtail uploaded file and return a ContentFile.

    Hard rule:
    - never raise because of optimization failure
    - return original bytes unchanged if anything goes wrong
    """
    raw = _read_bytes(uploaded_file)
    filename = getattr(uploaded_file, "name", None)

    try:
        with Image.open(io.BytesIO(raw)) as img:
            result = optimize_pil_image(
                img,
                filename=filename,
                max_bytes=max_bytes,
                preserve_original_format=preserve_original_format,
                allow_webp_fallback=allow_webp_fallback,
            )
            return ContentFile(result.content, name=result.filename)

    except UnidentifiedImageError:
        return ContentFile(raw, name=filename or "upload.bin")

    except Exception:
        logger.exception("Uploaded image optimization failed; returning original upload unchanged.")
        return ContentFile(raw, name=filename or "upload.bin")


def optimize_image_file(
    file_or_bytes,
    *,
    filename: Optional[str] = None,
    max_bytes: int = DEFAULT_MAX_BYTES,
    preserve_original_format: bool = True,
    allow_webp_fallback: bool = True,
) -> Tuple[bytes, str]:
    """
    Convenience wrapper that returns (optimized_bytes, optimized_filename).
    """
    raw = _read_bytes(file_or_bytes)
    safe_filename = filename or getattr(file_or_bytes, "name", None) or "image"

    try:
        with Image.open(io.BytesIO(raw)) as img:
            result = optimize_pil_image(
                img,
                filename=safe_filename,
                max_bytes=max_bytes,
                preserve_original_format=preserve_original_format,
                allow_webp_fallback=allow_webp_fallback,
            )
            return result.content, result.filename

    except UnidentifiedImageError:
        return raw, safe_filename

    except Exception:
        logger.exception("File optimization failed; returning original bytes unchanged.")
        return raw, safe_filename