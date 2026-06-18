from hanzi_quiz_api.quiz import check_answer

def test_check_answer():
    correct_hanzi = '书'
    correct_pinyin = 'shū'

    hanzi_guess1 = '书'
    hanzi_guess2 = '苹果'
    hanzi_guess3 = ''
    hanzi_guess4 = None

    pinyin_guess1 = 'shū'
    pinyin_guess2 = 'shuǐ'
    pinyin_guess3 = ''
    pinyin_guess4 = None

    assert check_answer(correct_hanzi, correct_pinyin, hanzi_guess1, pinyin_guess1) == {'hanzi_correct': True, 'pinyin_correct': True}
    assert check_answer(correct_hanzi, correct_pinyin, hanzi_guess2, pinyin_guess1) == {'hanzi_correct': False, 'pinyin_correct': True}
    assert check_answer(correct_hanzi, correct_pinyin, hanzi_guess3, pinyin_guess1) == {'hanzi_correct': False, 'pinyin_correct': True}
    assert check_answer(correct_hanzi, correct_pinyin, hanzi_guess4, pinyin_guess1) == {'hanzi_correct': False, 'pinyin_correct': True}
    assert check_answer(correct_hanzi, correct_pinyin, hanzi_guess1, pinyin_guess2) == {'hanzi_correct': True, 'pinyin_correct': False}
    assert check_answer(correct_hanzi, correct_pinyin, hanzi_guess1, pinyin_guess3) == {'hanzi_correct': True, 'pinyin_correct': False}
    assert check_answer(correct_hanzi, correct_pinyin, hanzi_guess1, pinyin_guess4) == {'hanzi_correct': True, 'pinyin_correct': False}