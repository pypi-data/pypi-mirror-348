import sys
import argparse
import fileinput
from typing import Union
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


class OpenFileOrSTDStreams:
    """Unified opener for output files and STDStreams (STDIN and STDOUT)"""

    # From 3.10 it should be enough to use encoding='UTF-8' directly in fileinput.input()!

    def __init__(self, path: Union[list, str], mode='r', *, encoding=None, **kwargs):
        allowed_modes = {'r', 'w'}
        if mode not in allowed_modes:
            raise ValueError(f"Mode ({mode}) is invalid! Options are {', '.join(sorted(allowed_modes))} !")
        self._mode = mode

        if isinstance(path, list) and mode != 'r':
            raise ValueError("Multiple files can be opened for reading only (mode='r')!")

        if encoding is None:
            raise ValueError('Encoding must be specified!')
        self._encoding = encoding

        self._path = path
        self._kwargs = kwargs
        self._fh = None
        self._close = False
        if path == '-':
            # There is no way to set STDOUT or specify the encoding for STDIN in fileinput.input()
            # to force encoding even when no UTF-8 locale is set (e.g. in Docker containers)
            if self._mode == 'r':
                self._fh = TextIOWrapper(sys.stdin.buffer, encoding=self._encoding, **self._kwargs)
            elif self._mode == 'w':
                self._fh = TextIOWrapper(sys.stdout.buffer, encoding=self._encoding, **self._kwargs)

    def __enter__(self):
        if self._fh is None:
            if self._mode == 'r':  # Reading one or more files (fileinput closes itself automatically)
                self._fh = fileinput.input(self._path,
                                           openhook=
                                           lambda filename, mode: open(filename, mode, encoding=self._encoding))
            else:  # Writing to file
                self._fh = open(self._path, self._mode, encoding=self._encoding, **self._kwargs)
                self._close = True
        # Reading from and writing to STDIN/STDOUT has already been set up
        return self._fh

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._close:
            self._fh.close()


def main():
    """Command line entry point.
    """
    args = get_args()
    input_filename = args.pop('input')
    output_filename = args.pop('output')
    separate_lines = args.pop('separate_lines')
    with OpenFileOrSTDStreams(input_filename, encoding='UTF-8') as inp_fh, \
            OpenFileOrSTDStreams(output_filename, mode='w', encoding='UTF-8') as out_fh:
        if separate_lines:
            for line in inp_fh:
                out_fh.writelines(tokenize(line, **args))
        else:
            for line in tokenize(inp_fh, **args):
                print(line, end='', file=out_fh)


if __name__ == '__main__':
    main()
