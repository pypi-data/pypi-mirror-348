"""
Parse config rules

sai_expand(0, 5)
sai_expand(.0, 5)
sai_expand(0., 5)
sai_expand(0.0, 5)
sai_expand(0, .5)
sai_expand(.0, .5)
sai_expand(0., .5)
sai_expand(0.0, .5)
sai_expand(0, 5.)
sai_expand(.0, 5.)
sai_expand(0., 5.)
sai_expand(0.0, 5.)
sai_expand(0, 5.0)
sai_expand(.0, 5.0)
sai_expand(0., 5.0)
sai_expand(0.0, 5.0)

sai_rand(-1, 1)
sai_choose(repeat=False)
sai_choose(repeat=False, tag=tag)
sai_sequence()
sai_sequence(tag=tag)

sai_expand(0, sai_rand(-1, 1))
sai_expand(sai_rand(0, 4), 0)
sai_expand(sai_rand(0, 4), sai_rand(-1, 1))

sai_choose(num=1, unique=speaker_id, repeat=False)
sai_choose(num=1, repeat=False)
sai_choose(num=1, unique=speaker_id, repeat=True)
sai_choose(num=1, repeat=True)
sai_sequence(num=0)
sai_sequence(num=0, unique=speaker_id)

"""

from dataclasses import dataclass


@dataclass
class Match:
    group: str
    span: tuple[int, int]

    def start(self) -> int:
        return self.span[0]

    def end(self) -> int:
        return self.span[1]


def find_sai_expand(text: str) -> list[Match]:
    import re

    results = []
    matches = re.finditer(r"sai_expand\(", text)
    if matches:
        for match in matches:
            s = match.start()
            e = match.end()
            num_lparen = 1
            while num_lparen != 0 and e < len(text):
                if text[e] == "(":
                    num_lparen += 1
                elif text[e] == ")":
                    num_lparen -= 1
                e += 1
            if num_lparen != 0:
                raise ValueError(f"Unbalanced parenthesis in '{text}'")

            results.append(Match(group=text[s:e], span=(s, e)))

    return results


def parse_sai_expand(text: str) -> list[str]:
    """
    expand_syntax ::= expand_keyword lparen expand_item next_expand_item+ rparen
    expand_keyword ::= sai_expand
    lparen ::= (
    expand_item ::= expand_syntax | rand_syntax | number
    rand_syntax ::= rand_keyword lparen rand_item comma rand_item rparen
    rand_item ::= real number
    comma ::= ,
    number ::= real number or signed integer
    next_item ::= comma item
    rparen ::= )
    """
    import pyparsing as pp

    lparen = pp.Literal("(")
    rparen = pp.Literal(")")
    comma = pp.Literal(",")

    real_number = pp.pyparsing_common.real
    signed_integer = pp.pyparsing_common.signed_integer
    number = real_number | signed_integer

    identifier = pp.Word(pp.alphanums + "_.-")

    rand_literal = pp.Literal("sai_rand")
    rand_expression = (rand_literal + lparen + number + comma + number + rparen).set_parse_action(
        lambda tokens: "".join(map(str, tokens))
    )

    expand_literal = pp.Literal("sai_expand")
    expand_args = pp.DelimitedList(rand_expression | identifier, min=1)
    expand_expression = expand_literal + lparen + expand_args("args") + rparen

    try:
        result = expand_expression.parse_string(text)
    except pp.ParseException as e:
        raise ValueError(f"Could not parse '{text}'") from e

    return list(result.args)


def sai_expand(text: str) -> list[str]:
    # initialize with input
    expanded = [text]

    # look for pattern
    matches = find_sai_expand(text)

    # if not found, early exit
    if not matches:
        return expanded

    # remove entry we are expanding
    expanded.pop()

    # start with the innermost match
    match = matches[-1]
    prelude = text[: match.start()]
    postlude = text[match.end() :]

    # loop over parsed expand values
    for value in parse_sai_expand(match.group):
        # extend result with expand of replacement (for handling multiple expands in a single rule)
        expanded.extend(sai_expand(prelude + value + postlude))

    return expanded
