from cryptography.fernet import Fernet
from glob import glob
import json
import os
import pathlib
import tarfile
import time

import requests


class BBox:
    """
    A bounding box class for spatial filtering.

    Attributes
    ----------
    llx : float
        The longitude of the lower-left corner of the bounding box.
    lly : float
        The latitude of the lower-left corner of the bounding box.
    urx : float
        The longitude of the upper-right corner of the bounding box.
    ury : float
        The latitude of the upper-right corner of the bounding box.

    """

    def __init__(self, llx, lly, urx, ury):
        self.llx, self.lly, self.urx, self.ury = llx, lly, urx, ury

    @property
    def spatial_filter(self):
        """
        Returns a spatial filter for use with USGS EarthExplorer API.

        Returns
        -------
        dict
            A dictionary containing a spatial filter in JSON format, 
            consisting of the filter type 'mbr' (Minimum Bounding 
            Rectangle), the latitude and longitude of the lower-left 
            corner of the bounding box, and the latitude and longitude 
            of the upper-right corner of the bounding box.

        """
        return {
            'filterType': "mbr",
            'lowerLeft': {'latitude': self.lly, 'longitude': self.llx},
            'upperRight': {'latitude': self.ury, 'longitude': self.urx}}


class EarthExplorerDownloader:
    """
    A class for downloading data from the USGS EarthExplorer API.

    Attributes
    ----------
    dataset : str
        The name of the dataset to be downloaded.
    label : str
        A label for the downloaded data.
    bbox : BBox
        A bounding box object containing the geographic area to 
        download data for.
    start : str
        The start date for the temporal filter.
    end : str
        The end date for the temporal filter.

    """

    base_url = "https://m2m.cr.usgs.gov/api/api/json/stable/{endpoint}"
    product_filter = {
        'productName': 'C2 ARD Tile Surface Reflectance Bundle Download'}
    dld_file_tmpl = '{display_id}.tar'

    def __init__(self, dataset, label, bbox, start, end):
        self.api_key = None
        self.login()

        self.dataset, self.label = dataset, label
        self.bbox, self.start, self.end = bbox, start, end

        self.temporal_filter = {'start': start, 'end': end}
        self.acquisition_filter = self.temporal_filter

        self.path_tmpl = os.path.join(self.label, self.dld_file_tmpl)
        if not os.path.exists(label):
            os.makedirs(label)

        self._dataset_alias = None

    def get_ee_login_info(self, info_type):
        """
        Retrieves login information for the USGS EarthExplorer (EE) API.

        Parameters
        ----------
        info_type : str
            The type of login information to retrieve (either 'username' 
            or 'password').

        Returns
        -------
        str
            The login information requested.

        """
        # Generate and store key
        key_path = os.path.join(pathlib.Path.home(), '.ee_key')
        if not os.path.exists(key_path):
            print('Generating new key...')
            key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        fernet = Fernet(key)

        # Collect and store login info
        info_path = os.path.join(
            pathlib.Path.home(),
            '.ee_{}'.format(info_type))
        if not os.path.exists(info_path):
            info = input('Enter {}: '.format(info_type))
            with open(info_path, 'wb') as info_file:
                info_file.write(fernet.encrypt(bytes(info, 'utf-8')))
        with open(info_path, 'rb') as info_file:
            return fernet.decrypt(info_file.read()).decode("utf-8")

    def login(self):
        """
        Logs in to the EE API using the specified username and password.

        Returns
        -------
        None

        """
        if self.api_key is None:
            login_payload = {
                'username': self.get_ee_login_info('username'),
                'password': self.get_ee_login_info('password')}
            self.api_key = self.post("login", login_payload)
            print('Login Successful')

    @property
    def headers(self):
        if self.api_key is None:
            return None
        return {'X-Auth-Token': self.api_key}

    def logout(self):
        """
        Logs out of the EE API

        Returns
        -------
        None

        """
        self.post("logout", None)
        print("Logged Out\n\n")

    def post(self, endpoint, data):
        """
        Sends a POST request to the given endpoint with the provided 
        data.

        Parameters
        ----------
        endpoint : str
            The endpoint to send the request to.
        data : dict
            A dictionary containing the data to be sent with the 
            request.

        Returns
        -------
        dict
            A dictionary containing the data returned from the server.

        """
        # Send POST requests
        url = self.base_url.format(endpoint=endpoint)
        response = requests.post(url, json.dumps(data), headers=self.headers)

        # Raise any HTTP Errors
        response.raise_for_status()

        # Return data
        return response.json()['data']

    @property
    def dataset_alias(self):
        """
        Returns the dataset alias for the given dataset.

        If dataset alias is already set, returns the same, otherwise 
        searches for the dataset that matches the given dataset name, 
        spatial and temporal filters, and sets the dataset alias
        based on the first matching dataset.

        Returns:
        --------
        str:
            The dataset alias for the given dataset, spatial and 
            temporal filters.

        """
        if self._dataset_alias is None:
            print("Searching datasets...")
            params = {
                'datasetName': self.dataset,
                'spatialFilter': self.bbox.spatial_filter,
                'temporalFilter': self.temporal_filter}
            datasets = self.post("dataset-search", params)

            # Get a single dataset alias
            if len(datasets) > 1:
                print(datasets)
                raise ValueError('Multiple datasets found - refine search.')
            self._dataset_alias = datasets[0]['datasetAlias']

            print('Using dataset alias: {}'.format(self._dataset_alias))
        return self._dataset_alias

    def find_scene_ids(self):
        """
        Searches for scenes of the dataset associated with the given 
        dataset alias and returns the details of all the scenes found 
        within the specified bounding box and acquisition filters.

        Returns:
        --------
        scenes : dict
            A dictionary containing details of all the scenes found within the specified
            bounding box and acquisition filters.

        """
        params = {
            'datasetName': self.dataset_alias,
            'startingNumber': 1,

            'sceneFilter': {
                'spatialFilter': self.bbox.spatial_filter,
                'acquisitionFilter': self.acquisition_filter}}

        print("Searching scenes...")
        scenes = self.post("scene-search", params)
        print('Found {} scenes'.format(scenes['recordsReturned']))
        return scenes

    def find_available_product_info(self):
        """
        Find and return a list of available products for the selected 
        dataset.

        Returns
        -------
        list of dict
            A list of available product information with keys: 
            'entityId' and 'productId'

        Raises
        ------
        ValueError
            If no available products are found.

        """
        scenes = self.find_scene_ids()
        params = {
            'datasetName': self.dataset_alias,
            'entityIds': [scene['entityId'] for scene in scenes['results']]}
        products = self.post("download-options", params)

        # Aggregate a list of available products
        product_info = []
        for product in products:
            # Make sure the product is available for this scene
            if product['available'] == True or product['proxied'] == True:
                product_info.append({
                    'entityId': product['entityId'],
                    'productId': product['id']})
        if not product_info:
            raise ValueError('No available products.')
        return product_info

    def submit_download_request(self):
        """
        Submits a download request for the available product information.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If no products found with the specified boudnaries.

        """
        product_info = self.find_available_product_info()
        # Did we find products?
        if product_info:
            # Request downloads
            params = {
                'downloads': product_info,
                'label': self.label}
            downloads = self.post("download-request", params)
            print('Downloads staging...')
        else:
            raise ValueError(
                'No products found with the specified boundaries.')

    def check_download_status(self):
        """
        Retrieve the status of a download request.

        Returns
        -------
        dict
            A dictionary with information about the download request, 
            including download progress and available URLs for 
            downloading the requested files.
        """
        params = {'label': self.label}
        downloads = self.post("download-retrieve", params)
        return downloads

    def wait_for_available_downloads(self, timeout=None):
        """
        Waits for all requested downloads to become available.

        Parameters
        ----------
        timeout : int, optional
            The maximum amount of time (in deconds) to wait for the 
            downloads. If None, waits indefinitely.

        Returns
        -------
        dict 
            A dictionary containing information about the downloaded 
            products.

        """
        keep_waiting = True
        while keep_waiting:
            downloads = self.check_download_status()
            n_queued = downloads['queueSize']
            keep_waiting = n_queued > 0
            if keep_waiting:
                print("\n", n_queued,
                      "downloads queued but not yet available. "
                      "Waiting for 30 seconds.\n")
                time.sleep(30)

            if not timeout is None:
                timeout -= 30
                if timeout < 0:
                    break

        return downloads

    def download(self, wait=True, timeout=None, override=True):
        """
        Download the requested files and save them to disk.

        Parameters
        ----------
        wait : bool, optional
            Whether to wait for the downloads to become available 
            (default is True).
        timeout : int, optional
            The maximum time to wait for the downloads to become 
            available in seconds (default is None).
        override : bool, optional
            Whether to override existing downloaded files with the same 
            name (default is True).

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If no downloads are available or if the specified product 
            filter does not match the downloaded file.

        Notes
        -----
        This method downloads the files and saves them to disk. The 
        files will be saved to the path specified by the `path_tmpl` 
        attribute with the `display_id` of the download. If the 
        `override` parameter is set to False, files with the same name 
        will not be downloaded again.

        """
        # Check download status
        if wait:
            downloads = self.wait_for_available_downloads(timeout=timeout)
        else:
            downloads = self.check_download_status()

        available_or_proxied = (
            downloads['available']
            + [dld for dld in downloads['requested'] if dld['statusCode'] == 'P'])
        if not available_or_proxied:
            raise ValueError('No available downloads.')

        # Download available downloads
        for download in available_or_proxied:
            # Filter out products
            if not self.product_filter is None:
                match = [download[k] == v for k,
                         v in self.product_filter.items()]
                if not all(match):
                    continue

            # Download and save compressed file
            dld_path = self.path_tmpl.format(display_id=download['displayId'])
            # Cache downloads
            if override or not os.path.exists(dld_path):
                print('Saving download: {}'.format(download['displayId']))
                with open(dld_path, 'wb') as dld_file:
                    response = requests.get(download['url'])
                    dld_file.write(response.content)

            self.uncompress(dld_path)

    def uncompress(self, download_path):
        """
        Extracts all files from a compressed tar archive into the 
        directory specified by `self.label`.

        Parameters:
        -----------
        download_path: str
            The path to the compressed tar archive to be extracted.

        Returns:
        --------
        None

        """
        # Extract compressed files
        with tarfile.TarFile(download_path, 'r') as dld_tarfile:
            dld_tarfile.extractall(self.label)