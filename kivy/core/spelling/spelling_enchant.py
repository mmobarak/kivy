'''
Enchant Spelling
================

Implementation spelling backend based on enchant.

.. warning:: pyenchant doesn't have dedicated build anymore for Windows/x64.
             See https://github.com/kivy/kivy/issues/5816 for more information
'''


import enchant

from kivy.core.spelling import SpellingBase, NoSuchLangError


class SpellingEnchant(SpellingBase):
    '''
    Spelling backend based on the enchant library.
    '''

    def __init__(self, language=None):
        self._language = None
        super(SpellingEnchant, self).__init__(language)

    def select_language(self, language):
        try:
            self._language = enchant.Dict(language)
        except enchant.DictNotFoundError:
            err = 'Enchant Backend: No language for "%s"' % (language, )
            raise NoSuchLangError(err)

    def list_languages(self):
        # Note: We do NOT return enchant.list_dicts because that also returns
        #       the enchant dict objects and not only the language identifiers.
        return enchant.list_languages()

    def check(self, word):
        if not word:
            return None
        return self._language.check(word)

    def suggest(self, fragment):
        suggestions = self._language.suggest(fragment)
        # Don't show suggestions that are invalid
        suggestions = [s for s in suggestions if self.check(s)]
        return suggestions
