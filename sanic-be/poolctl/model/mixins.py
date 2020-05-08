"""
Mixin classes for the poolctl model.

"""
from __future__ import annotations

from typing import Union, Optional, BinaryIO
import os
import pickle
from pathlib import PosixPath

from sanic.log import logger as log
from poolctl.utils.misc import typeof, nameof

OptionalPathOrOpenFileT = Union[BinaryIO, str, PosixPath, None]


class FileNotProvided(Exception):
    """Raise when persistence-related calls have no OptionalPathOrOpenFileT
    argument provided."""


class PersistMixin(object):
    # must be set for file-less persistence-related calls to succeed
    persistent_file: OptionalPathOrOpenFileT = None
    instance: Optional[PersistMixin] = None

    @classmethod
    async def from_persistent_data(cls, file: OptionalPathOrOpenFileT = None, **kw) -> PersistMixin:
        assert not cls.instance, f'{cls.__name__} singleton instantiation violation'
        cls.instance = await cls._private_from_persistent_data(file, **kw)
        return cls.instance

    @classmethod
    async def _private_from_persistent_data(cls, file: OptionalPathOrOpenFileT = None, **kw) -> PersistMixin:

        file = file if file else cls.persistent_file
        if not file:
            raise FileNotProvided('neither in %.persistent_file nor in this call', cls.__name__)

        if hasattr(file, 'read'):  # is a stream
            if hasattr(file, 'seek'):
                file.seek(0)
            pickled_binary = file.read()
            log.debug('Loaded %s from open file %r', nameof(cls), file)
            return await cls._from_persistent_data(pickle.loads(pickled_binary), **kw)

        # path exists:
        if os.path.exists(file):
            with open(file, 'rb') as fd:
                pickled_binary = fd.read()
                log.debug('Read %s from file %s', nameof(cls), file)
                return await cls._from_persistent_data(
                    pickle.loads(pickled_binary) if pickled_binary else None,
                    **kw)

        # when path does not exist:
        log.debug('No persistence source available (yet) for %s', nameof(cls))
        return await cls._from_persistent_data(None)

    @classmethod
    async def _from_persistent_data(cls, data: Optional[dict], **kw: dict) -> PersistMixin:
        raise NotImplementedError('abstract')

    def __init__(self):
        self._dirty = False

    def set_clean(self):
        self._dirty = False

    def is_dirty(self):
        return self._dirty

    def persistent_data(self) -> Optional[dict]:
        if not self._dirty:
            return None
        return self._persistent_data()

    def _persistent_data(self) -> dict:
        raise NotImplementedError('abstract')

    async def persist(self, file: OptionalPathOrOpenFileT = None) -> None:
        if not self._dirty:
            log.debug('%s collection NOT dirty - skip persistence', typeof(self))
            return

        file = file if file else self.persistent_file
        if not file:
            raise FileNotProvided('neither in %.persistent_file nor in this call', typeof(self))

        pickled_data = pickle.dumps(self._persistent_data())
        log.info('%s collection IS dirty - saving...', typeof(self))

        # Consider using async write if the data becomes larger than say 16 KBytes
        if hasattr(file, 'write'):
            if hasattr(file, 'seek'):
                file.seek(0)  # rewind to start if possible
            file.write(pickled_data)
            if hasattr(file, 'truncate'):
                file.truncate()  # make sure we drop old stuff if any
            self.set_clean()
            return

        with open(file, 'wb') as fd:
            fd.write(pickled_data)
        self.set_clean()
