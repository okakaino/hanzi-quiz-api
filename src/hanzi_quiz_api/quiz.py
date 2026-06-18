def check_answer(correct_hanzi: str, correct_pinyin: str,
                 hanzi_choice: str, pinyin_choice: str) -> dict:
    """Return which parts the user got right."""

    return {
        'hanzi_correct': hanzi_choice == correct_hanzi,
        'pinyin_correct': pinyin_choice == correct_pinyin
    }