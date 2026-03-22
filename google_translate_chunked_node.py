"""
Google Translate Chunked Node for ComfyUI
Translates long texts with automatic chunking support.
"""

import os
import requests
import json
from server import PromptServer
from aiohttp import web

try:
    from googletrans import Translator, LANGUAGES
except ImportError:
    print("[GoogleTranslateChunked] Error: googletrans not installed. Install with: pip install googletrans==4.0.0-rc1")
    Translator = None
    LANGUAGES = {"en": "english", "ru": "russian"}


# ===== Global Settings =====
translator = Translator() if Translator else None
google_translation_key = os.environ.get("GOOGLE_TRANSLATION_API_KEY")

# Maximum chunk size for translation (Google Translate limit)
MAX_CHUNK_SIZE = int(os.environ.get("GOOGLE_TRANSLATE_CHUNK_SIZE", 4999))


def split_text_into_chunks(text, max_chunk_size=MAX_CHUNK_SIZE):
    """
    Split long text into chunks at sentence or word boundaries.
    """
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    remaining_text = text

    while len(remaining_text) > max_chunk_size:
        chunk_end = max_chunk_size

        # Priority: break at sentence boundary
        sentence_breakers = ['. ', '! ', '? ', '.\n', '!\n', '?\n', '\n\n', '\n']
        best_break = -1

        for breaker in sentence_breakers:
            pos = remaining_text.rfind(breaker, 0, max_chunk_size)
            if pos > best_break:
                best_break = pos + len(breaker)

        if best_break > max_chunk_size // 2:
            chunk_end = best_break
        else:
            space_pos = remaining_text.rfind(' ', 0, max_chunk_size)
            if space_pos > max_chunk_size // 2:
                chunk_end = space_pos + 1
            else:
                chunk_end = max_chunk_size

        chunk = remaining_text[:chunk_end].strip()
        if chunk:
            chunks.append(chunk)
        remaining_text = remaining_text[chunk_end:].strip()

    if remaining_text:
        chunks.append(remaining_text)

    return chunks


def translate_single_chunk(prompt, srcTrans="auto", toTrans="en"):
    """Translate a single chunk of text."""
    if not prompt or prompt.strip() == "":
        return ""

    if not google_translation_key:
        if translator is None:
            print("[GoogleTranslateChunked] Warning: Translator not available")
            return prompt
        result = translator.translate(prompt, src=srcTrans, dest=toTrans)
        return result.text if hasattr(result, "text") else ""
    else:
        result = TranslationResult.translate_by_key(prompt, src=srcTrans, dest=toTrans)
        return result.text if hasattr(result, "text") else ""


def translate(prompt, srcTrans=None, toTrans=None, max_chunk_size=MAX_CHUNK_SIZE):
    """Translate text with automatic chunking."""
    if not srcTrans:
        srcTrans = "auto"
    if not toTrans:
        toTrans = "en"
    if not prompt or prompt.strip() == "":
        return ""

    if len(prompt) <= max_chunk_size:
        return translate_single_chunk(prompt, srcTrans, toTrans)

    print(f"[GoogleTranslateChunked] Text length: {len(prompt)} chars, splitting into chunks...")
    chunks = split_text_into_chunks(prompt, max_chunk_size)
    print(f"[GoogleTranslateChunked] Split into {len(chunks)} chunks")

    translated_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"[GoogleTranslateChunked] Translating chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")
        try:
            translated = translate_single_chunk(chunk, srcTrans, toTrans)
            translated_chunks.append(translated)
        except Exception as e:
            print(f"[GoogleTranslateChunked] Error translating chunk {i+1}: {e}")
            translated_chunks.append(chunk)

    result = " ".join(translated_chunks)
    print(f"[GoogleTranslateChunked] Translation complete, result length: {len(result)} chars")
    return result


class TranslationResult:
    def __init__(self, text=""):
        self.text = text

    @staticmethod
    def translate_by_key(text, src, dest):
        url = f"https://translation.googleapis.com/language/translate/v2?key={google_translation_key}"
        data = {"q": text, "target": dest}
        try:
            resp = requests.post(url, data=data)
            resp_data = json.loads(resp.text)
            if "translations" in resp_data.get("data", {}):
                translations = resp_data["data"]["translations"]
                if translations:
                    return TranslationResult(translations[0]["translatedText"])
        except Exception as e:
            print(f"[GoogleTranslateChunked] API key translation error: {e}")
        return TranslationResult("")


@PromptServer.instance.routes.post("/google_translate_chunked/translate_manual")
async def translate_manual(request):
    json_data = await request.json()
    prompt = json_data.get("prompt", "")
    if "prompt" in json_data and "srcTrans" in json_data and "toTrans" in json_data:
        srcTrans = json_data.get("srcTrans")
        toTrans = json_data.get("toTrans")
        translate_text_prompt = translate(prompt, srcTrans, toTrans)
        return web.json_response({"translate_prompt": translate_text_prompt})
    return web.json_response({"translate_prompt": prompt})


class GoogleTranslateChunkedNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "placeholder": "Enter text to translate"}),
                "from_translate": (["auto"] + list(LANGUAGES.keys()), {"default": "auto"}),
                "to_translate": (list(LANGUAGES.keys()), {"default": "en"}),
            },
            "optional": {
                "manual_translate": ("BOOLEAN", {"default": False}),
                "chunk_size": ("INT", {"default": MAX_CHUNK_SIZE, "min": 100, "max": 10000}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("translated_text",)
    FUNCTION = "translate_text"
    CATEGORY = "text/translate"
    DESCRIPTION = "Translate text with automatic chunking for long texts."

    def translate_text(self, text, from_translate="auto", to_translate="en", manual_translate=False, chunk_size=MAX_CHUNK_SIZE):
        if manual_translate:
            return (text,)
        translated = translate(text, from_translate, to_translate, chunk_size)
        return (translated,)


class GoogleTranslateChunkedCLIPTextEncodeNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "placeholder": "Enter text to translate"}),
                "from_translate": (["auto"] + list(LANGUAGES.keys()), {"default": "auto"}),
                "to_translate": (list(LANGUAGES.keys()), {"default": "en"}),
                "clip": ("CLIP",),
            },
            "optional": {
                "manual_translate": ("BOOLEAN", {"default": False}),
                "chunk_size": ("INT", {"default": MAX_CHUNK_SIZE, "min": 100, "max": 10000}),
            }
        }

    RETURN_TYPES = ("CONDITIONING", "STRING")
    RETURN_NAMES = ("conditioning", "translated_text")
    FUNCTION = "translate_text"
    CATEGORY = "conditioning/translate"
    DESCRIPTION = "Translate and encode text with CLIP."

    def translate_text(self, text, from_translate, to_translate, clip, manual_translate=False, chunk_size=MAX_CHUNK_SIZE):
        if manual_translate:
            translated = text
        else:
            translated = translate(text, from_translate, to_translate, chunk_size)
        tokens = clip.tokenize(translated)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]], translated)


NODE_CLASS_MAPPINGS = {
    "GoogleTranslateChunkedNode": GoogleTranslateChunkedNode,
    "GoogleTranslateChunkedCLIPTextEncodeNode": GoogleTranslateChunkedCLIPTextEncodeNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GoogleTranslateChunkedNode": "Google Translate Chunked",
    "GoogleTranslateChunkedCLIPTextEncodeNode": "Google Translate Chunked (CLIP)",
}
