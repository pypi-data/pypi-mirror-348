# UzbekTagger

**UzbekTagger** is a part-of-speech (POS) tagging library for text in the Uzbek language. This library allows you to automatically assign grammatical categories (such as noun, verb, adjective, etc.) to each word in a given text.

### Article: [UzbekTagger: The rule-based POS tagger for Uzbek language](https://www.researchgate.net/publication/370418960_UzbekTagger_The_rule-based_POS_tagger_for_Uzbek_language)
### GitHub link:  https://github.com/MaksudSharipov/UzbekTagger

##  Features

- Tokenizes and tags Uzbek sentences with grammatical categories
- Supports basic POS tagging (NOUN, VERB, ADJ, PRON, etc.)
- Simple and lightweight interface

##  Installation:

You can install the library using pip:

```python
pip install UzbekTagger
```

## Example:
```python

from UzbekTagger import pos

print(pos.tagger("Men bugun uyga ertaroq ketdim. Boshqa bolalar bugun maktabdan kechroq kelar ekan."))

```

## Result:

```python 
 Men/PRON bugun/ADV uyga/NOUN ertaroq/ADV ketdim/VERB ./PUNCT

 Boshqa/ADV bolalar/NOUN bugun/ADV maktabdan/NOUN kechroq/VERB kelar ekan/VERB ./PUNCT
```