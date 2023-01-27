import sys
from word import Word
from paradigm import Paradigm


def open_file(letter):
    output_file = open('out/{}.xml'.format(letter), 'w')
    output_file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
    output_file.write('<Wordlist>\n')
    return output_file


def close_file(file):
    file.write('</Wordlist>')
    file.close()


def process_paradigm(lemma, forms, pdgId, output_file):
    try:
        lemma_word = Word(lemma)
        form_words = [Word(form) for form in forms]
        paradigm = Paradigm(lemma_word, form_words)
        paradigm.translate()
        paradigm.save(pdgId, output_file)
    except NotImplementedError:
        pass
    except Exception as e:
        print('Lemma was not processed: {}'.format(lemma))
        print(e)


if len(sys.argv) != 2:
    raise Exception('One argument required, {} provided'.format(len(sys.argv) - 1))

pdgId = 0
current_letter = 'а'
lemma = ''
forms = []
current_file = open_file(current_letter)

with open(sys.argv[1]) as input_file:
    for line in input_file:
        if line.startswith(' '):
            forms.append(line)
        else:
            if lemma and not lemma.lower().startswith("'"):
                pdgId += 1
                process_paradigm(lemma, forms, pdgId, current_file)
            lemma = line
            forms = []
            if not lemma.lower().startswith(current_letter) and not lemma.lower().startswith("'"):
                close_file(current_file)
                current_letter = lemma.lower()[0]
                current_file = open_file(current_letter)

    close_file(current_file)
