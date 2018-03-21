from html.parser import HTMLParser


class TestParser(HTMLParser):

    image_tag = '<img src="{p}" style="{s}" />'

    def __init__(self, *args, **kwargs):
        self.question_list = []
        self.current_question = None
        self.text = ''
        self.is_true = False
        HTMLParser.__init__(self, *args, **kwargs)

    def start_question(self):
        self.current_question = {
            'text': '',
            'answers': []
        }

        self.question_list.append(
            self.current_question)

    def handle_starttag(self, tag, attrs):
        if tag == 'question':
            self.start_question()
            self.text = ''

        if tag == 'answer':
            self.text = ''
            self.is_true = 'is_true' in dict(attrs)

    def handle_endtag(self, tag):
        if tag == "question":
            self.current_question['text'] = self.text

        if tag == "answer":
            self.current_question['answers'].append({
                'text': self.text,
                'is_true': self.is_true
            })
            self.is_true = False

    def handle_startendtag(self, tag, attrs):
        attrs = dict(attrs)
        self.text += self.image_tag.format(
            **{'p': attrs['src'], 's': attrs['style']}
        )

    def handle_data(self, data):
        self.text += data


def pasre_test_format(data):
    test_parser = TestParser()
    test_parser.feed(data)
    return test_parser.question_list
