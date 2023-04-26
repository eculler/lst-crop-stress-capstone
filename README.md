# Remotely Sensed Crop Stress Early Indicator

[![DOI](https://zenodo.org/badge/627146632.svg)](https://zenodo.org/badge/latestdoi/627146632)

Shared repo for the Earth Analytics 2023 Capstone.

**Remember to pull changes before beginning to code!**

### Environment

We recommend setting up a conda environment using the [geospatial](https://geospatial.gishub.org/) package (follow the instructions to [install with mamba](https://geospatial.gishub.org/installation/#using-mamba)). The `environment.yml` file is included primarily for documentation.

### Data Access

You must receive Hydrosat Fusion hub account credentials prior to running this project. 

Add your Hydrosat Fusion Hub account credentials to the `secrets/` folder in a file called `creds.json` with the format:

```json
{
    "username":"",
    "password":""
}
```

See the [Hydrosat Fusion Hub Documentation](https://hydrosat.github.io/fusion-hub-docs/intro.html) for additional guidance.

### Collaborators
- [Erik Anderson](https://github.com/eriktuck)
- [Stepan Bryleev](https://github.com/StepanBryleev)
- [Tyler Cruikshank](https://github.com/tcruicks)
