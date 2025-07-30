from django.conf import settings
from luqum.visitor import TreeTransformer
from luqum.tree import NONE_ITEM
from luqum.parser import parser


class RemovePhraseTransformer(TreeTransformer):
    def visit_phrase(self, _node, _context):
        yield NONE_ITEM

def remove_phrases(qs):
    return [str(RemovePhraseTransformer().visit(parser.parse(q))) for q in qs]

def build_semantic_summary(document_dict, filtered_data):
    embedding_data = {}

    for filter in getattr(settings, "SEMANTIC_SEARCH_ADDITIONAL_FILTERS", []):
        embedding_data[filter.name()] = filter.document_value(document_dict)

    embedding_data.update(filtered_data)

    data_text = ""
    for name, value in embedding_data.items():
        name = name.replace("_", " ")
        if isinstance(value, list):
            for v in value:
                data_text += f"{name} is {v}. "
        elif value:
            data_text += f"{name} is {value}. "

    return data_text
