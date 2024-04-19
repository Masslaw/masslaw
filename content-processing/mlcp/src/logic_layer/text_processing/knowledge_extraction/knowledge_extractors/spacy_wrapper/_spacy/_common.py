from typing import List

from spacy.tokens.span import Span
from spacy.tokens.token import Token


def get_entity_span_for_token(token: Token) -> Span | None:
    for ent in token.doc.ents:
        if ent.start <= token.i <= ent.end:
            return ent


def get_compound_chain(token: Token):
    return get_token_dependency_chain(token, ['compound'])


def get_token_dependency_chain(token, dependencies, _visited=None):
    visited = _visited or set()
    if token in visited: return set()
    visited.add(token)
    dependency_chain = {token}
    for child in token.children:
        if child.dep_ in dependencies:
            dependency_chain.update(get_token_dependency_chain(child, dependencies, visited))
    if token.head != token and token.dep_ in dependencies:
        dependency_chain.update(get_token_dependency_chain(token.head, dependencies, visited))
    return sort_tokens(list(dependency_chain))


def traverse_upward(token: Token, stop_condition: callable) -> List[Token]:
    token_chain = [token]
    while True:
        if stop_condition(token): return token_chain
        if token.head == token: return token_chain
        return token_chain + traverse_upward(token.head, stop_condition)


def traverse_downward(token: Token, stop_condition: callable) -> List[Token]:
    token_chain = [token]
    if stop_condition(token): return token_chain
    for child in token.children: token_chain += traverse_downward(child, stop_condition)
    return token_chain


def find_common_ancestor(token1: Token, token2: Token) -> Token | None:
    token1_chain = traverse_upward(token1, lambda token: False)
    token2_chain = traverse_upward(token2, lambda token: False)
    common_ancestors = set(token1_chain) & set(token2_chain)
    if not common_ancestors: return None
    return min(common_ancestors, key=lambda t: token1_chain.index(t))


def get_dependency_distance_between_tokens(token1: Token, token2: Token) -> int:
    common_ancestor = find_common_ancestor(token1, token2)
    if not common_ancestor: return None
    connecting_tokens = {token1, token2}
    current = token1
    while current != common_ancestor:
        current = current.head
        connecting_tokens.add(current)
    current = token2
    while current != common_ancestor:
        current = current.head
        connecting_tokens.add(current)
    return len(connecting_tokens)


def sort_tokens(tokens: List[Token]):
    return sorted(tokens, key=lambda token: token.i)
