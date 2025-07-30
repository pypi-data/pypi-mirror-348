import xml.etree.ElementTree as et
from pathlib import Path
import nltk.tokenize
from nltk.tokenize import RegexpTokenizer

class service_to_uzbek_text:

    def text_normalizer(text):
        # text=text.lower()
        text = text.replace("'", "‘")
        text = text.replace("`", "‘")
        text = text.replace("‘", "‘")
        text = text.replace("‘", "‘")
        text = text.replace("‘", "‘")
        text = text.replace("’", "‘")
        solid_sign = ["sun‘iy", "sur‘at", "jur‘at", "sa‘y"]
        for x in solid_sign:
            if (x in text):
                new_x = x.replace("‘", "ʼ")
                text = text.replace(x, new_x)
        return text

    def word_normalizer(word):
        word = word.lower()
        word = word.strip()
        word = word.replace("'", "‘")
        word = word.replace("`", "‘")
        word = word.replace("‘", "‘")
        word = word.replace("‘", "‘")
        word = word.replace("‘", "‘")
        word = word.replace("’", "‘")
        solid_sign = ["sun‘iy", "sur‘at", "jur‘at", "sa‘y"]
        for x in solid_sign:
            if (x in word):
                new_x = x.replace("‘", "ʼ")

        return word

    def word_tokenizer(text):
        text = service_to_uzbek_text.text_normalizer(text)
        tokenize = RegexpTokenizer("[\w`'‘‘‘’‘-]+")
        tokens = tokenize.tokenize(text)
        return tokens

    def sent_tokenizer(text):
        sent = nltk.tokenize.sent_tokenize(text)
        return sent

class pos:
    __this_directory = Path(__file__).parent
    #__dir = __this_directory.joinpath('words.xml')
    __tree = et.parse(__this_directory/"word.xml")
    __root = __tree.getroot()

    def __double_words(a):

        a = list(a)
        verb = ["edi", "ekan", "emish","kerak"]
        l1 = len(a)
        l2 = len(verb)
        i = 0
        while (i < l1 - 1):
            for j in range(l2):
                if (a[i + 1]["word"] == verb[j]):
                    b = True
                    if ((a[i]["root"] == "null") and (a[i + 1]["root"] == "null")):
                        a[i]["root"] = a[i]["word"] + " " + a[i + 1]["word"]
                    elif (a[i]["root"] == "null"):
                        a[i]["root"] = a[i]["word"] + " " + a[i + 1]["root"]
                    elif (a[i + 1]["root"] == "null"):
                        a[i]["root"] = a[i]["root"] + " " + a[i + 1]["word"]
                    else:
                        a[i]["root"] = a[i]["root"] + " " + a[i + 1]["root"]

                    a[i]["word"] = a[i]["word"] + " " + a[i + 1]["word"]
                    a[i]["pos"] = "VERB"
                    #print(a[i])
                    a.pop(i + 1)
                    i = i - 1
                    l1 = len(a)
            i = i + 1

        return a

    def __check_with_affix(a):
        #a = list(a)
        verb = ['di', 'lan','lash','lashtir','lantir']
        noun = ['lig', 'lik', 'vchi','ga','ka','qa','dan']
        for v in verb:
            if (v in a["affix"]):
                if (a['pos'] == 'VERB'):
                    break
                else:
                    a['pos'] = 'VERB'
        for v in noun:
            if (v in a["affix"]):
                if (a['pos'] == 'NOUN'):
                    break
                else:
                    a['pos'] = 'NOUN'
        return a

    def __tag_word(a, root):

        if (str(a['word']).isdigit()):
            a['pos'] = 'NUM'
            a['root'] = a['word']
            return a

        a = dict(a)
        for dic in root:
            s = dic.text
            if ((dic.attrib["classId"] == "VERB") and ("moq" in s[-3:])):
                s = str(dic.text[:-3])
            s = service_to_uzbek_text.word_normalizer(s)

            l = len(s)
            if ((s == a["word"][:l].lower()) and (len(s) > 1) or (s == a["word"][:l].lower()) and (s == 'u')):
                if (a['root'] == "null"):
                    a["pos"] = str(dic.attrib["classId"])
                    a["root"] = s
                    a["affix"] = a["word"][l:]
                elif (l > len(a["root"])):
                    a["pos"] = str(dic.attrib["classId"])
                    a["root"] = s
                    a["affix"] = a["word"][l:]
        return a

    def __check_with_lar(a, root):
        if(len(a['affix'])==0):
            return a

        if (str(a['root'])[-2:] == 'la') and (str(a['affix'])[0] == 'r'):
            b = {'word': a['root'][:-1], 'pos': "null", 'root': 'null', 'affix': 'null'}
            b = pos.__tag_word(b, root)
            if not (b['root'] == 'null'):
                a['pos'] = b['pos']
                a['root'] = b['root']
                a['affix'] = b['affix'] + 'a' + a['affix']
        return a

    # print(__check_with_lar({'word':'vakillari','pos':'fel','root':'vakilla', 'affix':'ri'},root))

    def __tag(tokens, root):

        a = []

        for token in tokens:
            a.append({'word': str(token), "pos": "null", "root": "null", "affix": "null"})

        for i in range(len(a)):
            a[i] = pos.__tag_word(a[i], root)
            a[i]=pos.__check_with_lar(a[i],root)
            a[i]=pos.__check_with_affix(a[i])
        a = pos.__double_words(a)
        #print(a)

        return a

    def tagger(text):

        tagged_text=""
        sentences = service_to_uzbek_text.sent_tokenizer(text)
        for sent in sentences:
            punk=sent[-1]
            if not(punk in '.!?'):
                punk='.'
            tagged_sent=""
            tokens = service_to_uzbek_text.word_tokenizer(sent)
            tagged_list=pos.__tag(tokens,pos.__root)
            #print(tagged_list)
            for i in range(len(tagged_list)):
                tagged_sent=tagged_sent+' '+tagged_list[i]['word']+'/'+tagged_list[i]['pos']
            tagged_sent=tagged_sent+' '+punk+'/PUNCT\n'
            tagged_text=tagged_text+tagged_sent
            #print(tagged_sent)
        return tagged_text

#print(pos.tagger("Men bugun uyga bordim"))