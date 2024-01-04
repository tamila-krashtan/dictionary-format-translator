import sys
import psycopg2
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


def process_paradigm(lemma, forms, pdgId=None):
    try:
        lemma_word = Word(lemma)
        form_words = [Word(form) for form in forms]
        paradigm = Paradigm(lemma_word, form_words)
        paradigm.translate()
        paradigm.save_xml(pdgId, current_file) if xml else paradigm.save_postgres(cur)
    except NotImplementedError:
        pass
    except Exception as e:
        print(f'Lemma was not processed: {lemma}')
        print(e)


if len(sys.argv) != 3 and len(sys.argv) != 4:
    raise Exception('Wrong number of arguments')

if sys.argv[2] == "xml":
    xml = True
elif sys.argv[2] == "db":
    xml = False
    db_password = sys.argv[3]
else:
    raise Exception('Wrong mode. Has to be either xml or db')

pdgId = 0
current_letter = 'а'
lemma = ''
forms = []
current_file = open_file(current_letter)

with open(sys.argv[1]) as input_file:
    if not xml:
        conn = psycopg2.connect(f"dbname=vesum user=postgres password={db_password}")
        cur = conn.cursor()

    counter = 0
    for line in input_file:
        if line.startswith(' '):
            forms.append(line)
        else:
            if lemma and not lemma.lower().startswith("'"):
                pdgId += 1
                process_paradigm(lemma, forms, pdgId)
            lemma = line
            forms = []
            if xml:
                if not lemma.lower().startswith(current_letter) and not lemma.lower().startswith("'"):
                    close_file(current_file)
                    current_letter = lemma.lower()[0]
                    current_file = open_file(current_letter)
            else:
                counter += 1
                if not counter % 1000:
                    print(counter)

    if xml:
        close_file(current_file)
    else:
        print("committing...")
        conn.commit()
        print("committed")
        cur.close()
        conn.close()
