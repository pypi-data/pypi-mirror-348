# Posturner - Universal POS Tag Converter

Posturner is a Python tool for converting language-specific part-of-speech (POS) tags to universal POS tags. It supports multiple languages through mapping files.

## Features

- Convert POS tags from various languages to universal POS tags
- Support for multiple languages through mapping files
- Simple Python API for integration with NLP pipelines
- Includes a comprehensive multi-language mapping file

## Installation

```bash
pip install posturner
```

## Usage

### Basic Usage
```python
from posturner import trans_universal_pos

# Convert a language-specific POS tag to universal POS
print(trans_universal_pos("nimisõna"))  # Output: NOUN
print(trans_universal_pos("tegusõna"))  # Output: VERB
print(trans_universal_pos("名词"))      # Output: NOUN
```

### Supported Languages
Posturner currently supports conversion for:
- Estonian (et)
- English (en)
- Chinese (zh)
- Japanese (ja)
- Urdu (ur)

Example conversions:
- nimisõna(et) → NOUN
- tegusõna(et) → VERB
- noun(en) → NOUN
- 名词(zh) → NOUN
- 動詞(ja) → VERB
- اسم(ur) → NOUN

## Advanced Usage

You can use your own mapping files by placing them in the posturner directory:
```python
from posturner.set import pos_set

# Add custom mappings
pos_set["my_custom_tag"] = "NOUN"
```

## Contributing

Contributions are welcome! Please submit pull requests with:
- New language mappings
- Bug fixes
- Documentation improvements

## License

MIT License - See LICENSE file for details.

