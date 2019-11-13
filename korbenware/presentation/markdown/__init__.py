from korbenware.structuring import asdict, assert_dictable, is_dictable


def is_markdownable(obj):
    return hasattr(obj, '_repr_markdown_')


def _visit(level, obj):
    header = f'{"#" * level} {obj.__class__.__name__}'

    lines = [header, '']

    listed_attrs = []
    markdownable_attrs = []

    for k, v in asdict(obj).items():
        print(v, type(v), is_dictable(v), is_markdownable(v))
        if is_dictable(v) or is_markdownable(v):
            markdownable_attrs.append((k, v))
        else:
            listed_attrs.append((k, v))

    for k, v in listed_attrs:
        lines.append(f'* **{k}:** {v}')

    lines.append('')

    for k, v in markdownable_attrs:
        if is_markdownable(v):
            lines = lines + ['', v._repr_markdown_(), '']
        else:
            lines = lines + visit(level + 1, v)

        lines.append('')

    return '\n'.join(lines)


def markdownable(cls):
    assert_dictable(cls)

    def repr_markdown(self):
        return _visit(1, self)

    cls._repr_markdown_ = repr_markdown

    return cls
