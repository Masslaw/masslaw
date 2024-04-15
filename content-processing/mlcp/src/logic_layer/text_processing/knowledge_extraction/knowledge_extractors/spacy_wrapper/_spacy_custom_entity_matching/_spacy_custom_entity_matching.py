import spacy
from spacy.matcher.matcher import Matcher
from spacy.tokens.doc import Doc
from spacy.tokens.span import Span
from spacy.language import Language

from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._spacy_custom_entity_matching._custom_entity_matching_config import CUSTOM_ENTITY_MATCHING


def load_custom_entity_matcher_to_spacy_model(spacy_model: Language):
    matcher = _construct_custom_matcher(spacy_model)
    matcher_pipe = _construct_matcher_pipe(spacy_model, matcher)
    spacy_model.add_pipe(matcher_pipe, after='ner')


def _construct_custom_matcher(spacy_model: Language) -> Matcher:
    matcher = Matcher(spacy_model.vocab)
    for entity_type, patterns in CUSTOM_ENTITY_MATCHING.items(): matcher.add(entity_type, patterns)
    return matcher


def _construct_matcher_pipe(spacy_model: Language, matcher: Matcher) -> str:
    pipe_name = "custom_entity_matcher"
    pipe_component = lambda doc: _process_document_matches(doc, spacy_model, matcher)
    Language.component(pipe_name)(pipe_component)
    return pipe_name


def _process_document_matches(doc: Doc, spacy_model: Language, matcher: Matcher):
    matches = matcher(doc)
    spans = []
    for match_id, start, end in matches:
        rule_id = spacy_model.vocab.strings[match_id]
        span = Span(doc, start, end, label=rule_id)
        spans.append(span)
    all_spans = list(doc.ents) + spans
    merged_spans = _merge_overlapping_spans(all_spans)
    doc.ents = merged_spans
    return doc


def _merge_overlapping_spans(spans):
    if len(spans) < 2: return []
    sorted_spans = sorted(spans, key=lambda span: span.start)
    merged_spans = []
    current_start = sorted_spans[0].start
    current_end = sorted_spans[0].end
    current_label = sorted_spans[0].label_
    for span in sorted_spans[1:]:
        if span.start <= current_end:
            current_end = max(current_end, span.end)
            continue
        merged_spans.append(Span(span.doc, current_start, current_end, label=current_label))
        current_start = span.start
        current_end = span.end
        current_label = span.label_
    merged_spans.append(Span(sorted_spans[-1].doc, current_start, current_end, label=current_label))
    return merged_spans


