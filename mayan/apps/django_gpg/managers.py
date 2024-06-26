import io
import logging
import shutil

from django.db import models

from mayan.apps.storage.utils import NamedTemporaryFile

from .classes import GPGBackend, KeyStub, SignatureVerification
from .exceptions import (
    DecryptionError, KeyDoesNotExist, KeyFetchingError, VerificationError
)
from .literals import KEY_TYPE_PUBLIC, KEY_TYPE_SECRET
from .settings import setting_keyserver

logger = logging.getLogger(name=__name__)


class KeyManager(models.Manager):
    def _preload_keys(
        self, all_keys=False, key_fingerprint=None, key_id=None
    ):
        # Preload keys.
        if all_keys:
            logger.debug(msg='preloading all keys')
            keys = self.values()
        elif key_fingerprint:
            logger.debug('preloading key fingerprint: %s', key_fingerprint)
            keys = self.filter(fingerprint=key_fingerprint).values()
            if not keys:
                logger.debug(
                    'key fingerprint %s not found', key_fingerprint
                )
                raise KeyDoesNotExist(
                    'Specified key for verification not found'
                )
        elif key_id:
            logger.debug('preloading key id: %s', key_id)
            keys = self.filter(fingerprint__endswith=key_id).values()
            if keys:
                logger.debug('key id %s impored', key_id)
            else:
                logger.debug('key id %s not found', key_id)
        else:
            keys = ()

        return keys

    def decrypt_file(
        self, file_object, all_keys=False, key_fingerprint=None, key_id=None
    ):
        keys = self._preload_keys(
            all_keys=all_keys, key_fingerprint=key_fingerprint, key_id=key_id
        )

        decrypt_result = GPGBackend.get_instance().decrypt_file(
            file_object=file_object, keys=keys
        )

        logger.debug('decrypt_result.status: %s', decrypt_result.status)

        if not decrypt_result.status or decrypt_result.status == 'no data was provided':
            raise DecryptionError('Unable to decrypt file')

        file_object.close()

        return io.BytesIO(initial_bytes=decrypt_result.data)

    def private_keys(self):
        return self.filter(key_type=KEY_TYPE_SECRET)

    def public_keys(self):
        return self.filter(key_type=KEY_TYPE_PUBLIC)

    def receive_key(self, key_id):
        key_data = GPGBackend.get_instance().recv_keys(
            key_id=key_id, keyserver=setting_keyserver.value
        )

        if not key_data:
            raise KeyFetchingError('No key found')
        else:
            return self.create(key_data=key_data)

    def search(self, query):
        key_data_list = GPGBackend.get_instance().search_keys(
            keyserver=setting_keyserver.value, query=query
        )

        result = []
        for key_data in key_data_list:
            result.append(
                KeyStub(raw=key_data)
            )

        return result

    def verify_file(
        self, file_object, signature_file=None, all_keys=False,
        key_fingerprint=None, key_id=None
    ):
        keys = self._preload_keys(
            all_keys=all_keys, key_fingerprint=key_fingerprint,
            key_id=key_id
        )

        if signature_file:
            # Save the original data and invert the argument order:
            # signature first, file second.
            with NamedTemporaryFile() as temporary_file_object:
                shutil.copyfileobj(
                    fsrc=file_object, fdst=temporary_file_object
                )
                temporary_file_object.seek(0)

                with NamedTemporaryFile() as temporary_signature_file_object:
                    shutil.copyfileobj(
                        fsrc=signature_file,
                        fdst=temporary_signature_file_object
                    )
                    temporary_signature_file_object.seek(0)
                    signature_file.seek(0)
                    verify_result = GPGBackend.get_instance().verify_file(
                        data_filename=temporary_file_object.name,
                        file_object=temporary_signature_file_object,
                        keys=keys
                    )
        else:
            verify_result = GPGBackend.get_instance().verify_file(
                file_object=file_object, keys=keys
            )

        logger.debug('verify_result.status: %s', verify_result.status)

        if verify_result:
            # Signed and key present.
            logger.debug(msg='signed and key present')
            return SignatureVerification(verify_result.__dict__)
        elif verify_result.status == 'no public key' and not (key_fingerprint or all_keys or key_id):
            # Signed but key not present, retry with key fetch.
            logger.debug(msg='no public key')
            file_object.seek(0)
            return self.verify_file(
                file_object=file_object, signature_file=signature_file,
                key_id=verify_result.key_id
            )
        elif verify_result.key_id:
            # Signed, retried and key still not found.
            logger.debug(msg='signed, retried and key still not found')
            return SignatureVerification(verify_result.__dict__)
        else:
            logger.debug(msg='file not signed')
            raise VerificationError('File not signed')
