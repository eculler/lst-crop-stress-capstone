# Remotely Sensed Crop Stress Early Indicator

Can satellite remote sensing detect early stage crop stress at high resolution across whole-farm scale?

Modern agribusiness often employs targeted technology to optimize cropland productivity using modern information and communication technologies at fine spatial resolution (within-field scale). High resolution remotely sensed data of soil conditions and vegetation health provides near real-time information that informs adaptive irrigation and fertilization technology. NDVI is a commonly used remotely sensed index that provides data on the "greenness" or health of crop vegetation.  However, the index is a lagging indicator of crop stress because water or heat stress occurs prior to the degradation of vegetation greenness.

Hydrosat provides a proprietary "fused" thermal infrared land surface temperature (LST) imagery product that is downscaled to 20 m resolution using a combination of MODIS, Sentinel and Landsat imaging platforms. LST provides a leading indication of crop stress relative to NDVI. Hydrosat utilizes a data mining approach for sharpening thermal satellite imagery (DMS) (Gao, F. 2012) and a separate algorithm for interpolating land surface temperature between measurement points (STARFM) (Gao, F 2006). This high resolution fused product is produced daily and presents an added value opportunity for agribusiness

This project aims to support this effort by exploring the relationship between land surface temperature and canopy temperature, an index known as Canopy Air Temperature Index (CATD), to evaluate the availability of moisture to the crops. When crop moisture is limited, leaf stomata close which prevents cooling of the leaf surface and leads to a larger values of CATD.

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
conda env create -f lst-comparison-tcruicks-environment.yml
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

> Gao, F. Masek, J. Schwaller, M. Hall, F. 2006. On the Blending of Landsat and MODIS Surface Reflectance: Predicting Landsat Surface Reflectance. IEE Transaction on Geoscience and Remote Sensing Vol 44, No 8.
>
> Gao, F. Kustas, W. Anderson, M. 2012. A Data Mining Approach for Sharpening Thermal Satellite Imagery Over Land. Remote Sensing. doi: 10.3390/rs4113287.
