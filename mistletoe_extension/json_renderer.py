import json5
import re
from mistletoe.html_renderer import HTMLRenderer
from mistletoe.span_token import RawText
from mistletoe.block_token import ThematicBreak
from mistletoe_extension.custom_span_tokens import PersonalInfo, BeginDocument
from mistletoe_extension.custom_block_tokens import CvEntry

ThematicBreak.pattern = re.compile(r' {0,3}(?:([-])\s*?)(?:\1\s*?){2,}$')

class JsonCVRenderer(HTMLRenderer):
    def __init__(self):
        super().__init__(CvEntry, PersonalInfo, BeginDocument)
        self._suppress_ptag_stack = [True]
        self.first = True
        self.started = False
        self.description_open = False

    def render_document(self, token):
        template = ('{{\n'
                    '{inner}')
        
        self.footnotes.update(token.footnotes)
        body = template.format(inner=self.render_inner(token))
        ending = ('null,\n'
                    '"ImagePath": null,\n'
                    '"SubSections": [\n'
                    ']\n'
                    '}\n'
                    ']\n'
                    '}') if self.description_open else (']\n}\n]\n}')
        json_object = json5.loads(body + ending)
        return json5.dumps(json_object, sort_keys=False, indent=4, quote_keys=True, trailing_commas=False, ensure_ascii=False)

    def render_personal_info(self, token):
        return ''

    def render_heading(self, token):
        inner = self.render_inner(token)
        if token.level == 1:
            template = ('\"Title\": "{}",\n'
                    '"SubTitle": "{}",\n'
                    '"Description": ')
            split_title = inner.split('-')
            name = split_title[0].strip()
            self.description_open = True
            return template.format(name, " - ".join([x.strip() for x in split_title[1:]]))
        image_path = 'null' if self.started else '"staticData/profile.jpg"'
        template = ('null,\n'
                    '"ImagePath": ') + image_path + (',\n'
                    '"SubSections": [\n') if self.description_open else ''
        template += (']\n'
                    '}},\n') if self.started else ''
        template += ('{{\n'
                    '"Title": "{}",\n'
                    '"SubTitle": null,\n'
                    '"Description": ')
        self.started = True
        self.description_open = True
        return template.format(inner)

    def render_begin_document(self, token):
        return ''
    
    def render_thematic_break(self, token):
        return ''

    def render_strong(self, token):
        return self.render_inner(token)

    def render_paragraph(self, token):
        if BeginDocument in [type(x) for x in token.children]:
            return ''
        if not self.started:
            render = super().render_paragraph(token)
            template = ('"{}",\n'
                    '"ImagePath": "staticData/profile.jpg",\n'
                    '"SubSections": [\n') if len(render.strip()) > 0 else ('null,\n'
                                                                        '"ImagePath": "staticData/profile.jpg",\n'
                                                                        '"SubSections": [\n')
            self.description_open = False
            return template.format(render)
        template = ('"{}",\n'
                    '"ImagePath": null,\n'
                    '"SubSections": [\n') if self.description_open and self.started else '{}'
        self.description_open = False
        return template.format(super().render_paragraph(token))
    
    def render_list(self, token):
        template = ('"{}",\n'
                        '"ImagePath": null,\n'
                        '"SubSections": [') if self.description_open else '{}'
        self.description_open = False

        list_template = '<{tag}{attr}>{inner}</{tag}>'
        if token.start is not None:
            tag = 'ol'
            attr = ' start={}'.format(token.start) if token.start != 1 else ''
        else:
            tag = 'ul'
            attr = ' style=list-style-type:disc'
        self._suppress_ptag_stack.append(not token.loose)
        inner = ''.join([self.render(child) for child in token.children])
        self._suppress_ptag_stack.pop()
        return '\n' + template.format(list_template.format(tag=tag, attr=attr, inner=inner)) + '\n'

    def render_cv_entry(self, token):
        template = ('null,\n'
                    '"ImagePath": null,\n'
                    '"SubSections": [\n') if self.description_open else ''
        self.description_open = False

        lines = list(filter(None, self.render_inner(token).split('\n')))
        split_pipe = [x.strip() for x in lines[0].split('|')]

        should_be_simple = len(split_pipe) == 1
        template += ('{{\n'
                '"Title": "{}",\n'
                '"SubTitle": {},\n'
                '"Description": {},\n'
                '"ImagePath": null,\n'
                '"SubSections": []\n'
                '}},\n')
        title = lines[0] if should_be_simple else split_pipe[1]
        split_pipe.pop(1)
        subtitle = 'null' if should_be_simple else '"' + ' | '.join(split_pipe) + '"'
        return template.format(title, subtitle, 'null' if should_be_simple or len(lines) == 1 else '"' + '\n'.join(lines[1:]) + '"')