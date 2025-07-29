#!/usr/bin/env python

import argparse
import logging
from pathlib import Path
import sys
from dataclasses import dataclass

from cyclopts import App, Parameter
import gcsfs


@dataclass
class Config:
    threads: int = 3
    bounds: list[float] | None = None
    resolution: float | None = None
    dtype: str | None = None
    resampling: str | None = None
    nodata_per_band: bool = False
    list: bool = False
    outdir: str | None = None
    outname: str | None = None
    align_to_blocks: bool = True
    chunk_timeout: int = 300
    blocks_per_job: int = 1
    debug: bool = False


from get_result.vrtconverter import VrtResultConverter
from get_result.zarrconverter import ZarrResultConverter


logging.basicConfig(format='%(levelname)s:%(asctime)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# todo:
#  - error on unsuported args for zarr
#  - don't overwrite output file
#  - set bandnames
#  - s11-production-dprof-cache/Deforestation/deforestation_filtered/deforestation_filtered_v2.zarr does not work as input


app = App()


@app.default
def get_result(
        threads: int = 3,
        bounds: tuple[float, float, float, float] | None = None,
        resolution: float | None = None,
        dtype: str | None = None,
        resampling: str | None = None,
        nodata_per_band: bool = False,
        list: bool = False,
        outdir: str | None = None,
        outname: str | None = None,
        align_to_blocks: bool = True,
        chunk_timeout: int = 300,
        blocks_per_job: int = 1,
        debug: bool = False,
        *sources: str,
):
    """Download and process raster data from Google Cloud Storage.

    Parameters:
        source (list[str]): Bucket + uri where the result is stored; format: "bucket/uri/to/data" or "bucket/resultnumber"
        threads (int): Number of simultaneous download threads to use
        bounds (list[float] | None): Output bounds (minx miny maxx maxy)
        resolution (float | None): Output resolution (in decimal degrees)
        dtype (str | None): Output dtype
        resampling (str | None): Resampling algorithm (any of nearest, bilinear, cubic, cubicspline, lanczos, average, mode)
        nodata_per_band (bool): When true, propagate a separate nodata value for each band, instead of using the nodata value from the first band for all bands
        list (bool): Print a list of vrts of this result, then exit
        outdir (str | None): Output folder. Cannot be used together with --outname; default output filename(s) are used
        outname (str | None): Output file name. Cannot be used together with --outdir
        align_to_blocks (bool): Align output bounds to source blocks (faster but bounds might change)
        chunk_timeout (int): Timeout to read a single output chunk (in seconds)
        blocks_per_job (int): Approximate number of blocks per job
        debug (bool): Enable debug logging
        sources: one or multiple source uri's. A source uri takes the form "bucket/uri/to/data" or "bucket/resultnumber"
    """
    if debug:
        logger.setLevel(logging.DEBUG)

    if outdir and outname:
        raise RuntimeError('Cannot specify both --outdir and --outname.')

    config = Config(threads=threads, bounds=bounds, resolution=resolution, dtype=dtype,
        resampling=resampling, nodata_per_band=nodata_per_band, list=list, outdir=outdir,
        outname=outname, align_to_blocks=align_to_blocks, chunk_timeout=chunk_timeout,
        blocks_per_job=blocks_per_job, debug=debug)

    for source_path in sources:
        bucket, uri = source_path.split('/', maxsplit=1)

        if '.zarr' in uri:
            if uri.endswith('.zarr'):
                uri = f'{uri}/result'
            zarr_converter = ZarrResultConverter(f'gs://{bucket}/{uri}', config)
            zarr_converter.convert()

        else:
            try:
                result_number = f'{int(uri):06d}'
            except ValueError:
                vrt_converter = VrtResultConverter(f'{bucket}/{uri}', config)
                vrt_converter.convert()
            else:
                gcs = gcsfs.GCSFileSystem()

                vrts = [Path(f) for f in gcs.ls(f'{bucket}/{result_number}/', detail=False) if
                        f.endswith('.vrt')]

                print(f'Found {len(vrts)} vrts:')
                for vrt in vrts:
                    print(vrt)

                if list:
                    sys.exit()

                for vrt in vrts:
                    vrt_converter = VrtResultConverter(str(vrt), config)
                    vrt_converter.convert()


def main():
    app()

if __name__ == "__main__":
    main()


# def main():
#     app()
#     parser = argparse.ArgumentParser()
#     parser.add_argument('source', type=str, nargs='+',
#                         help='bucket + uri where the result is stored; format: "bucket/uri/to/data" or "bucket/resultnumber"')
#     # parser.add_argument('dataset', type=str,
#     #                     help='number of the dprof result, or key to zarr')
#     parser.add_argument('--threads', type=int, required=False, default=3,
#                         help='number of simultaneous download threads to use')
#     parser.add_argument('--bounds', type=float, nargs=4, required=False,
#                         help='output bounds (minx miny maxx maxy)')
#     parser.add_argument('--resolution', type=float, required=False,
#                         help='output resolution (in decimal degrees')
#     parser.add_argument('--dtype', type=str, required=False,
#                         help='output dtype')
#     parser.add_argument('--resampling', type=str, required=False,
#                         help='resampling algorithm (any of nearest, bilinear, cubic, cubicspline, '
#                              'lanczos, average, mode)')
#     parser.add_argument('--nodata-per-band', action='store_true',
#                         help='when true, propagate a separate nodata value for each band, instead '
#                              'of using the nodata value from the first band for all bands, '
#                              'assuming that it is the same for the whole file. This is slightly '
#                              'slower with result vrts with many bands.')
#     parser.add_argument('--list', action='store_true',
#                         help='print a list of vrts of this result, then exit')
#     parser.add_argument('--outdir', type=str, required=False,
#                         help='output folder. Cannot be used together with --outname; '
#                              'default output filename(s) are used.')
#     parser.add_argument('--outname', type=str, required=False,
#                         help='output file name. Cannot be used together with --outdir.')
#     parser.add_argument('--align-to-blocks', default=True, action=argparse.BooleanOptionalAction,
#                         help='align output bounds to source blocks (faster but bounds might change)')
#     parser.add_argument('--chunk-timeout', type=int, default=300,
#                         help='timeout to read a single output chunk (in seconds).')
#     parser.add_argument('--blocks-per-job', type=int, default=1, required=False,
#                         help='approximate number of blocks per job. Default: 1')
#     parser.add_argument('--debug', action='store_true',
#                         help='enable debug logging.')
#
#     args = parser.parse_args()
#     list_vrts = args.list
#     threads = args.threads
#     sources = args.source
#     resolution = args.resolution
#     resampling = args.resampling
#     nodata_per_band = args.nodata_per_band
#
#     print("debug:", args.debug)
#
#     if args.debug:
#         logger.setLevel(logging.DEBUG)
#
#     if args.outdir and args.outname:
#         raise RuntimeError('Cannot specify both --outdir and --outname.')
#
#     for source in sources:
#         bucket, uri = source.split('/', maxsplit=1)
#
#         if '.zarr' in uri:
#             # if no group specified, use the defaul 'result' group
#             if uri.endswith('.zarr'):
#                 uri = f'{uri}/result'
#             zarr_converter = ZarrResultConverter(f'gs://{bucket}/{uri}', args)
#             zarr_converter.convert()
#
#         else:
#             try:
#                 result_number = f'{int(uri):06d}'
#             except ValueError:
#                 # last part cannot be parsed as int, so it's not a dprof deliverable result
#                 vrt_converter = VrtResultConverter(f'{bucket}/{uri}', args)
#                 vrt_converter.convert()
#             else:
#                 gcs = gcsfs.GCSFileSystem()
#
#                 vrts = [Path(f) for f in gcs.ls(f'{bucket}/{result_number}/', detail=False)
#                         if f.endswith('.vrt')]
#
#                 print(f'Found {len(vrts)} vrts:')
#                 for vrt in vrts:
#                     print(vrt)
#
#                 if list_vrts:
#                     sys.exit()
#
#                 for vrt in vrts:
#                     vrt_converter = VrtResultConverter(str(vrt), args)
#                     vrt_converter.convert()
#
#
# if __name__ == "__main__":
#     main()
