from mistletoe.block_token import BlockToken, Heading, CodeFence, ThematicBreak, List, Paragraph, tokenizer, _token_types
import re

ThematicBreak.pattern = re.compile(r' {0,3}(?:([-])\s*?)(?:\1\s*?){2,}$')

class CvEntry(BlockToken):
    """
    Block quote token. (["> # heading\\n", "> paragraph\\n"])
    This is a container block token. Its children are block tokens - container or leaf ones.
    """
    def __init__(self, parse_buffer):
        # span-level tokenizing happens here.
        self.children = tokenizer.make_tokens(parse_buffer)

    @staticmethod
    def start(line):
        stripped = line.lstrip(' ')
        if len(line) - len(stripped) > 3:
            return False
        return stripped.startswith('###')

    @classmethod
    def read(cls, lines):
        # first line
        line = cls.convert_leading_tabs(next(lines).lstrip()).split('###', 1)[1]
        if len(line) > 0 and line[0] == ' ':
            line = line[1:]
        line_buffer = [line]

        # loop
        next_line = lines.peek()
        while (next_line is not None
                and next_line.strip() != ''
                and not Heading.start(next_line)
                and not CodeFence.start(next_line)
                and not ThematicBreak.start(next_line)):
                
            stripped = cls.convert_leading_tabs(next_line.lstrip())
            line_buffer.append(stripped)
            next(lines)
            next_line = lines.peek()
        # block level tokens are parsed here, so that footnotes
        # in quotes can be recognized before span-level tokenizing.
        Paragraph.parse_setext = False
        parse_buffer = tokenizer.tokenize_block(line_buffer, _token_types)
        Paragraph.parse_setext = True
        return parse_buffer

    @staticmethod
    def convert_leading_tabs(string):
        string = string.replace('>\t', '   ', 1)
        count = 0
        for i, c in enumerate(string):
            if c == '\t':
                count += 4
            elif c == ' ':
                count += 1
            else:
                break
        if i == 0:
            return string
        return '>' + ' ' * count + string[i:]