# ComfyUI Google Translate Chunked Node

**Quick Links / Быстрые ссылки / 快速链接:**
- [🇷🇺 Русский](#-русский)
- [🇨🇳 中文](#-中文)
- [🇬🇧 English](#-english)

---

## 🇷🇺 Русский

Кастомная нода ComfyUI для перевода длинных текстов с автоматическим разбиением на чанки.

### Возможности

- **Автоматическое разбиение**: Переводит тексты любой длины, автоматически разбивая их на части
- **Умное разбиение**: Разбивает текст по границам предложений, избегая разрыва слов
- **Два типа нод**:
  - `Google Translate Chunked` — Простой перевод текста
  - `Google Translate Chunked (CLIP)` — Перевод + CLIP-энкодинг для пайплайнов
- **Настраиваемый размер чанка**: Можно изменить максимальный размер части в каждой ноде
- **Обработка ошибок**: При ошибке перевода сохраняется оригинальный текст части
- **Логирование прогресса**: Видите ход перевода в консоли ComfyUI

### Установка

#### Способ 1: Ручная установка

1. Скачайте этот пакет
2. Распакуйте папку `ComfyUI_GoogleTranslate_Chunked` в директорию `custom_nodes` вашего ComfyUI:
   ```
   ComfyUI/
   └── custom_nodes/
       └── ComfyUI_GoogleTranslate_Chunked/
           ├── __init__.py
           ├── google_translate_chunked_node.py
           └── README.md
   ```
3. Перезапустите ComfyUI

#### Способ 2: Клонирование через Git

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YOUR_REPO/ComfyUI_GoogleTranslate_Chunked.git
```

#### Зависимости

Нода требует библиотеку `googletrans`. Если не установлена:

```bash
pip install googletrans==4.0.0-rc1
```

Или используя встроенный Python ComfyUI:
```bash
cd ComfyUI/python_embeded
python -m pip install googletrans==4.0.0-rc1
```

### Использование

#### Нода Google Translate Chunked

| Вход | Тип | Описание |
|------|-----|----------|
| text | STRING | Текст для перевода (любой длины) |
| from_translate | COMBO | Исходный язык (по умолчанию: автоопределение) |
| to_translate | COMBO | Целевой язык |
| manual_translate | BOOLEAN | Пропустить перевод если True |
| chunk_size | INT | Макс. символов в чанке (по умолчанию: 4999) |

#### Нода Google Translate Chunked (CLIP)

То же самое, плюс:
| Вход | Тип | Описание |
|------|-----|----------|
| clip | CLIP | CLIP модель для энкодинга текста |

| Выход | Тип | Описание |
|-------|-----|----------|
| conditioning | CONDITIONING | Закодированное условие |
| translated_text | STRING | Переведённый текст |

### Как это работает

1. **Проверка длины**: Если текст в пределах лимита чанка, переводится целиком
2. **Умное разбиение**: Для длинных текстов разбиение по границам предложений (`.`, `!`, `?`, переносы строк)
3. **Последовательный перевод**: Каждая часть переводится отдельно
4. **Конкатенация**: Результаты объединяются в один переведённый текст

### Вывод в консоли

При переводе длинных текстов вы увидите прогресс в консоли ComfyUI:

```
[GoogleTranslateChunked] Text length: 12500 chars, splitting into chunks...
[GoogleTranslateChunked] Split into 3 chunks (max 4999 chars each)
[GoogleTranslateChunked] Translating chunk 1/3 (4995 chars)...
[GoogleTranslateChunked] Translating chunk 2/3 (4998 chars)...
[GoogleTranslateChunked] Translating chunk 3/3 (2507 chars)...
[GoogleTranslateChunked] Translation complete, result length: 11200 chars
```

### Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `GOOGLE_TRANSLATION_API_KEY` | API ключ Google Cloud Translation (опционально) | None |
| `GOOGLE_TRANSLATE_CHUNK_SIZE` | Размер чанка по умолчанию | 4999 |

### Устранение неполадок

#### Ошибка "googletrans not installed"

```bash
pip install googletrans==4.0.0-rc1
```

#### Ошибки перевода

Нода использует неофициальный API Google Translate, который может иногда сбоить. Нода:
1. Запишет ошибку в консоль
2. Сохранит оригинальный текст для проблемного чанка
3. Продолжит перевод остальных частей

#### Ограничение частоты запросов

Для очень длинных текстов с большим количеством частей Google может временно ограничить запросы. Подождите несколько минут и попробуйте снова.

---

## 🇨🇳 中文

一个支持自动分块的ComfyUI自定义节点，用于翻译长文本。

### 功能特点

- **自动分块**：通过自动拆分文本，可翻译任意长度的文本
- **智能分割**：尽可能在句子边界处分割文本，避免截断单词
- **两种节点类型**：
  - `Google Translate Chunked` - 简单文本翻译
  - `Google Translate Chunked (CLIP)` - 翻译 + CLIP编码，用于工作流
- **可配置分块大小**：可在每个节点中调整最大分块大小
- **错误处理**：优雅地处理翻译错误，保留失败分块的原始文本
- **进度日志**：在ComfyUI控制台中查看翻译进度

### 安装方法

#### 方法1：手动安装

1. 下载此软件包
2. 将 `ComfyUI_GoogleTranslate_Chunked` 文件夹解压到您的ComfyUI `custom_nodes` 目录：
   ```
   ComfyUI/
   └── custom_nodes/
       └── ComfyUI_GoogleTranslate_Chunked/
           ├── __init__.py
           ├── google_translate_chunked_node.py
           └── README.md
   ```
3. 重启ComfyUI

#### 方法2：通过Git克隆

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YOUR_REPO/ComfyUI_GoogleTranslate_Chunked.git
```

#### 依赖要求

此节点需要 `googletrans` 库。如果未安装：

```bash
pip install googletrans==4.0.0-rc1
```

或使用ComfyUI内置Python：
```bash
cd ComfyUI/python_embeded
python -m pip install googletrans==4.0.0-rc1
```

### 使用方法

#### Google Translate Chunked 节点

| 输入 | 类型 | 描述 |
|------|------|------|
| text | STRING | 要翻译的文本（任意长度） |
| from_translate | COMBO | 源语言（默认：自动检测） |
| to_translate | COMBO | 目标语言 |
| manual_translate | BOOLEAN | 如果为True则跳过翻译 |
| chunk_size | INT | 每个分块的最大字符数（默认：4999） |

#### Google Translate Chunked (CLIP) 节点

同上，另外还有：
| 输入 | 类型 | 描述 |
|------|------|------|
| clip | CLIP | 用于文本编码的CLIP模型 |

| 输出 | 类型 | 描述 |
|------|------|------|
| conditioning | CONDITIONING | 编码后的条件 |
| translated_text | STRING | 翻译后的文本 |

### 工作原理

1. **长度检查**：如果文本在分块大小限制内，直接翻译
2. **智能分割**：对于较长的文本，在句子边界（`.`、`!`、`?`、换行符）处分割
3. **顺序翻译**：每个分块分别翻译
4. **合并结果**：结果拼接成一个完整的翻译文本

### 控制台输出

翻译长文本时，您将在ComfyUI控制台中看到进度：

```
[GoogleTranslateChunked] Text length: 12500 chars, splitting into chunks...
[GoogleTranslateChunked] Split into 3 chunks (max 4999 chars each)
[GoogleTranslateChunked] Translating chunk 1/3 (4995 chars)...
[GoogleTranslateChunked] Translating chunk 2/3 (4998 chars)...
[GoogleTranslateChunked] Translating chunk 3/3 (2507 chars)...
[GoogleTranslateChunked] Translation complete, result length: 11200 chars
```

### 环境变量

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `GOOGLE_TRANSLATION_API_KEY` | Google Cloud Translation API密钥（可选） | None |
| `GOOGLE_TRANSLATE_CHUNK_SIZE` | 默认分块大小 | 4999 |

### 故障排除

#### "googletrans not installed" 错误

```bash
pip install googletrans==4.0.0-rc1
```

#### 翻译错误

此节点使用非官方的Google Translate API，可能会偶尔失败。节点会：
1. 在控制台记录错误
2. 保留该分块的原始文本
3. 继续翻译剩余分块

#### 频率限制

对于包含多个分块的非常长的文本，Google可能会临时限制请求。请等待几分钟后重试。

---

## 🇬🇧 English

A custom ComfyUI node for translating long texts with automatic chunking support.

### Features

- **Automatic Chunking**: Translates texts of any length by automatically splitting them into chunks
- **Smart Splitting**: Breaks text at sentence boundaries when possible, avoiding mid-word cuts
- **Two Node Types**:
  - `Google Translate Chunked` - Simple text translation
  - `Google Translate Chunked (CLIP)` - Translation + CLIP encoding for pipelines
- **Configurable Chunk Size**: Adjust the maximum chunk size per node
- **Error Handling**: Gracefully handles translation errors, preserving original text for failed chunks
- **Progress Logging**: See translation progress in the ComfyUI console

### Installation

#### Method 1: Manual Installation

1. Download this package
2. Extract/copy the `ComfyUI_GoogleTranslate_Chunked` folder to your ComfyUI `custom_nodes` directory:
   ```
   ComfyUI/
   └── custom_nodes/
       └── ComfyUI_GoogleTranslate_Chunked/
           ├── __init__.py
           ├── google_translate_chunked_node.py
           └── README.md
   ```
3. Restart ComfyUI

#### Method 2: Clone via Git

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YOUR_REPO/ComfyUI_GoogleTranslate_Chunked.git
```

#### Requirements

The node requires the `googletrans` library. If not installed:

```bash
pip install googletrans==4.0.0-rc1
```

Or using ComfyUI's embedded Python:
```bash
cd ComfyUI/python_embeded
python -m pip install googletrans==4.0.0-rc1
```

### Usage

#### Google Translate Chunked Node

| Input | Type | Description |
|-------|------|-------------|
| text | STRING | Text to translate (any length) |
| from_translate | COMBO | Source language (default: auto-detect) |
| to_translate | COMBO | Target language |
| manual_translate | BOOLEAN | Skip translation if True |
| chunk_size | INT | Max characters per chunk (default: 4999) |

#### Google Translate Chunked (CLIP) Node

Same as above, plus:
| Input | Type | Description |
|-------|------|-------------|
| clip | CLIP | CLIP model for text encoding |

| Output | Type | Description |
|--------|------|-------------|
| conditioning | CONDITIONING | Encoded conditioning |
| translated_text | STRING | Translated text |

### How It Works

1. **Length Check**: If text is within chunk size limit, translate directly
2. **Smart Split**: For longer texts, split at sentence boundaries (`.`, `!`, `?`, newlines)
3. **Sequential Translation**: Each chunk is translated separately
4. **Concatenation**: Results are joined back into a single translated text

### Console Output

When translating long texts, you'll see progress in the ComfyUI console:

```
[GoogleTranslateChunked] Text length: 12500 chars, splitting into chunks...
[GoogleTranslateChunked] Split into 3 chunks (max 4999 chars each)
[GoogleTranslateChunked] Translating chunk 1/3 (4995 chars)...
[GoogleTranslateChunked] Translating chunk 2/3 (4998 chars)...
[GoogleTranslateChunked] Translating chunk 3/3 (2507 chars)...
[GoogleTranslateChunked] Translation complete, result length: 11200 chars
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_TRANSLATION_API_KEY` | Google Cloud Translation API key (optional) | None |
| `GOOGLE_TRANSLATE_CHUNK_SIZE` | Default chunk size | 4999 |

### Troubleshooting

#### "googletrans not installed" error

```bash
pip install googletrans==4.0.0-rc1
```

#### Translation errors

The node uses the unofficial Google Translate API which may occasionally fail. The node will:
1. Log the error in the console
2. Keep the original text for that chunk
3. Continue with remaining chunks

#### Rate limiting

For very long texts with many chunks, Google may temporarily rate-limit requests. Wait a few minutes and try again.

