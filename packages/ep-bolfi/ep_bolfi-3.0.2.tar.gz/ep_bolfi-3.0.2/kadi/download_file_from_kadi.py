#!/usr/bin/env python
import xmlhelpy

from kadi_apy.lib.core import KadiManager, Record


@xmlhelpy.command(version='1.0')
@xmlhelpy.argument(
    'record',
    default=None,
    param_type=xmlhelpy.Integer,
    description="Permanent identifier of the record."
)
@xmlhelpy.argument(
    'file',
    default=None,
    param_type=xmlhelpy.String,
    description="Name of the file to download."
)
def download_file_from_kadi(record, file):
    """Downloads a file from a Kadi4Mat instance (see ~/.kadiconfig)."""
    manager = KadiManager()
    record_handle = Record(manager, id=record, create=False)
    file_id = record_handle.get_file_id(file)
    record_handle.download_file(file_id, file)


if __name__ == '__main__':
    download_file_from_kadi()
