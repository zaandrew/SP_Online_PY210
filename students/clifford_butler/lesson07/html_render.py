#!/usr/bin/env python3

"""
A class-based system for rendering html.

Author: Clifford Butler
"""

# This is the framework for the base class
class Element(object):
    tag = "html"
    indent = "  "

    def __init__(self, content=None, **kwargs):
        if content is None:
            self.contents = []
        else:
            self.contents = [content]

        if kwargs is not None:
            self.attributes = kwargs
        else:
            self.attributes = {}
            
    def append(self, new_content):
        self.contents.append(new_content)

    def render(self, out_file, cur_ind=""):
        new_indent = cur_ind + self.indent
        out_file.write(cur_ind + self.a_open_tag())
        out_file.write("\n")
        for content in self.contents:
            try:
                content.render(out_file, cur_ind = new_indent)
            except AttributeError:
                out_file.write(new_indent + content)
            out_file.write("\n")
        out_file.write(cur_ind + self.a_close_tag())
        
    def a_open_tag(self):
        open_tag = ["<{}".format(self.tag)]
        for key, value in self.attributes.items():
            open_tag.append(' {}="{}"'.format(key, value))
        open_tag.append(">")
        return "".join(open_tag)

    def a_close_tag(self):
        return "</{}>".format(self.tag)
    
class Body(Element):
    tag = 'body'

class Html(Element):
    tag = 'html'
    def render(self, out_file, cur_ind=""):
        out_file.write(cur_ind)
        out_file.write("<!DOCTYPE html>\n")
        super().render(out_file, cur_ind)

class P(Element):
    tag = 'p'

class Head(Element):
    tag = 'head'

class OneLineTag(Element):
    def render(self, out_file, cur_ind=""):
        out_file.write(cur_ind)
        out_file.write(self.a_open_tag())
        out_file.write(self.contents[0])
        out_file.write(self.a_close_tag())

    def append(self, content):
        raise NotImplementedError

class Title(OneLineTag):
    tag = "title"

class SelfClosingTag(Element):
    def __init__(self, content=None, **kwargs):
        if content is not None:
            raise TypeError("SelfClosingTag can not contain any content")
        super().__init__(content=content, **kwargs)

    def render(self, out_file, cur_ind=""):
        tag = self.a_open_tag()[:-1] + " />\n"
        out_file.write(cur_ind + tag)

    def append(self, *args):
        raise TypeError("You can not add content to a SelfClosingTag")

class Hr(SelfClosingTag):
    tag = "hr"

class Br(SelfClosingTag):
    tag = "br"

class A(OneLineTag):
    tag = 'a'
    def __init__(self, link, content=None, **kwargs):
        kwargs['href'] = link
        super().__init__(content, **kwargs)

class Ul(Element):
    tag = "ul"

class Li(Element):
    tag = "li"

class H(OneLineTag):
    tag = 'h'
    def __init__(self, level, content=None, **kwargs):
        self.tag = 'h{}'.format(level)
        super().__init__(content=content,**kwargs)

class Meta(Element):
    def __init__(self, charset):
        self.charset = charset
    def render(self, out_file, cur_ind=""):
        out_file.write(cur_ind + '<meta charset="{}" />\n'.format(self.charset))

