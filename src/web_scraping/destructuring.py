import re
HEADER_PATTERN = re.compile("(.+?):$")
LIST_ENTRY_PATTERN = re.compile("(.+?): (.+)")

# Should also handle note texts, that is, delete them
# notes should be logged at debug level to a special file


def get_key(header):
    key = HEADER_PATTERN.match(header)
    return key.group(1) if key else None


def get_key_value(entry):
    key_value_pair = LIST_ENTRY_PATTERN.match(entry)
    return key_value_pair.group(1), key_value_pair.group(2) if key_value_pair is not None else (None, None)


def destructure_list_like(html_fragments):
    mapping = {}
    i = 0
    for element in html_fragments:
        if i % 2 == 0:
            header = element
        else:
            mapping[get_key(header)] = element
        i = (i + 1) % 2
    return mapping


# TODO : this could be a recursive function
def destructure_nested_lists(html_fragments):
    mapping = {}
    current_key = None
    for fragment in html_fragments:
        outer_key = get_key(fragment)
        if outer_key:
            current_key = outer_key
        else:
            key, value = get_key_value(fragment)
            mapping[current_key + "_" + key] = value

    return mapping


def destructure_list_like_with_text(html_fragments):
    mapping = {'caption': next(html_fragments)}
    mapping.update(destructure_list_like(html_fragments))
    return mapping


def destructure_text_paragraph(html_fragments, field_names=("rate", )):
    return {k: fragment for k, fragment in zip(field_names, list(html_fragments))}
