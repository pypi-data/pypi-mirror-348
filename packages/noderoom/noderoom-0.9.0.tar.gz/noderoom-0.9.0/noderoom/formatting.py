import re

class Format:
    ANSI = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'italic': '\033[3m',
        'light_red': '\033[91m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'dark_grey': '\033[90m',
        'light_cyan': '\033[96m',
    }

    @classmethod
    def ansi(cls, text, *styles):
        return ''.join(cls.ANSI[s] for s in styles) + text + cls.ANSI['reset']

    @classmethod
    def headers(cls, line):
        if line.startswith('### '):
            return cls.ansi(line[4:], 'bold', 'blue')
        elif line.startswith('## '):
            return cls.ansi(line[3:], 'bold', 'yellow')
        elif line.startswith('# '):
            return cls.ansi(line[2:], 'bold', 'light_red')
        elif line.strip() == '---':
            return '-' * 30
        return None

    @classmethod
    def bullets(cls, line):
        if line.strip().startswith('- '):
            return '• ' + line.strip()[2:]
        return None

    @classmethod
    def inline(cls, text, ai_name=None):
        def think_replacer(match):
            if ai_name:
                return cls.ansi(f"({ai_name}) is thinking...", 'dark_grey')
            else:
                return cls.ansi(match.group(1), 'dark_grey')

        text = re.sub(r'<think>(.*?)</think>', think_replacer, text)
        text = re.sub(r'\*\*(.*?)\*\*', lambda m: cls.ansi(m.group(1), 'bold'), text)
        text = re.sub(r'\*(.*?)\*', lambda m: cls.ansi(m.group(1), 'italic'), text)
        return text


    @classmethod
    def table(cls, lines):
        rows = []
        for line in lines:
            if '|' in line:
                parts = [p.strip() for p in line.strip('|').split('|')]
                rows.append(parts)
        if not rows:
            return []
        widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]

        def fmt_row(row):
            return '│ ' + ' │ '.join(f"{cell:<{widths[i]}}" for i, cell in enumerate(row)) + ' │'

        result = [
            '┌' + '┬'.join('─' * (w + 2) for w in widths) + '┐',
            fmt_row(rows[0]),
            '├' + '┼'.join('─' * (w + 2) for w in widths) + '┤'
        ]
        for row in rows[1:]:
            result.append(fmt_row(row))
        result.append('└' + '┴'.join('─' * (w + 2) for w in widths) + '┘')
        return result

    @classmethod
    def markdown(cls, text, verbose_output=False, ai_name=None):
        output = []
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if '|' in line:
                table_lines = []
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
                output.extend(cls.table(table_lines))
                continue

            header = cls.headers(line)
            if header:
                output.append(header)
            else:
                bullet = cls.bullets(line)
                if bullet:
                    output.append(cls.inline(bullet, ai_name))
                else:
                    output.append(cls.inline(line, ai_name))
            i += 1

        return '\n'.join(output)




# Convenient aliases for other modules to import
format_markdown = Format.markdown
format_text = Format.markdown
style_text = Format.markdown
parse_markdown = Format.markdown
markdown_to_ansi = Format.markdown
md_to_ansi = Format.markdown

# Example usage
if __name__ == '__main__':
    sample = """
# Title Header
## Sub Header
### Sub-sub Header
---
- Bullet point one
- Bullet point *with italics*
- Bullet point **with bold**
<think>This is a thought</think>

| Name    | Role        |
|---------|-------------|
| Byte    | Mega Mind   |
| Toasty  | Comic Relief|

Regular **bold** and *italic* and <think>thinking</think> line.
    """
    print(format_markdown(sample))
