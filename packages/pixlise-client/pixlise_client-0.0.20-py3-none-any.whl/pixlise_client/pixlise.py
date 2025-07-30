import os
import sys
import platform
import array as arr
from ctypes import *
from typing import List

from .pixlisemsgs import scan_pb2
from .pixlisemsgs import scan_msgs_pb2
from .pixlisemsgs import scan_entry_metadata_msgs_pb2
from .pixlisemsgs import quantification_retrieval_msgs_pb2
from .pixlisemsgs import image_msgs_pb2
from .pixlisemsgs import roi_msgs_pb2
from .pixlisemsgs import scan_beam_location_msgs_pb2
from .pixlisemsgs import scan_entry_msgs_pb2
from .pixlisemsgs import image_beam_location_msgs_pb2
from .pixlisemsgs import spectrum_msgs_pb2
from .pixlisemsgs import diffraction_data_pb2
from .pixlisemsgs import roi_pb2
from .pixlisemsgs import spectrum_pb2

from google.protobuf.json_format import MessageToJson


#####################################################
# Go string conversion
#####################################################

class go_string(Structure):
    _fields_ = [
        ("p", c_char_p),
        ("n", c_int)]

def makeGoString(str):
    return go_string(c_char_p(str.encode('utf-8')), len(str))

#####################################################
# Needed to be able to allocate memory from Go
#####################################################

# A function that receives an array type string and a size,
# and returns a pointer.
alloc_f = CFUNCTYPE(c_void_p, c_char_p, c_int64)

_arrays: List[arr.array] = []

@alloc_f
def my_alloc(typecode, size):
    #print("my_alloc", typecode, size)
    allocdArray = arr.array(typecode.decode(), (0 for _ in range(size)))
    #print(allocdArray)
    _arrays.append(allocdArray)
    return allocdArray.buffer_info()[0]


def _popArray():
    global _arrays
    arr = _arrays[0]
    _arrays = _arrays[1:]
    return arr

#####################################################
# Error struct to use Go returned errors
#####################################################
class Error(Structure):
    _fields_ = [('err', c_char_p)]

    # NOTE: This thing will leak memory... Look at cleanup code in: https://fluhus.github.io/snopher/

#####################################################
# Helpers to reduce code duplication
#####################################################

def readArrayResult(msgName, err, parseInto):
    if len(err) > 0:
        print(msgName, "error:", err)
        return None
    
    parseInto.ParseFromString(bytes(_popArray()))
    return parseInto

#####################################################
    

