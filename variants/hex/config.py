COLS = 'abcdefghijk'
VALID_HEXES = None  # заполняется при импорте


def _get_valid_hexes():
    from variants.hex.board import VALID_HEXES as VH
    return VH


def _parse_input(normalized_input):
    global VALID_HEXES
    if VALID_HEXES is None:
        VALID_HEXES = _get_valid_hexes()

    def label_to_qr(label):
        col_l = label[0]
        row_n = int(label[1:])
        q = COLS.index(col_l) - 5
        r = 6 - row_n
        if (q, r) in VALID_HEXES:
            return q, r
        return None

    if len(normalized_input) == 1:
        qr = label_to_qr(normalized_input[0])
        if qr:
            return qr
        return None

    elif len(normalized_input) == 2:
        from_qr = label_to_qr(normalized_input[0])
        to_qr   = label_to_qr(normalized_input[1])
        if from_qr and to_qr:
            return from_qr[0], from_qr[1], to_qr[0], to_qr[1]
        return None

    return None


params = {
    'input_max_number': 11,
    'input_max_letter': 11,
    'parse_input': _parse_input,
}