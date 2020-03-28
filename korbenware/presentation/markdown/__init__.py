import datetime

import arrow

from korbenware.keys import assert_keys, has_keys, iter_items


def is_markdownable(obj):
    return hasattr(obj, '_repr_markdown_')


def _visit(level, obj, name=None):
    if not name:
        name = obj.__class__.__name__
    header = f'{"#" * level} {name}'

    lines = [header, '']

    listed_attrs = []
    markdownable_attrs = []

    for k, v in iter_items(obj):
        if has_keys(v) or is_markdownable(v):
            markdownable_attrs.append((k, v))
        else:
            listed_attrs.append((k, v))

    for k, v in listed_attrs:
        if type(v) == list:
            lines.append(f'* **{k}:**')
            for element in v:
                lines.append(f'    * {element}')
        elif type(v) == dict:
            lines.append(f'* **{k}:**')
            for elem_k, elem_v in v.items():
                lines.append(f'    * **{elem_k}:** {elem_v}')
        elif type(v) == datetime.datetime:
            lines.append(f'* **{k}:** {v} ({arrow.get(v).humanize()})')
        else:
            lines.append(f'* **{k}:** {v}')

    lines.append('')

    for k, v in markdownable_attrs:
        if is_markdownable(v):
            lines = lines + ['', v._repr_markdown_(level + 1, name=k), '']
        else:
            lines = lines + _visit(level + 1, v, name=k)

        lines.append('')

    return '\n'.join(lines)


def markdownable(cls):
    assert_keys(cls)

    def repr_markdown(self, level=1, name=None):
        return _visit(level, self, name)

    cls._repr_markdown_ = repr_markdown

    return cls