class Pixlise:
    def __init__(self) -> None:
        # Try to find the platform-specific shared lib
        libName = "pixlise-"

        system = platform.system()
        machine = platform.machine()

        if machine == "AMD64" or machine == "x86_64":
            machine = "amd64"
        elif machine == "arm64":
            machine += "arm64"
        else:
            sys.exit("Unknown machine: " + machine)

        if system == "Linux":
            libName += "linux-" + machine + ".so"
        elif system == "Windows":
            libName += "windows.dll"
        elif system == "Darwin":
            libName += "darwin-" + machine + ".so"

        dllpath = os.path.join(os.path.dirname(__file__), libName)

        print("PIXLISE library loading: " + dllpath)

        self._lib = CDLL(dllpath)
        self._lib.authenticate.argtypes = [alloc_f]
        self._lib.authenticate.restype = c_char_p
        self._lib.listScans.argtypes = [Structure]
        self._lib.listScans.restype = c_char_p
        self._lib.getScanMetaList.argtypes = [Structure]
        self._lib.getScanMetaList.restype = c_char_p
        self._lib.getScanMetaData.argtypes = [Structure]
        self._lib.getScanMetaData.restype = c_char_p
        self._lib.getScanEntryDataColumns.argtypes = [Structure]
        self._lib.getScanEntryDataColumns.restype = c_char_p
        self._lib.getScanEntryDataColumnAsMap.argtypes = [Structure, Structure]
        self._lib.getScanEntryDataColumnAsMap.restype = c_char_p
        self._lib.getScanSpectrum.argtypes = [Structure, c_int32, c_int32, Structure]
        self._lib.getScanSpectrum.restype = c_char_p
        self._lib.getScanSpectrumRangeAsMap.argtypes = [Structure, c_int32, c_int32, Structure]
        self._lib.getScanSpectrumRangeAsMap.restype = c_char_p
        self._lib.listScanQuants.argtypes = [Structure]
        self._lib.listScanQuants.restype = c_char_p
        self._lib.getQuant.argtypes = [Structure, c_bool]
        self._lib.getQuant.restype = c_char_p
        self._lib.getQuantColumns.argtypes = [Structure]
        self._lib.getQuantColumns.restype = c_char_p
        self._lib.getQuantColumnAsMap.argtypes = [Structure, Structure, Structure]
        self._lib.getQuantColumnAsMap.restype = c_char_p
        self._lib.listScanImages.argtypes = [Structure, c_bool]
        self._lib.listScanImages.restype = c_char_p
        self._lib.listScanROIs.argtypes = [Structure]
        self._lib.listScanROIs.restype = c_char_p
        self._lib.getROI.argtypes = [Structure, c_bool]
        self._lib.getROI.restype = c_char_p
        self._lib.getScanBeamLocations.argtypes = [Structure]
        self._lib.getScanBeamLocations.restype = c_char_p
        self._lib.getScanEntries.argtypes = [Structure]
        self._lib.getScanEntries.restype = c_char_p
        self._lib.getScanImageBeamLocationVersions.argtypes = [Structure]
        self._lib.getScanImageBeamLocationVersions.restype = c_char_p
        self._lib.getScanImageBeamLocations.argtypes = [Structure, Structure, c_int32]
        self._lib.getScanImageBeamLocations.restype = c_char_p
        self._lib.setUserScanCalibration.argtypes = [Structure, Structure, c_float, c_float]
        self._lib.setUserScanCalibration.restype = c_char_p
        self._lib.getScanBulkSumCalibration.argtypes = [Structure]
        self._lib.getScanBulkSumCalibration.restype = c_char_p
        self._lib.getDiffractionPeaks.argtypes = [Structure, c_int32]
        self._lib.getDiffractionPeaks.restype = c_char_p
        self._lib.getDiffractionAsMap.argtypes = [Structure, c_int32, c_int32, c_int32]
        self._lib.getDiffractionAsMap.restype = c_char_p
        self._lib.getRoughnessAsMap.argtypes = [Structure, c_int32]
        self._lib.getRoughnessAsMap.restype = c_char_p
        self._lib.createROI.argtypes = [Structure, c_bool]
        self._lib.createROI.restype = c_char_p
        self._lib.saveMapData.argtypes = [Structure, Structure]
        self._lib.saveMapData.restype = c_char_p
        self._lib.loadMapData.argtypes = [Structure]
        self._lib.loadMapData.restype = c_char_p

    def authenticate(self):
        return self._lib.authenticate(my_alloc)

    def listScans(self, scanId: str):
        return readArrayResult("listScans", self._lib.listScans(makeGoString(scanId)), scan_msgs_pb2.ScanListResp())

    def getScanMetaList(self, scanId: str):
        return readArrayResult("getScanMetaList", self._lib.getScanMetaList(makeGoString(scanId)), scan_msgs_pb2.ScanMetaLabelsAndTypesResp())

    def getScanMetaData(self, scanId: str):
        return readArrayResult("getScanMetaData", self._lib.getScanMetaData(makeGoString(scanId)), scan_entry_metadata_msgs_pb2.ScanEntryMetadataResp())

    def getScanEntryDataColumns(self, scanId: str):
        return readArrayResult("getScanEntryDataColumns", self._lib.getScanEntryDataColumns(makeGoString(scanId)), scan_pb2.ClientStringList())

    def getScanEntryDataColumnAsMap(self, scanId: str, columnName: str):
        return readArrayResult("getScanEntryDataColumnAsMap", self._lib.getScanEntryDataColumnAsMap(makeGoString(scanId), makeGoString(columnName)), scan_pb2.ClientMap())

    def getScanSpectrum(self, scanId: str, pmc: int, spectrumType: int, detector: str):
        return readArrayResult("getScanSpectrum", self._lib.getScanSpectrum(makeGoString(scanId), pmc, spectrumType, makeGoString(detector)), spectrum_msgs_pb2.SpectrumResp())

    def getScanSpectrumRangeAsMap(self, scanId: str, channelStart: int, channelEnd: int, detector: str):
        return readArrayResult("getScanSpectrumRangeAsMap", self._lib.getScanSpectrumRangeAsMap(makeGoString(scanId), channelStart, channelEnd, makeGoString(detector)), spectrum_msgs_pb2.SpectrumResp())

    def listScanQuants(self, scanId: str):
        return readArrayResult("listScanQuants", self._lib.listScanQuants(makeGoString(scanId)), quantification_retrieval_msgs_pb2.QuantListResp())

    def getQuant(self, quantId: str, summaryOnly: bool):
        return readArrayResult("getQuant", self._lib.getQuant(makeGoString(quantId), summaryOnly), quantification_retrieval_msgs_pb2.QuantGetResp())

    def listScanImages(self, scanIds: List[str], mustIncludeAll: bool):
        if not (scanIds and isinstance(scanIds, list) and all(isinstance(scanId, str) for scanId in scanIds)):
            raise TypeError('scanIds must be a list of one or more string ids')

        goScanIds = "|".join(scanIds)

        return readArrayResult("listScanImages", self._lib.listScanImages(makeGoString(goScanIds), mustIncludeAll), image_msgs_pb2.ImageListResp())

    def listScanROIs(self, scanId: str):
        return readArrayResult("listScanROIs", self._lib.listScanROIs(makeGoString(scanId)), roi_msgs_pb2.RegionOfInterestListResp())

    def getROI(self, id: str, isMist: bool):
        return readArrayResult("getROI", self._lib.getROI(makeGoString(id), isMist), roi_msgs_pb2.RegionOfInterestGetResp())

    def getScanBeamLocations(self, scanId: str):
        return readArrayResult("getScanBeamLocations", self._lib.getScanBeamLocations(makeGoString(scanId)), scan_beam_location_msgs_pb2.ClientBeamLocations())

    def getScanEntries(self, scanId: str):
        return readArrayResult("getScanEntries", self._lib.getScanEntries(makeGoString(scanId)), scan_entry_msgs_pb2.ScanEntryResp())

    def getScanImageBeamLocationVersions(self, imageName: str):
        return readArrayResult("getScanImageBeamLocationVersions", self._lib.getScanImageBeamLocationVersions(makeGoString(imageName)), image_beam_location_msgs_pb2.ImageBeamLocationVersionsResp())

    def getScanImageBeamLocations(self, imageName: str, scanId: str, version: int):
        return readArrayResult("getScanImageBeamLocations", self._lib.getScanImageBeamLocations(makeGoString(imageName), makeGoString(scanId), version), image_beam_location_msgs_pb2.ImageBeamLocationsResp())

    def setUserScanCalibration(self, scanId: str, detector: str, starteV: float, perChanneleV: float):
        return readArrayResult("setUserScanCalibration", self._lib.setUserScanCalibration(makeGoString(scanId), makeGoString(detector), starteV, perChanneleV), spectrum_pb2.ClientEnergyCalibration())

    def getScanBulkSumCalibration(self, scanId: str):
        return readArrayResult("getScanBulkSumCalibration", self._lib.getScanBulkSumCalibration(makeGoString(scanId)), spectrum_pb2.ClientEnergyCalibration())

    def getDiffractionPeaks(self, scanId: str, calibrationSource: int):
        return readArrayResult("getDiffractionPeaks", self._lib.getDiffractionPeaks(makeGoString(scanId), calibrationSource), diffraction_data_pb2.ClientDiffractionData())

    def getDiffractionAsMap(self, scanId: str, calibrationSource: int, channelStart: int, channelEnd: int):
        return readArrayResult("getDiffractionAsMap", self._lib.getDiffractionAsMap(makeGoString(scanId), calibrationSource, channelStart, channelEnd), diffraction_data_pb2.ClientDiffractionData())

    def getRoughnessAsMap(self, scanId: str, calibrationSource: int):
        return readArrayResult("getRoughnessAsMap", self._lib.getRoughnessAsMap(makeGoString(scanId), calibrationSource), diffraction_data_pb2.ClientDiffractionData())

    def getQuantColumns(self, quantId: str):
        return readArrayResult("getQuantColumns", self._lib.getQuantColumns(makeGoString(quantId)), scan_pb2.ClientStringList())

    def getQuantColumnAsMap(self, quantId: str, columnName: str, detector: str):
        return readArrayResult("getQuantColumnAsMap", self._lib.getQuantColumnAsMap(makeGoString(quantId), makeGoString(columnName), makeGoString(detector)), scan_pb2.ClientMap())
   
    def allocROI(self, pmcs: List[int]) -> roi_pb2.ROIItem:
        item = roi_pb2.ROIItem()
        for pmc in pmcs:
            item.scanEntryIndexesEncoded.append(pmc)
        return item

    def createROI(self, roi: roi_pb2.ROIItem, isMist: bool):
        # Encode item to protobuf byte array
        roiJSON = MessageToJson(roi)
        return readArrayResult("createROI", self._lib.createROI(makeGoString(roiJSON), isMist), roi_msgs_pb2.RegionOfInterestWriteResp())

    def saveMapData(self, mapData: scan_pb2.ClientMap):
        # Encode item to protobuf byte array
        mapDataJSON = MessageToJson(mapData)

        err = self._lib.createROI(makeGoString(mapDataJSON))
        if len(err) > 0:
            print("saveMapData", "error:", err)
        return None

    def loadMapData(self, key: str):
        return readArrayResult("loadMapData", self._lib.loadMapData(makeGoString(key)), scan_pb2.ClientMap())

    def uploadImage(self, key: str, image: image_msgs_pb2.ImageUploadHttpRequest):
        return readArrayResult("uploadImage", self._lib.uploadImage(makeGoString(key)), scan_pb2.ClientMap())
    
    def allocImage(self, imageName: str, imageFilePath: str, originScanId: str, associatedScanIds: List[str]) -> image_msgs_pb2.ImageUploadHttpRequest:
        # Read image first
        with open(imageFilePath, mode="rb") as imgFile:
            imgData = imgFile.read()

            img = image_msgs_pb2.ImageUploadHttpRequest()
            img.name = imageName
            img.imageData = imgData
            img.originScanId = originScanId
            img.associatedScanIds = associatedScanIds
            return img
        print("allocImage: Failed to read", imageFilePath)
        return None

    def setImageBeamMatch(self, image: image_msgs_pb2.ImageUploadHttpRequest, matchImageName: str, xOffset: float, yOffset: float, xScale: float, yScale: float):
        # Set the right fields to turn this into a beam matched image
        xform = image_msgs_pb2.ImageMatchTransform()
        xform.beamImageFileName = matchImageName
        xform.xOffset = xOffset
        xform.yOffset = yOffset
        xform.xScale = xScale
        xform.yScale = yScale

        image.beamImageRef = xform
