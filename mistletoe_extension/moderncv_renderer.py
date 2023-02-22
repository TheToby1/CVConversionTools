from mistletoe.latex_renderer import LaTeXRenderer
from mistletoe.span_token import RawText
from mistletoe.block_token import ListItem
from mistletoe_extension.custom_span_tokens import PersonalInfo, PageBreak, BeginDocument
from mistletoe_extension.custom_block_tokens import CvEntry

SOCIALS = ['github', 'gitlab', 'twitter', 'linkedin']
PHONES = ['mobile', 'fixed', 'fax']

class ModernCVRenderer(LaTeXRenderer):
    def __init__(self):
        super().__init__(CvEntry, PersonalInfo, BeginDocument, PageBreak)
        self.packages['babel'] = '[english]'
        self.packages['eurosym'] = []
        self.packages['geometry'] = '[left=.9cm, right=.9cm, top=.6cm, bottom=.6cm]'
        self.packages['lmodern'] = []
    
    def render_document(self, token):
        template = ('\\documentclass[10pt,a4paper,sans]{{moderncv}}\n'
                    '\\moderncvstyle{{classic}}\n'
                    '\\moderncvcolor{{blue}}\n'
                    '\\renewcommand{{\\listitemsymbol}}{{-~}}\n'
                    '\\nopagenumbers{{}}\n'
                    '{packages}'
                    '\\setlength{{\\hintscolumnwidth}}{{3cm}}\n\n'
                    '{inner}'
                    '\\end{{document}}\n')
        self.footnotes.update(token.footnotes)
        return template.format(inner=self.render_inner(token),
                               packages=self.render_packages())

    def render_heading(self, token):
        inner = self.render_inner(token)
        if token.level == 1:
            template = ('\\name{{{}}}{{{}}}\n'
                    '\\title{{{}}}')
            split_title = inner.split('-')
            name = split_title[0].strip().split(' ')
            return template.format(*name, split_title[1].strip())
        elif token.level == 2:
            return '\n\\section{{{}}}\n'.format(inner)
        elif token.level == 3:
            return '\n\\subsection{{{}}}\n'.format(inner)
        return '\n\\subsubsection{{{}}}\n'.format(inner)

    def render_personal_info(self, token):
        template = '\{inner}{{{target}}}'
        target = token.target
        inner = self.render_inner(token)
        if inner in SOCIALS:
            inner = 'social[{inner}]'.format(inner=inner)
        if inner in PHONES:
            inner = 'phone[{inner}]'.format(inner=inner)
        return template.format(target=target, inner=inner)

    def render_begin_document(self, token):
        template = ('\\begin{document}\n'
                    '\\makecvtitle\n'
                    '\\vspace*{-12mm}')
        return template

    def render_page_break(self, token):
        return '\\clearpage\n'

    def render_list(self, token):
        return self.render_inner(token)

    def render_list_item(self, token):
        inner = self.render_inner(token).replace('\n', ' ')
        return '\\cvlistitem{{{}}}\n'.format(inner)

    def convert_pipe_to_bracket(string):
        return string.replace('|', '}{')

    def render_cv_entry(self, token):
        lines = list(filter(None, self.render_inner(token).split('\n')))
        split_pipe = lines[0].split('|')
        if len(lines) == 1 and len(split_pipe) <= 2:
            inner = lines[0].replace(' | ', '}{')
            template = '\\cvitem{{{}}}\n'
            return template.format(inner)
        elif ListItem in [type(y) for x in token.children for y in x.children]:
            inner_first_section = '}{'.join([x.strip() for x in split_pipe])
            missing_brackets = 6 - len(split_pipe)

            first_section_template = '\\cventry{{{}}}'
            first_section = first_section_template.format(inner_first_section)
            cv_entry = first_section + '{}' * missing_brackets + '\n'

            all_items = [x + '\n' if '\\cvlistitem' in x else '\\cvitem{{}}{{{}}}\n'.format(x) for x in lines[1:]]
            return cv_entry + ''.join(all_items)
        else:
            inner_first_section = '}{'.join([x.strip() for x in split_pipe])
            missing_brackets = 5 - len(split_pipe)

            first_section_template = '\\cventry{{{}}}'
            first_section = first_section_template.format(inner_first_section)
            ending = '{{{}}}'.format('\n'.join(lines[1:]))
            return first_section + '{}' * missing_brackets + ending + '\n'

    def render_table(self, token):
        def render_align(column_align):
            if column_align != [None]:
                cols = [get_align(col) for col in token.column_align]
                return '{{{}}}'.format(' '.join(cols))
            else:
                return ''

        def get_align(col):
            if col is None:
                return 'l'
            elif col == 0:
                return 'p{2cm}'
            elif col == 1:
                return '|r'
            raise RuntimeError('Unrecognized align option: ' + col)

        template = ('\\setlength{{\\tabcolsep}}{{0.5em}}\n'
                    '{{\\renewcommand{{\\arraystretch}}{{1.2}}\n'
                    '\\begin{{tabular}}{align}\n'
                    '{inner}'
                    '\\end{{tabular}}}}\n')
        if hasattr(token, 'header'):
            head_template = '{inner}\\hline\n'
            head_inner = self.render_table_row(token.header)
            head_rendered = head_template.format(inner=head_inner)
        else: 
            head_rendered = ''
        inner = self.render_inner(token)
        align = render_align(token.column_align)
        return template.format(inner=head_rendered+inner, align=align)