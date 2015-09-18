# -*- coding: UTF-8 -*-

import logging
from collections import OrderedDict
from pydrive.drive import GoogleDrive
from apiclient.http import BatchHttpRequest
from uuid import uuid4

logger = logging.getLogger('pydrive_browser')


class PydriveBrowser(object):

    def __init__(self, gauth):
        self._pydrive = GoogleDrive(gauth)

    def list_files(self, path=None, q=None, fields=None, trashed = False): # dsadasdasdas
        drive = self._pydrive
        if not q:
            q = "'{path}' in parents and trashed={trashed}"
            kwargs = {'trashed': trashed}
            if path is None:
                kwargs['path'] = 'root'
            else:
                kwargs['path'] = path

            q = q.format(**kwargs)

        file_list = drive.ListFile({'q': q}).GetList()
        return file_list

    def get(self, file_ids, fields=None):

        self._pydrive.auth.Authorize()
        files = self._pydrive.auth.service.files()
        batch_response = OrderedDict()

        def batch_callback(request_id, response, exception):
            file_id = request_id.split('__', 2)[1]
            if exception:
                logger.error("Error on drive batch operation for %s: %s",
                             request_id, exception)
                batch_response[file_id] = {'exception': exception}
            else:
                batch_response[file_id] = response

        batch_request = BatchHttpRequest(callback=batch_callback)

        for file_id in file_ids:
            batch_request.add(
                files.get(fileId=file_id, fields=','.join(fields)),
                request_id='get__%s__%s' % (file_id, uuid4())
            )

        batch_request.execute()
        return batch_response

    def share(self, file_ids, emails, callback=None):
        """
        Share a list of files to a list of e-mails.
        """
        if not isinstance(file_ids, (list, tuple)):
            raise ValueError(
                "We are expecting a list of file_ids, not %s" % file_ids
            )

        if not isinstance(emails, (list, tuple)):
            raise ValueError(
                "We are expecting a list of emails, not %s" % emails
            )

        self._pydrive.auth.Authorize()
        perms = self._pydrive.auth.service.permissions()
        http = self._pydrive.auth.http
        batch_response = OrderedDict()

        def batch_callback(request_id, response, exception):
            file_id = request_id.split('__', 2)[1]
            if exception:
                logger.error("Error on drive batch operation for %s: %s",
                             request_id, exception)
                batch_response[file_id].update({'exception': exception})
            else:
                batch_response[file_id].update(response)

        batch_request = BatchHttpRequest(callback=batch_callback)

        for file_id in list(set(file_ids)):
            for email in list(set(emails)):
                kwargs = {
                    'fileId': file_id,
                    'body': {
                        'value': email,
                        'type': 'user',
                        'role': 'writer'
                    }
                }
                batch_id = 'share__%s__%s' % (file_id, uuid4())
                batch_request.add(perms.insert(**kwargs), request_id=batch_id)
                logger.info(
                    "Batch share request added with ID %s and data %s",
                    batch_id, kwargs
                )
                batch_response[file_id] = {'insert_kwargs': kwargs}

        batch_request.execute()
        return batch_response
