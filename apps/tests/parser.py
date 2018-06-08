from html.parser import HTMLParser


class TestParser(HTMLParser):

    image_tag = '<img src="{p}" style="{s}" />'

    def __init__(self, *args, **kwargs):
        self.question_list = []
        self.current_question = None
        self.text = ''
        self.is_true = False
        self.klass = None
        self.points_amount = 1
        HTMLParser.__init__(self, *args, **kwargs)

    def start_question(self):
        self.current_question = {
            'text': '',
            'klass': self.klass,
            'points_amount': self.points_amount,
            'answers': []
        }

        self.question_list.append(
            self.current_question)

    def handle_starttag(self, tag, attrs):
        if tag == 'question':
            attrs = dict(attrs)
            self.klass = attrs.get('klass', '""')[1:-1]
            self.points_amount = attrs.get('points_amount', '"1"')[1:-1]
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
                'is_true': self.is_true,
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
