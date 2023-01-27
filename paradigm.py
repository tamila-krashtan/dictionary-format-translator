from dataclasses import dataclass


@dataclass
class SearchWord:
    word: str
    tag: str = ''
    meaning: str = None
    orthography: str = None
    type: str = ''
    options: str = ''


class Paradigm:

    def __init__(self, lemma, forms):
        self.dict_lemma = lemma
        self.dict_forms = forms
        self.search_lemma = SearchWord(lemma.head, meaning=lemma.comment)
        self.search_forms = []

        self.pos = lemma.tags[0]
        if 'ua_2019' in lemma.tags:
            self.search_lemma.orthography = 'ua_2019'
        elif 'ua_1992' in lemma.tags:
            self.search_lemma.orthography = 'ua_1992'

    def translate(self):
        match self.pos:
            case 'noun':
                self.translate_noun()
            case 'verb':
                self.translate_verb()
            case 'adj':
                self.translate_adjective()
            case 'adv':
                self.translate_adverb()
            case 'advp':
                raise NotImplementedError('Not processing advp yet')
            case 'prep':
                self.translate_preposition()
            case 'conj':
                self.translate_conjunction()
            case 'part':
                self.translate_particle()
            case 'intj':
                self.translate_interjection()
            case 'numr':
                self.search_lemma.tag = 'M'
                self.search_forms.append(SearchWord(self.search_lemma.word))
            case 'noninfl':
                self.translate_other()
            case 'onomat':
                self.translate_other()
            case _:
                raise Exception('Unknown POS tag: {}'.format(self.pos))

    def save(self, paradigm_id, output_file):
        output_file.write('  <Paradigm pdgId="{}" lemma="{}" tag="{}"'
                          .format(paradigm_id, self.search_lemma.word, self.search_lemma.tag))
        if self.search_lemma.meaning:
            output_file.write(' meaning="{}"'.format(self.search_lemma.meaning))
        output_file.write('>\n')

        output_file.write('    <Variant id="a" lemma="{}"'.format(self.search_lemma.word))
        if self.search_lemma.orthography:
            output_file.write(' orthography="{}"'.format(self.search_lemma.orthography))
        output_file.write('>\n')

        for search_form in self.search_forms:
            output_file.write('      <Form tag="{}"'.format(search_form.tag))
            if search_form.options:
                output_file.write(' options="{}"'.format(search_form.options))
            output_file.write('>{}</Form>\n'.format(search_form.word))

        output_file.write('    </Variant>\n  </Paradigm>\n')

    def translate_noun(self):
        self.search_lemma.tag = 'N'
        if 'prop' in self.dict_lemma.tags:
            self.search_lemma.tag += 'P'
        else:
            self.search_lemma.tag += 'C'

        if 'anim' in self.dict_lemma.tags:
            self.search_lemma.tag += 'A'
        else:
            self.search_lemma.tag += 'I'

        if 'abbr' in self.dict_lemma.tags:
            self.search_lemma.tag += 'B'
        else:
            self.search_lemma.tag += 'N'

        if 'm' in self.dict_lemma.tags:
            self.search_lemma.tag += 'M'
        elif 'f' in self.dict_lemma.tags:
            self.search_lemma.tag += 'F'
        elif 'n' in self.dict_lemma.tags:
            self.search_lemma.tag += 'N'
        elif 'ns' in self.dict_lemma.tags:
            self.search_lemma.tag += 'P'
        else:
            self.search_lemma.tag += 'C'

        if 'p' in self.dict_lemma.tags:
            self.search_forms.append(SearchWord(self.search_lemma.word, tag='NP'))
        else:
            self.search_forms.append(SearchWord(self.search_lemma.word, tag='NS'))

        for dict_form in self.dict_forms:
            search_form = SearchWord(dict_form.head)
            if 'ua_2019' in dict_form.tags:
                search_form.orthography = 'ua_2019'
            elif 'ua_1992' in dict_form.tags:
                search_form.orthography = 'ua_1992'

            if 'v_rod' in dict_form.tags:
                search_form.tag += 'G'
            elif 'v_dav' in dict_form.tags:
                search_form.tag += 'D'
            elif 'v_zna' in dict_form.tags:
                search_form.tag += 'A'
            elif 'v_oru' in dict_form.tags:
                search_form.tag += 'I'
            elif 'v_mis' in dict_form.tags:
                search_form.tag += 'L'
            elif 'v_kly' in dict_form.tags:
                search_form.tag += 'V'
            else:
                search_form.tag += 'N'

            if 'p' in dict_form.tags:
                search_form.tag += 'P'
            else:
                search_form.tag += 'S'

            self.search_forms.append(search_form)

    def translate_adjective(self):
        self.search_lemma.tag = 'A'
        if 'compc' in self.dict_lemma.tags:
            self.search_lemma.tag += 'C'
        elif 'comps' in self.dict_lemma.tags:
            self.search_lemma.tag += 'S'
        else:
            self.search_lemma.tag += 'P'

        self.search_forms.append(SearchWord(self.search_lemma.word, tag='MNS'))

        for dict_form in self.dict_forms:
            search_form = SearchWord(dict_form.head)
            if 'ua_2019' in dict_form.tags:
                search_form.orthography = 'ua_2019'
            elif 'ua_1992' in dict_form.tags:
                search_form.orthography = 'ua_1992'

            if 'p' in dict_form.tags:
                search_form.tag += 'P'
            elif 'f' in dict_form.tags:
                search_form.tag += 'F'
            elif 'n' in dict_form.tags:
                search_form.tag += 'N'
            else:
                search_form.tag += 'M'

            if 'v_rod' in dict_form.tags:
                search_form.tag += 'G'
            elif 'v_dav' in dict_form.tags:
                search_form.tag += 'D'
            elif 'v_zna' in dict_form.tags:
                search_form.tag += 'A'
            elif 'v_oru' in dict_form.tags:
                search_form.tag += 'I'
            elif 'v_mis' in dict_form.tags:
                search_form.tag += 'L'
            elif 'v_kly' in dict_form.tags:
                search_form.tag += 'V'
            else:
                search_form.tag += 'N'

            if 'p' in dict_form.tags:
                search_form.tag += 'P'
            else:
                search_form.tag += 'S'

            if 'ranim' in dict_form.tags:
                search_form.options = 'anim'
            elif 'rinanim' in dict_form.tags:
                search_form.options = 'inanim'

            self.search_forms.append(search_form)

    def translate_verb(self):
        self.search_lemma.tag = 'V'
        if 'perf' in self.dict_lemma.tags:
            self.search_lemma.tag += 'P'
        else:
            self.search_lemma.tag += 'M'

        if 'rev' in self.dict_lemma.tags:
            self.search_lemma.tag += 'R'
        else:
            self.search_lemma.tag += 'N'

        self.search_forms.append(SearchWord(self.search_lemma.word, tag='0'))

        for dict_form in self.dict_forms:
            search_form = SearchWord(dict_form.head)
            if 'ua_2019' in dict_form.tags:
                search_form.orthography = 'ua_2019'
            elif 'ua_1992' in dict_form.tags:
                search_form.orthography = 'ua_1992'

            if 'futr' in dict_form.tags:
                search_form.tag += 'F'
            elif 'past' in dict_form.tags:
                search_form.tag += 'P'
            elif 'pres' in dict_form.tags:
                search_form.tag += 'R'
            else:
                continue

            if 'impr' in dict_form.tags:
                search_form.tag += 'I'

            if '1' in dict_form.tags:
                search_form.tag += '1'
            elif '2' in dict_form.tags:
                search_form.tag += '2'
            elif '3' in dict_form.tags:
                search_form.tag += '3'
            elif 'impers' in dict_form.tags:
                search_form.tag += '0'

            if 'm' in dict_form.tags:
                search_form.tag += 'M'
            elif 'f' in dict_form.tags:
                search_form.tag += 'F'
            elif 'n' in dict_form.tags:
                search_form.tag += 'N'
            elif 'past' in dict_form.tags:
                search_form.tag += 'X'

            if 'p' in dict_form.tags:
                search_form.tag += 'P'
            else:
                search_form.tag += 'S'

            self.search_forms.append(search_form)

    def translate_adverb(self):
        self.search_lemma.tag = 'R'

        if 'compc' in self.dict_lemma.tags:
            self.search_forms.append(SearchWord(self.search_lemma.word, tag='C'))
        elif 'comps' in self.dict_lemma.tags:
            self.search_forms.append(SearchWord(self.search_lemma.word, tag='S'))
        else:
            self.search_forms.append(SearchWord(self.search_lemma.word, tag='P'))

    def translate_conjunction(self):
        self.search_lemma.tag = 'C'

        if 'subord' in self.dict_lemma.tags:
            self.search_lemma.tag += 'S'
        elif 'coord' in self.dict_lemma.tags:
            self.search_lemma.tag += 'K'

        self.search_forms.append(SearchWord(self.search_lemma.word))

    def translate_preposition(self):
        self.search_lemma.tag = 'I'
        self.search_forms.append(SearchWord(self.search_lemma.word))

    def translate_particle(self):
        self.search_lemma.tag = 'E'
        self.search_forms.append(SearchWord(self.search_lemma.word))

    def translate_interjection(self):
        self.search_lemma.tag = 'Y'
        self.search_forms.append(SearchWord(self.search_lemma.word))

    def translate_other(self):
        self.search_lemma.tag = 'Z'
        self.search_forms.append(SearchWord(self.search_lemma.word))
