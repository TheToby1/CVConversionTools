import html
import re
from mistletoe.html_renderer import HTMLRenderer
from mistletoe.span_token import RawText
from mistletoe.block_token import ThematicBreak
from mistletoe_extension.custom_span_tokens import PersonalInfo, PageBreak, BeginDocument

ThematicBreak.pattern = re.compile(r' {0,3}(?:([-])\s*?)(?:\1\s*?){2,}$')

class MudBlazorCVRenderer(HTMLRenderer):
    def __init__(self):
        super().__init__(PersonalInfo, BeginDocument, PageBreak)
        self.first = True

    def render_document(self, token):
        template = ('<MudList Clickable="false">\n'
                    '{inner}'
                    '</NestedList>\n'
                    '</MudListItem>\n'
                    '</MudList>')
        self.footnotes.update(token.footnotes)
        return template.format(inner=self.render_inner(token))

    def render_personal_info(self, token):
        return ''

    def render_paragraph(self, token):
        inner_render = self.render_inner(token)
        if self._suppress_ptag_stack[-1]:
            return '{}'.format(inner_render)

        if inner_render is None or inner_render == '' or inner_render.isspace():
            return ''
        if all(isinstance(item, RawText) for item in token.children):
            return '<MudListItem>\n{}</MudListItem>\n'.format(inner_render)
        else:
            return '<MudListItem>\n<NestedList>\n{}</NestedList>\n</MudListItem>\n'.format(inner_render)
    
    def render_raw_text(self, token):
        return '{}\n'.format(html.escape(token.content))
    
    def render_begin_document(self, token):
        return ''

    def render_page_break(self, token):
        return ''
    
    def render_list(self, token):
        template = '<MudListItem>\n<NestedList>\n{inner}</NestedList>\n</MudListItem>\n'
        self._suppress_ptag_stack.append(not token.loose)
        inner = '\n'.join([self.render(child) for child in token.children])
        self._suppress_ptag_stack.pop()
        return template.format(inner=inner)
    
    def render_list_item(self, token):
        if len(token.children) == 0:
            return '    <MudListItem></MudListItem>\n'
        inner = '\n'.join([self.render(child) for child in token.children])
        inner_template = '\n{}\n'
        if self._suppress_ptag_stack[-1]:
            if token.children[0].__class__.__name__ == 'Paragraph':
                inner_template = inner_template[1:]
            if token.children[-1].__class__.__name__ == 'Paragraph':
                inner_template = inner_template[:-1]
        return '    <MudListItem>\n{}</MudListItem>\n'.format(inner_template.format(inner))
    
    def render_heading(self, token):
        inner = self.render_inner(token)
        if token.level == 1:
            return ''
        elif token.level == 2:
            if self.first:
                self.first = False
                return '<MudListItem>\n<ChildContent>\n<MudText Class="mud-typography-h4">{}\n</MudText>\n</ChildContent>\n<NestedList>\n'.format(super().render_heading(token))
            else:
                return '</NestedList>\n</MudListItem>\n<MudListItem><ChildContent>\n<MudText Class="mud-typography-h4">{}\n</MudText>\n</ChildContent><NestedList>\n'.format(super().render_heading(token))

        return '<MudListItem>\n{}</MudListItem>\n'.format(super().render_heading(token))

    def render_table(self, token):
        # This is actually gross and I wonder if there's a better way to do it.
        #
        # The primary difficulty seems to be passing down alignment options to
        # reach individual cells.
        template = '<MudSimpleTable>\n{inner}</MudSimpleTable>'
        if hasattr(token, 'header'):
            head_template = '<thead>\n{inner}</thead>\n'
            head_inner = self.render_table_row(token.header, is_header=True)
            head_rendered = head_template.format(inner=head_inner)
        else: head_rendered = ''
        body_template = '<tbody>\n{inner}</tbody>\n'
        body_inner = self.render_inner(token)
        body_rendered = body_template.format(inner=body_inner)
        return template.format(inner=head_rendered+body_rendered)