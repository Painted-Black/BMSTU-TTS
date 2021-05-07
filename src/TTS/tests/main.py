import unittest

import tests.syllable_unit_test
import tests.letter_phoneme_transcriptor_test
import tests.phoneme_allophone_transcriptor_test


if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_runner = unittest.TextTestRunner()

    syllable_suite = test_loader.loadTestsFromModule(tests.syllable_unit_test)
    lpt_suite = test_loader.loadTestsFromModule(tests.letter_phoneme_transcriptor_test)
    pat_suite = test_loader.loadTestsFromModule(tests.phoneme_allophone_transcriptor_test)

    test_runner.run(syllable_suite)
    #test_runner.run(lpt_suite)
    #test_runner.run(pat_suite)
    # unittest.main()
