from setuptools import setup
try:
    from Cython.Build import cythonize
except ModuleNotFoundError:
    pass
from pathlib import Path
from setuptools import find_packages
import os

class SourceInfo:

    class PYXPath:

        def __init__(self, module, path):
            self.module = module
            self.path = path

        def make_ext(self):
            g = {}
            with open(f"{self.path}bld") as f: # Assume project root.
                exec(f.read(), g)
            return g['make_ext'](self.module, self.path)

    def __init__(self, rootdir):
        def addextpaths(dirpath, moduleprefix, suffix = '.pyx'):
            for name in sorted(os.listdir(os.path.join(rootdir, dirpath))):
                if name.endswith(suffix):
                    module = f"{moduleprefix}{name[:-len(suffix)]}"
                    if module not in extpaths:
                        extpaths[module] = self.PYXPath(module, os.path.join(dirpath, name))
        self.packages = find_packages(rootdir)
        extpaths = {}
        addextpaths('.', '')
        for package in self.packages:
            addextpaths(package.replace('.', os.sep), f"{package}.")
        self.extpaths = extpaths.values()

    def setup_kwargs(self):
        kwargs = dict(packages = self.packages)
        try:
            kwargs['long_description'] = Path('README.md').read_text()
            kwargs['long_description_content_type'] = 'text/markdown'
        except FileNotFoundError:
            pass
        if self.extpaths:
            kwargs['ext_modules'] = cythonize([path.make_ext() for path in self.extpaths])
        return kwargs

sourceinfo = SourceInfo('.')
setup(
    name = 'pym2149',
    version = '39',
    description = 'YM2149 emulator supporting YM files, OSC to JACK, PortAudio, WAV',
    url = 'https://github.com/combatopera/pym2149',
    author = 'Andrzej Cichocki',
    author_email = '3613868+combatopera@users.noreply.github.com',
    py_modules = [],
    install_requires = ['aridity>=84', 'diapyr>=26', 'foyndation>=15', 'lagoon>=49', 'Lurlene>=13', 'minBlepy>=16', 'numpy>=2.0.2', 'outjack>=15', 'pyrbo>=18', 'splut>=4', 'timelyOSC>=4'],
    package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
    entry_points = {'console_scripts': ['bpmtool=pym2149.scripts.bpmtool:main', 'dosound2jack=pym2149.scripts.dosound2jack:main', 'dosound2txt=pym2149.scripts.dosound2txt:main', 'dosound2wav=pym2149.scripts.dosound2wav:main', 'dsd2wav=pym2149.scripts.dsd2wav:main', 'lc2jack=pym2149.scripts.lc2jack:main', 'lc2portaudio=pym2149.scripts.lc2portaudio:main', 'lc2txt=pym2149.scripts.lc2txt:main', 'lc2wav=pym2149.scripts.lc2wav:main', 'ym2jack=pym2149.scripts.ym2jack:main', 'ym2portaudio=pym2149.scripts.ym2portaudio:main', 'ym2txt=pym2149.scripts.ym2txt:main', 'ym2wav=pym2149.scripts.ym2wav:main', 'mkdsd=ymtests.mkdsd:main']},
    **sourceinfo.setup_kwargs(),
)
