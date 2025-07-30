# PIXLISE Client Library for Python

This python package contains what's needed to communicate directly with the PIXLISE back-end and download, manipulate and upload data.

## Configuration and Authentication

It's a pip package, so can be installed by doing `pip install pixlise_client`. To update it `pip install --upgrade pixlise_client`. **Note that when upgrading it seems running the command twice ensures it does actually update, pip seems to not check for updates the first time**

Once installed, setting up a client is quite easy. **Note that you should get an error about a missing config file!**

```
from pixlise_client import pixlise

pixlib = pixlise.Pixlise()
authErr = pixlib.authenticate()
if len(authErr) > 0:
    print(authErr)
    exit(1)
```

Now you can create a config file in the path that the error message indicated (or if you prefer, use an environment variable, again as per the error message). Either way, the contents of the configuration needs to be JSON of the form:
```
{
        "host": "pixlise-host-address",
        "user": "your-user-name",
        "password": "your-password"
}
```

Where `pixlise-host-address` is the same URL you use in the browser for PIXLISE.

**Until we're confident all is working please use https://dev.pixlise.org!**

## Functions

Here you can read about all the functions the library exposes. You will need to call them all through the pixlib object created during the authentication step.

### About Error Handling

Note that all of these functions return an actual structure containing the data requested, but if an error occurs, they will return None and the error message will be printed to stdout. Please let us know if you prefer a different way to handle errors.


### Basic Scan Data

#### Listing Scans
```
scans = listScans(scanId: str)
```
Retrieves scan summary information (similar to PIXLISE dataset tiles). Note that if you specify a scan id (aka an RTT) it will just return the data for the scan specified, but an empty id retrieves all scans

#### Getting scan labels
```
labels = getScanMetaList(scanId: str)
```
You probably won't need this, the client will call this for some things internally

#### Getting a summary of scan entries
```
entries = getScanEntries(scanId: str)
```
This returns a list of structures, where each member contains a summary of what's available for that entry (aka PMC). This way you can check if a given PMC has Normal spectra, or Beam location information, before querying all the data for the scan.

#### Getting scan beam locations (x, y, z)
```
xyzs = getScanBeamLocations(scanId: str)
```
Returns the beam locations. These are not relative to an image, for that you need to call `getScanImageBeamLocations`. These are just the x,y,z coordinates.


### Housekeeping data
#### Getting raw housekeeping data, aka scan meta-data
```
meta = getScanMetaData(scanId: str)
```
This is the raw version that gets the structure itself. It has indexes that reference the scan labels list. To more easily use housekeeping data, see `getScanEntryDataColumns`.

#### Housekeeping data in map form
You can retrieve the list of housekeeping columns using:
```
cols = getScanEntryDataColumns(scanId: str)
```

To read an individual column as a map, use:
```
housekeeping = getScanEntryDataColumn(scanId: str, "f_head_yellow_piece")
```
This will return it with an array of PMCs, and an array of corresponding values read from the column specified.


### Accessing spectrum data
```
spectrum = getScanSpectrum(scanId: str, pmc: int, spectrumType: int, detector: str)
```
Note: spectrumType may be:
- 1 = Max Value
- 2 = Bulk Sum
- 3 = Normal
- 4 = Dwell

If you specify Max or Bulk, the pmc becomes irrelevant, you can set it to 0 or something else.

This will return a structure containing the spectrum. The counts field contains the list of counts (1 per channel).


### Quantification

#### Listing quantifications
```
quants = listScanQuants(scanId: str)
```
Lists available quants for a scan id.

#### Raw quantification access
```
quant = getQuant(quantId: str, SummaryOnly: bool)
```
If SummaryOnly is True, it won't download the quant data itself, just the summary info about it, who created it, when, input parameters, etc.
Otherwise data is returned, and can be more easily queried using `getQuantColumns` and `getQuantColumn`.

#### Downloading quant data in map form
```
cols = getQuantColumns(quantId: str)
```
Prints out all the columns in the quant file

```
quantMap = getQuantColumn(quantId: str, column: str, detector: str)
```
Column must be one of the ones returned by `getQuantColumns`, and detector needs to be `A`, `B` or `Combined`
This will return it with an array of PMCs, and an array of corresponding values read from the column specified.

### Regions Of Interest

#### Listing ROIs
```
rois = listScanROIs(scanId: str)
```
Returns all the ROIs associated with a scan. Each item is a structure containing all the properties of the ROI, except the PMCs in the ROI (because the listing may get large). To get the PMCs you need to call `getROI`

