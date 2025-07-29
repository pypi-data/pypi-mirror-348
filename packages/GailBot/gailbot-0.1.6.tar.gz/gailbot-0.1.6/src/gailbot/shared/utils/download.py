# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-12 13:39:44
# @Last Modified by:   Muhammad Umair

import shutil
from typing import List
from tqdm.auto import tqdm
import requests
from zipfile import ZipFile
import os
import socket
from .logger import makelogger
from gailbot.pluginSuiteManager.S3BucketManager import S3BucketManager
from urllib.parse import urlparse
from typing import Optional, List

logger = makelogger("download")



def download_single_url(
    url: str,
    download_path: str,
    extract_root: str,
    s3_client,
    unzip: bool = True,
    true_extract: bool = False
) -> Optional[str]:
    """
    Download one S3 URL to download_path, unzip under extract_root, and
    return the extract directory (or extract_root if true_extract=True), 
    or the zip path if unzip=False, or None on error.
    """
    try:
        parsed = urlparse(url)
        bucket = parsed.netloc.split(".")[0]
        key = parsed.path.lstrip("/")
        name = os.path.splitext(os.path.basename(key))[0]

        local_zip = os.path.join(download_path, f"{name}.zip")
        os.makedirs(os.path.dirname(local_zip), exist_ok=True)

        logger.info("Downloading s3://%s/%s → %s", bucket, key, local_zip)
        s3_client.download_file(bucket, key, local_zip)
    except Exception as e:
        logger.error("Failed to download %s: %s", url, e, exc_info=True)
        return None

    if not unzip:
        return local_zip

    try:
        # always unzip into a temp subfolder first
        subfolder = os.path.join(extract_root, name)
        if os.path.exists(subfolder):
            shutil.rmtree(subfolder)
        os.makedirs(subfolder, exist_ok=True)

        with ZipFile(local_zip, "r") as zf:
            zf.extractall(subfolder)

        if true_extract:
            # move everything from subfolder → extract_root
            for item in os.listdir(subfolder):
                src = os.path.join(subfolder, item)
                dst = os.path.join(extract_root, item)
                # if dst already exists, overwrite or handle as needed
                if os.path.exists(dst):
                    if os.path.isdir(dst):
                        shutil.rmtree(dst)
                    else:
                        os.remove(dst)
                shutil.move(src, dst)
            shutil.rmtree(subfolder)
            logger.info("Flattened contents of %s into %s", name, extract_root)
            return extract_root
        else:
            logger.info("Extracted %s → %s", local_zip, subfolder)
            return subfolder

    except Exception as e:
        logger.error("Failed to extract %s: %s", local_zip, e, exc_info=True)
        return None

def download_from_urls(
    urls: List[str],
    download_dir: str,
    unzip: bool = True,
) -> List[str]:
    """
    Download a list of S3 URLs and return the list of extracted paths.
    """
    dataset_download_path = os.path.join(download_dir, "download")
    dataset_extract_path = download_dir

    # prepare dirs
    if os.path.isdir(dataset_download_path):
        shutil.rmtree(dataset_download_path)
    os.makedirs(dataset_download_path, exist_ok=True)
    os.makedirs(dataset_extract_path, exist_ok=True)

    s3 = S3BucketManager.get_instance().get_s3()

    extracted = []
    for url in urls:
        logger.info("Processing URL: %s", url)
        path = download_single_url(
            url,
            download_path=dataset_download_path,
            extract_root=dataset_extract_path,
            s3_client=s3,
            unzip=unzip
        )
        if path:
            extracted.append(path)

    return extracted


def is_internet_connected() -> bool:
    """
    True if connected to the internet, false otherwise
    """
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            sock.close()
        return True
    except OSError:
        pass
    return False
