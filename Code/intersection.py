import re


def parse_helper(seq, start=0):
    tokens = []
    while start < len(seq):
        if seq[start] == "(":
            sub_seq, new_start = parse_helper(seq, start + 1)
            tokens.append(sub_seq)
            start = new_start
        elif seq[start] == ")":
            return tokens, start + 1
        elif seq[start] == ",":
            start += 1
        else:
            match = re.match(r"([a-zA-Z0-9_+]+)", seq[start:])
            if match:
                tokens.append(match.group(0))
                start += len(match.group(0))
            else:
                start += 1
    return tokens, start


def parse_sequence(seq):
    parsed, _ = parse_helper(seq, 0)
    return parsed


def intersect(seq1, seq2):
    if isinstance(seq1, list) and isinstance(seq2, list):
        intersected = []
        for item1 in seq1:
            for item2 in seq2:
                result = intersect(item1, item2)
                if result is not None and result not in intersected:
                    intersected.append(result)
        return intersected if intersected else None
    elif isinstance(seq1, str) and isinstance(seq2, str):
        if seq1 == seq2:
            return seq1
        else:
            return None
    return None


def format_sequence(seq):
    if isinstance(seq, list):
        result = []
        for item in seq:
            formatted_item = format_sequence(item)
            if formatted_item:
                result.append(formatted_item)
        return f"({','.join(result)})" if result else ""
    else:
        return seq


def rpst_intersect(seq1, seq2):
    parsed_seq1 = parse_sequence(seq1)
    parsed_seq2 = parse_sequence(seq2)

    intersection = intersect(parsed_seq1, parsed_seq2)
    result = format_sequence(intersection)
    return result


if __name__ == "__main__":
    # example:
    seq1 = "(ea_l1,X(->( ra_l1,nc_l1 )->(aa_l1, ca_l1,+(sp_l2,sw_l2,sc_l2))))"
    seq2 = "(ea_l1,da_l1, X(->( ra_l1,nc_l1, db_l2 ), ->(aa_l1, ca_l1,+(sp_l2,sw_l2,dc_l2))))"
    result = rpst_intersect(seq1, seq2)
    print(result)