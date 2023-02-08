from mistletoe.span_token import SpanToken
import re

class PersonalInfo(SpanToken):
    pattern = re.compile(r'`(.+?)`.*?\[(.+?)\].*\|?')
    precedence = 6
    def __init__(self, match_obj):
        self.target = match_obj.group(2)

class BeginDocument(SpanToken):
    pattern = re.compile(r' {0,3}(?:([_])\s*?)(?:\1\s*?){2,}')
    def __init__(self, match_obj):
        self.target = match_obj.group(1)

class PageBreak(SpanToken):
    pattern = re.compile(r' {0,3}(?:([*])\s*?)(?:\1\s*?){2,}')
    precedence = 6
    def __init__(self, match_obj):
        pass