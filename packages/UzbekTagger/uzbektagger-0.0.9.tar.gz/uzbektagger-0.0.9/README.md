# UzbekTagger

**UzbekTagger** is a part-of-speech (POS) tagging library for text in the Uzbek language. This library allows you to automatically assign grammatical categories (such as noun, verb, adjective, etc.) to each word in a given text.

##  Features

- Tokenizes and tags Uzbek sentences with grammatical categories
- Supports basic POS tagging (NOUN, VERB, ADJ, PRON, etc.)
- Simple and lightweight interface

##  Installation

You can install the library using pip:

```
pip install UzbekTagger
```

## Example
```
from UzbekTagger import UzbekTagger as tg

print(tg.pos("Men bugun uyga ertaroq ketdim. Boshqa bolalar bugun maktabdan kech kelar emish."))
```
