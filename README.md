# Remotely Sensed Crop Stress Early Indicator

Can satellite remote sensing detect early stage crop stress at high resolution across whole-farm scale?

Modern agribusiness employs adaptive and targeted technology that can optimize crop productivty down to the square meter of field area. High resolution remotely sense data of soil conditions and vegetation health provides near real-time information that informs adaptive irrigation and fertilization technology. NDVI is a commonly used remotely sensed index that provides data on the "greenness" or health of crop vegetation.  The index is a lagging indicator of crop stress because water or heat stress occurs prior to the degradation of vegetation greenness.

This project seeks to provide a high resolution (20m) product that provides a leading indication of crop stress relative to NDVI.  We aim to used land surface temperature (canopy temperature) to evaluate the availability of moisture to the crops.  The Canopy Air Temperature Index (CATD) is one index that can be computed using thermal infrared imagery of canopy temperature and ambient air temperature.  When crop moisture is limited, leaf stomata close which prevents cooling of the leaf surface and leads to a larger values of CATD.  

We use a proprietary "fused" thermal infrared land surface temperature (LST) imagery product that is downscaled to 20 m resolution using a combination of MODIS, Sentinel and Landsat imaging platforms. This high resolution fused product is produced daily and presents an added value opportunity for agribusiness.

As of May 1, 2023, this notebook does the following:
1. Extracts and plots a time-series of the four fused LST image components and the fused LST.
2. Extracts and plots NDVI a time-series of a fused NDVI index.
3. Extracts, downloads, and plots air temperature data from the HRRR model.
4. Computes and plots a time-series of CATD for the four fused LST image components and the fused LST..

# Collaborators and Acknowledgements

- [Erik Anderson](https://github.com/eriktuck)
- [Tyler Cruickshank](https://github.com/tcruicks)
- [Joe McGlinchy](https://github.com/joemcglinchy)
We thank Joe McGlinchy of Hydrosat for providing project guidance and data access.

[![DOI](https://zenodo.org/badge/627146632.svg)](https://zenodo.org/badge/latestdoi/627146632)

### Environment Requirements

An environment.yml file is provided for creating the environment needed to run this notebook.  After cloning the directory to your computer, create and activate the conda environment with the following commands in a terminal shell:

```bash
conda env create -f environment.yml
conda activate earth-analytics-python
```

The environment must be activated before running the notebook.

### Data Access

For satellite image access you must receive Hydrosat Fusion hub account credentials prior to running this project.  No data is stored locally.  Add your Hydrosat Fusion Hub account credentials to the `secrets/` folder in a file called `creds.json` with the format:

```json
{
    "username":"",
    "password":""
}
```
See the [Hydrosat Fusion Hub Documentation](https://hydrosat.github.io/fusion-hub-docs/intro.html) for additional guidance.

There are two to three sources of meteorological data available.  1) A comma delimited .csv file.  2) Use HRRR model data.  3) Use Synoptic Data API.  This notebook is currently (April 2023) download and using HRRR data.  The functionality is built in to the notebook.  All meteorological data is contained in the /data directory.
