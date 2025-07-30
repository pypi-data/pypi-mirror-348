from simpleworkspace.__lazyimporter__ import __LazyImporter__, __TYPE_CHECKING__
if(__TYPE_CHECKING__):
    from . import directory as _directory
    from . import file as _file
    from . import path as _path
    from .parsers import loader as _parsers
    from .audio import loader as _audio

directory: '_directory' = __LazyImporter__(__package__, '.directory')
file: '_file' = __LazyImporter__(__package__, '.file')
path: '_path' = __LazyImporter__(__package__, '.path')
parsers: '_parsers' = __LazyImporter__(__package__, '.parsers.loader')
audio: '_audio' = __LazyImporter__(__package__, '.audio.loader')
