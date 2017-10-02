import sys

from github import Github
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import FileHistory
from pygments.lexers.sql import SqlLexer

import definition
import parser
import tokenizer


class SQLGitHub:
    """Meta Component for SQLGitHub."""

    _PROMPT_STR = u"SQLGitHub> "

    def __init__(self, token):
        self._github = Github(token)
        self._parser = parser.SgParser(self._github)
        self._completer = WordCompleter(definition.COMMAND_TOKENS,
                                        ignore_case=True)

    def Execute(self, sql):
        tokens = tokenizer.SgTokenizer.Tokenize(sql)
        try:
            session = self._parser.Parse(tokens)
        except NotImplementedError:
            sys.stderr.write("Not implemented command tokens in SQL.\n")
        except SyntaxError:
            sys.stderr.write("SQL syntax incorrect.\n")
        else:
            result = session.Execute()
            print(result)
        

    def Start(self):
        while True:
            sql = prompt(self._PROMPT_STR,
                         history=FileHistory("history.txt"),
                         auto_suggest=AutoSuggestFromHistory(),
                         completer=self._completer,
                         lexer=SqlLexer)
            if sql in ["q", "exit"]:
                break
            self.Execute(sql)
