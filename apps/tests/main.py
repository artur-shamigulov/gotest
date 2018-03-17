from parserXML import get_full_text
from parser import TestParser

f = open('Shpory_matem.docx', 'rb')

a = TestParser()
a.feed(get_full_text(f))
f = open('output.html')

for question in a.current_question:
    answers = ''
    for answer in a.answers:
        answers += '<li>%s</li>' % answer

    f.write(
        '<p>Вопрос: %s</p><p>Ответы:</p><ul>%s</ul>' % (question['text'], answers)
    )

f.close()
