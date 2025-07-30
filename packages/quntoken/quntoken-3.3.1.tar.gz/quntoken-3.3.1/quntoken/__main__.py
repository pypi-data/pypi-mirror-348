import sys
import argparse
import fileinput
from pathlib import Path
from io import TextIOWrapper

try:
    from quntoken.version import __version__
except ModuleNotFoundError:
    from version import __version__
from quntoken import tokenize

FORMATS = {'json', 'raw', 'tsv', 'xml', 'spl'}
MODES = {'sentence', 'token'}


def get_args():
    """Handling of commandline arguments.
    """
    pars = argparse.ArgumentParser(description=__doc__)
    pars.add_argument(
        '-f',
        '--form',
        help='Valid formats: json, tsv, xml and spl (sentence per line, ignores mode). Default format: tsv.',
        default='tsv',
        choices=sorted(FORMATS)
    )
    pars.add_argument(
        '-m',
        '--mode',
        help='Modes: sentence or token (does not apply for form=spl). Default: token',
        default='token',
        choices=sorted(MODES)
    )
    conll_text_arg = \
        pars.add_argument(
            '-c',
            '--conll-text',
            help='Add CoNLL text metafield to contain the detokenized sentence '
                 '(only for mode == token and format == tsv). Default: False',
            default=False,
            action='store_true'
        )
    pars.add_argument(
        '-i',
        '--input',
        help='One or more input files.'
             '(\'-\' for STDIN) Default: STDIN',
        default='-',
        nargs='+'
    )
    pars.add_argument(
        '-o',
        '--output',
        help='One output file.'
             '(\'-\' for STDOUT) Default: STDOUT',
        default='-'
    )
    pars.add_argument(
        '-s',
        '--separate-lines',
        help='Separate processing of each line.'
             '(Starts new tokenizer for each line.) Default: False',
        action='store_true'
    )
    pars.add_argument(
        '-w',
        '--word-break',
        help='Eliminate word break from end of lines.',
        action='store_true'
    )
    pars.add_argument(
        '-v',
        '--version',
        action='version',
        version=__version__
    )
    res = vars(pars.parse_args())
    if res['conll_text'] and (res['mode'] != 'token' or res['form'] != 'tsv'):
        raise argparse.ArgumentError(conll_text_arg, 'can only be set if mode == token and form == tsv !')

    return res


class WriteFileOrStdout:
    """Unified opener for output file and STDOUT"""

    def __init__(self, path, mode, encoding, **kwargs):
        if mode not in {'w', 'wb'}:
            raise ValueError(f"Mode ({mode}) is invalid! Options are 'w' or 'wb' !")
        self._mode = mode

        self._kwargs = kwargs
        if path == '-':
            self._path = None
            if self._mode == 'w':
                self._fh = TextIOWrapper(sys.stdout.buffer, encoding=encoding, **self._kwargs)
            else:
                self._fh = sys.stdout.buffer
        else:
            self._path = Path(path)
            self._fh = None

    def __enter__(self):
        if self._fh is None:
            self._fh = open(self._path, self._mode, **self._kwargs)
        return self._fh

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._fh is not None:
            self._fh.close()


def main():
    """Command line entry point.
    """
    args = get_args()
    input_filename = args.pop('input')
    output_filename = args.pop('output')
    separate_lines = args.pop('separate_lines')
    # The openhook parameter is compatible with a wide range of Pyhton versions.
    # From 3.10 it is enough to use encoding='UTF-8' directly!
    with fileinput.input(input_filename,
                         openhook=lambda filename, mode: open(filename, mode, encoding='UTF-8')) as inp_fh, \
            WriteFileOrStdout(output_filename, mode='w', encoding='UTF-8') as out_fh:
        if separate_lines:
            for line in inp_fh:
                out_fh.writelines(tokenize(line, **args))
        else:
            for line in tokenize(inp_fh, **args):
                print(line, end='', file=out_fh)


if __name__ == '__main__':
    main()
