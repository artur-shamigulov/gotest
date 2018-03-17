# -*- coding: utf-8 -*-
import base64
import os

from HTMLParser import HTMLParser
from cStringIO import StringIO
from zipfile import ZipFile, BadZipfile

EMUS_PER_PIXEL = 9525
IMAGE_SHEMA = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'
WMF_PARSE_CALL = """wmf2gd --maxpect --maxwidth=300 --maxheight=100 inp.wmf>out.wmf"""


class Image(object):
    width = ''
    height = ''
    path = None
    image = None
    image_tag = '<img src="{p}" width="{w}" height="{h}" />'
    src_attr = 'data:image/%s;base64,%s'
    zf = None

    def __init__(self, zf):
        self.zf = zf

    def convert_wmf(self, path):
        tmp = open('inp.wmf', 'wb')
        tmp.write(self.zf.read('word/' + path))
        tmp.close()
        stream_out = StringIO()
        os.system(WMF_PARSE_CALL)
        base64.encode(open('out.wmf', 'rb'), stream_out)
        stream_out.seek(0)
        return self.src_attr % (path[:-3], stream_out.read())

    def convert_img(self, path):
        stream = StringIO()
        base64.encode(self.zf.open('word/' + path), stream)
        stream.seek(0)
        return self.src_attr % (path[:-3], stream.read())

    def get_image(self):
        if not self.image:
            if not self.path:
                return ''
            if self.path.lower().endswith('wmf'):
                self.image = self.convert_wmf(self.path)
            else:
                self.image = self.convert_img(self.path)
        return self.image_tag.format(**{
            'p': self.image,
            'w': self.width,
            'h': self.height
        })


class HeaderParser(HTMLParser):
    relationship_dict = {}

    def __init__(self, data, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self.feed(data)

    def get_relationship_dict(self):
        return self.relationship_dict

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('type') == IMAGE_SHEMA:
            self.relationship_dict[attrs['id']] = attrs['target']


class DocumentParser(HTMLParser):
    text = ''
    is_question = False

    cur_image = None

    relationship_dict = {}

    question_list = []
    cur_question = None

    def __init__(self, relationship_dict, zf, *args, **kwargs):
        self.relationship_dict = relationship_dict
        self.zf = zf
        HTMLParser.__init__(self, *args, **kwargs)

    def set_image_attr(self, attr, value):
        if self.cur_image:
            setattr(self.cur_image, attr, value)
        else:
            raise ValueError

    def handle_starttag(self, tag, attrs):
        if tag == 'w:b':
            self.is_question = True
        if tag == 'w:drawing':
            self.cur_image = Image(self.zf)

        if tag == "a:ext":
            width = int(dict(attrs).get('cx', 0)) / EMUS_PER_PIXEL
            if width:
                self.set_image_attr('width', width)
            height = int(dict(attrs).get('cy', 0)) / EMUS_PER_PIXEL
            if height:
                self.set_image_attr('height', height)

        if tag == 'a:blip':
            image_id = dict(attrs).get('r:embed')
            self.set_image_attr(
                'path', self.relationship_dict.get(image_id)
            )

    def handle_endtag(self, tag):
        if tag == "w:p":
            if len(self.text):
                if self.is_question:
                    self.cur_question = {
                        'question': self.text,
                        'variants': []
                    }
                    self.question_list.append(
                        self.cur_question
                    )
                else:
                    self.cur_question['variants'].append(self.text)
            self.is_question = False
            self.text = ''
        if tag == 'w:drawing':
            self.text += self.cur_image.get_image()

    def handle_data(self, data):
        self.text += data


def get_question_list(file):
    zf = ZipFile(file)

    header_parser = HeaderParser(zf.read('word/_rels/document.xml.rels'))
    relationship_dict = header_parser.get_relationship_dict()

    document_parser = DocumentParser(relationship_dict, zf)
    document_parser.feed(zf.read('word/document.xml'))

    return document_parser.question_list
