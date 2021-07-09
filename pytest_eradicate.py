import pytest
import eradicate
from io import StringIO

__version__ = '0.0.6'

HISTKEY = "eradicate/mtimes"


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption('--eradicate', action='store_true',
                    help="run eradicate on files")
    group.addoption('--aggressive', action='store_true', default=False,
                    help="Make more aggressive changes. This may result in false positives")
    group.addoption(
        '--whitelist',
        action="store",
        help=('String of "#" separated comment beginnings to whitelist. '
              'Single parts are interpreted as regex. '
              'OVERWRITING the default whitelist: {}').format(
                  eradicate.Eradicator.DEFAULT_WHITELIST))
    group.addoption(
        '--whitelist-extend',
        action="store",
        help=('String of "#" separated comment beginnings to whitelist '
              'Single parts are interpreted as regex. '
              'Overwrites --whitelist. '
              'EXTENDING the default whitelist: {} ').format(
                  eradicate.Eradicator.DEFAULT_WHITELIST))


def pytest_sessionstart(session):
    config = session.config
    if config.option.eradicate:
        config._eradicatemtimes = config.cache.get(HISTKEY, {})
        config._eradictor = eradicate.Eradicator()

        class Args(object):
            in_place = False
            aggressive = config.option.aggressive
            if config.option.whitelist and config.option.whitelist_extend:
                raise pytest.Collector.CollectError(
                    "Options --whitelist and --whitelist-extend are mutually exclusive"
                )
            whitelist = config.option.whitelist
            whitelist_extend = config.option.whitelist_extend

        config._eradicator_args = Args()

def pytest_collect_file(path, parent):
    config = parent.config
    if config.option.eradicate and path.ext == '.py':
        if hasattr(EradicateItem, "from_parent"):
            return EradicateItem.from_parent(parent, fspath=path)
        else:
            return EradicateItem(parent, path)


def pytest_sessionfinish(session):
    config = session.config
    if hasattr(config, "_eradicatemtimes"):
        config.cache.set(HISTKEY, config._eradicatemtimes)


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "eradicate(name): mark eradicate tests"
    )

class EradicateError(Exception):
    """ indicates an error during eradicate checks. """


class EradicateItem(pytest.Item, pytest.File):

    def __init__(self, parent, fspath):
        super(EradicateItem, self).__init__(fspath, parent)
        self.add_marker("eradicate")

    def setup(self):
        eradicatemtimes = self.config._eradicatemtimes
        self._eradicatemtime = self.fspath.mtime()
        old = eradicatemtimes.get(str(self.fspath), (0, []))
        if old == (self._eradicatemtime, []):
            pytest.skip("file(s) previously passed eradicate checks")

    def runtest(self):
        out = StringIO()

        self.session.config._eradicator.fix_file(
            str(self.fspath), self.session.config._eradicator_args, out)

        out.seek(0)
        errors = out.read()

        if errors:
            raise EradicateError(errors, 'error')
        # update mtime only if test passed
        # otherwise failures would not be re-run next time
        self.config._eradicatemtimes[str(self.fspath)] = (self._eradicatemtime, [])

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(EradicateError):
            return excinfo.value.args[0]
        return super(EradicateItem, self).repr_failure(excinfo)

    def reportinfo(self):
        return self.fspath, -1, "Commented out code found"