#### Getting an ROI
```
roi = getROI(roiId: str, isMist: bool)
```
Returns the full structure of the specified ROI including its PMC list. isMist needs to be set to True if querying Mist ROIs.

#### Creating ROIs
You can edit an existing ROI or create a new one with `createROI`. To edit a new one, retrieve the structure with `getROI` and change what's required, and call `createROI` to overwrite it. Note that if you change the id of the ROI in the structure, it won't overwrite.

```
roiResp = createROI(roiId: ROIItem, isMist: bool)
```
Note that it returns the created ROI (so if it generated an ROI id, that will be in the returned item).

To create a completely new ROI from scratch, you can call:
```
roi = allocROI(pmcs: List[int])
```
This creates a blank ROI structure with the PMC list set to what is specified. Name, Description and other fields can then be set, and it can be pussed to `createROI`.

For example:
```
roi = allocROI([7, 8, 10, 11])
roi.name = "peters ROI"
roi.scanId = "500302337"
roi.description = "Lib created ROI"

createdROI = createROI(roi, False)
```


### Image Access

#### Listing images for scans
This lists images for one or more scans. The reason you can specify more than one scan is to help find images that are associated with all the scans specified.. For images that are associated with more than one scan
```
images = listScanImages(["scanid1", "scanid2"], mustIncludeAll: bool)
```
Set mustIncludeAll to True to only return images that have all the scans associated with them. False would return any images that are associated with any of the scans specified.

#### Image Beam Locations (i,j coordinates)

First you need to know what versions of beam location data are available for a given image. There are multiple versions because our Beam Geometry Tool has evolved over time to output more accurate results, but you may want a specific version. To do this, call:
```
vers = getScanImageBeamLocationVersions(imageName: str)
```
Note that an image name here is assumed to be the scan id, a "/" and the image file name, for example: `500302337/PCW_1377_0789190464_000RCM_N064227850030233700030LUJ01.png`

It won't work without the first component of the name.

`getScanImageBeamLocationVersions` returns all the version numbers available in a list.

To retrieve the beam locations themselves, call:
```
ijs = getScanImageBeamLocations(imageName: str, scanId: str, version: int)
```

The scan id here may seem redundant but it's not! A given image may be associated with multiple scans, so here you're saying retrieve the beam locations for Dourbes 1 from an image that contains Dourbes 1 and 2 scan points. 

Note that if the version is set to -1, the latest version will be returned.

#### Image Uploads
```
uploadImage(key: str, image)
```
Allows uploading an image. Use the `allocImage()` and `setImageBeamMatch()` functions to allocate the various kinds of image/beam matching images.

```
image = allocImage(imageName: str, imageFilePath: str, originScanId: str, associatedScanIds: List[str])
```
Use to allocate an image structure describing the main fields in an image. This will read the file specified and put the image bytes into the structure created. The return value can be passed into `uploadImage()` or `setImageBeamMatch()`.

```
setImageBeamMatch(image, matchImageName: str, xOffset: float, yOffset: float, xScale: float, yScale: float)
```
Sets the specified image up as a beam matched image, ready to be used with `uploadImage()`


### Energy Calibration

Spectra are returned in terms of counts per channel but sometimes we want to know what energy (in eV) the channel is associated with (see `getDiffractionPeaks` for example). To retrieve the bulk sum spectrum energy calibration call:
```
getScanBulkSumCalibration(scanId: str):
```
This will return one structure per detector containing the energy calibration (start eV aka Offset, eV per channel aka XPERCHAN).

To specify a calibration to use call:
```
setUserScanCalibration(scanId: str, detector: str, starteV: float, perChanneleV: float):
```
Note that this is not saved anywhere, it's only stored in memory. This way it's available for subsequent calls to functions in the client that need it - once the client is freed from memory these are gone.


### Diffraction data
```
diffraction = getDiffractionPeaks(scanId: str, calibrationSource: int)
```
Retrieves the diffraction peaks for the given scan id. Note that calibrationSource can be set to:
- 1 = Bulk Sum
- 2 = User
So calling with calibrationSource=1 will use the calibration retrieved by `getScanBulkSumCalibration`, while calibrationSource=2 will use the one specified by `setUserScanCalibration`


### Custom Maps
```
saveMapData(key: str, pmcs: List[int], values: List[float])
```
Saves a map for a given name. These can be used in PIXLISE on visualisations. PMCs can be from a given scan, or if the map is not related to a given scan, it can be an increasing list of numbers, eg 0-N. Different users who call this with the same key will overwrite each others data, so try use a unique key!

```
map = loadMapData(key: str)
```
Loads a saved map with a given name.
