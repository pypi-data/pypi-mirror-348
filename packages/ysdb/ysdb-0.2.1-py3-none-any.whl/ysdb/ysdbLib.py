from ctypes import *
from platform import *
import time
import pkg_resources
import os
import distro

rdbLib = None
# 通过pkg_resources可以不依赖当前文件位置定位到所需dll文件
package_path = pkg_resources.resource_filename('ysdb', '')
if system().lower() == 'windows':
	rdbLib = cdll.LoadLibrary(os.path.join(package_path, 'win/ysdbLib.dll'))
elif system().lower() == 'linux' and distro.id().lower() == 'centos':
	# Note: keep dependency order
	lib_names = [
			"libGL.so.1",
			"libGLdispatch.so.0",
			"libGLX.so.0",
			"libIceUtil++11.so.36",
			"libIce++11.so.36",
			"libIceUtil.so.36",
			"libIce.so.36",
			"libicudata.so.56",
			"libicuuc.so.56",
			"libicui18n.so.56",
			"libQt5Core.so.5",
			"libQt5Network.so.5",
			#"libQt5Test.so.5",
			#"libQt5X11Extras.so.5",
			#"libQt5XcbQpa.so.5",
			"libX11.so.6",
			"libXau.so.6",
			"libxcb.so.1",
			"libXext.so.6",
			"libysLib.so",
			"libysdbLib.so",
			"libysdbLib.so.1",
			"libysLib.so.1",
	]
	for lib in lib_names:
			# print(f'loading lib {lib}')
			cdll.LoadLibrary(os.path.join(package_path, f"centos/{lib}"))
	rdbLib = cdll.LoadLibrary(os.path.join(package_path, 'centos/libysdbLib.so'))
elif system().lower() == 'linux' and distro.id().lower() == 'debian':
	# Note: keep dependency order
	lib_names = [
		"libIceUtil.so.35",
		"libIce.so.35",
		"libicudata.so.56",
		"libicuuc.so.56",
		"libicui18n.so.56",
		"libQt5Core.so.5",
		"libQt5Network.so.5",
		"libQt5Test.so.5",
		"libysLib.so",
		"libysdbLib.so",
		"libysdbLib.so.1",
		"libysLib.so.1",
	]
	for lib in lib_names:
		# print(f'loading lib {lib}')
		cdll.LoadLibrary(os.path.join(package_path, f"debian/{lib}"))
	rdbLib = cdll.LoadLibrary(os.path.join(package_path, 'debian/libysdbLib.so'))
elif system().lower() == 'darwin':
	raise Exception(f"YSDB not supported on platform {system()} (macos)")
else:
	raise Exception(f"YSDB not supported on platform {system()}")


class PointData(Structure):
	_fields_ = [
		("tm", c_int),
		("ms", c_int),
		("fVal", c_double),
		("nVal", c_int),
		("state", c_ubyte),
		("flag", c_ubyte)
	]


class PointInfo(Structure):
	_fields_ = [
		("group", c_ubyte),
		("id", c_int),
		("tag", c_char * 256),
		("desc", c_char * 256),
		("type", c_int),
		("parentId", c_int)
	]


class FloatRealData(Structure):
	_fields_ = [
		("id", c_int),
		("tm", c_int),
		("ms", c_int),
		("val", c_float),
		("flag", c_ubyte),
		("state", c_ubyte)
	]


class FloatData(Structure):
	_fields_ = [
		("tm", c_int),
		("ms", c_int),
		("val", c_float),
		("flag", c_ubyte),
		("state", c_ubyte)
	]


class FloatStatData(Structure):
	_fields_ = [
		("maxVal", c_float),
		("maxTm", c_int),
		("maxMs", c_int),
		("minVal", c_float),
		("minTm", c_int),
		("minMs", c_int),
		("aveVal", c_float),
		("sumVal", c_float)
	]


class DoubleRealData(Structure):
	_fields_ = [
		("id", c_int),
		("tm", c_int),
		("ms", c_int),
		("val", c_double),
		("flag", c_ubyte),
		("state", c_ubyte)
	]


class DoubleData(Structure):
	_fields_ = [
		("tm", c_int),
		("ms", c_int),
		("val", c_double),
		("flag", c_ubyte),
		("state", c_ubyte)
	]


class DoubleStatData(Structure):
	_fields_ = [
		("maxVal", c_double),
		("maxTm", c_int),
		("maxMs", c_int),
		("minVal", c_double),
		("minTm", c_int),
		("minMs", c_int),
		("aveVal", c_double),
		("sumVal", c_double)
	]


class BoolRealData(Structure):
	_fields_ = [
		("id", c_int),
		("tm", c_int),
		("ms", c_int),
		("val", c_ubyte),
		("flag", c_ubyte)
	]


class BoolData(Structure):
	_fields_ = [
		("tm", c_int),
		("ms", c_int),
		("val", c_ubyte),
		("flag", c_ubyte)
	]


class IntRealData(Structure):
	_fields_ = [
		("id", c_int),
		("tm", c_int),
		("ms", c_int),
		("val", c_int),
		("state", c_ubyte),
		("flag", c_ubyte)
	]


class IntData(Structure):
	_fields_ = [
		("tm", c_int),
		("ms", c_int),
		("val", c_int),
		("state", c_ubyte),
		("flag", c_ubyte)
	]


class IntStatData(Structure):
	_fields_ = [
		("maxVal", c_int),
		("maxTm", c_int),
		("maxMs", c_int),
		("minVal", c_int),
		("minTm", c_int),
		("minMs", c_int),
		("aveVal", c_int),
		("sumVal", c_int)
	]


class LongRealData(Structure):
	_fields_ = [
		("id", c_int),
		("tm", c_int),
		("ms", c_int),
		("val", c_longlong),
		("flag", c_ubyte)
	]


class LongData(Structure):
	_fields_ = [
		("tm", c_int),
		("ms", c_int),
		("val", c_longlong),
		("flag", c_ubyte)
	]


class BlobData(Structure):
	_fields_ = [
		("tm", c_int),
		("ms", c_int),
		("val", POINTER(POINTER(c_ubyte))),
		("state", c_ubyte),
		("flag", c_ubyte)
	]


class BlobRealData(Structure):
	_fields_ = [
		("id", c_int),
		("tm", c_int),
		("ms", c_int),
		("val", POINTER(POINTER(c_ubyte))),
		("state", c_ubyte),
		("flag", c_ubyte)
	]


class BlobDataInfo(Structure):
	_fields_ = [
		("id", c_int),
		("tm", c_int),
		("ms", c_int),
		("size", c_int),
		("state", c_ubyte),
		("flag", c_ubyte)
	]


class PointRealData(Structure):
	_fields_ = [
		("group", c_ubyte),
		("id", c_int),
		("tm", c_int),
		("ms", c_int),
		("fVal", c_double),
		("nVal", c_int),
		("state", c_ubyte),
		("flag", c_ubyte)
	]


class PointData(Structure):
	_fields_ = [
		("tm", c_int),
		("ms", c_int),
		("fVal", c_double),
		("nVal", c_int),
		("state", c_ubyte),
		("flag", c_ubyte)
	]


class OneSecQuery(Structure):
	_fields_ = [
		("group", c_ubyte),
		("id", c_int),
		("tag", c_char * 256),
		("tm", c_int),
		("ms", c_int),
		("mode", c_int),
		("interval", c_int)
	]


class HisQuery(Structure):
	_fields_ = [
		("group", c_ubyte),
		("id", c_int),
		("tag", c_char * 256),
		("startTm", c_int),
		("startMs", c_int),
		("endTm", c_int),
		("endMs", c_int),
		("mode", c_int),
		("interval", c_int)
	]


class EventInfo(Structure):
	_fields_ = [
		("id", c_int),
		("sTm", c_int),
		("sMs", c_int),
		("type", c_int),
		("grade", c_ubyte),
		("content", c_char * 512),

		("group", c_ubyte),
		("nVal", c_int),
		("fVal", c_double),
		("val1", c_int),
		("val2", c_int),
		("val3", c_int),
		("pars", c_char * 512),

		("state", c_ubyte),
		("eTm", c_int),
		("eMs", c_int),
		("cTm", c_int),
		("cMs", c_int),
		("user", c_int)
	]


class BlobWaveHead(Structure):
	_fields_ = [
		("type", c_ubyte),
		("saveMode", c_ubyte),
		("working", c_ubyte),
		("periodType", c_ubyte),
		("periodFreq", c_uint),
		("periodCnt", c_uint),
		("pointCnt", c_uint),
		("start", c_ulonglong),
		("end", c_ulonglong),

		("maxVal", c_double),
		("minVal", c_double),

		("dataCnt", c_uint),
		("keyCnt", c_uint),

		("back", c_ubyte * 512)
	]


rdbLib.rdbConnect.argtypes = [c_char_p, c_int]
rdbLib.rdbConnect.restype = c_int

rdbLib.readFloatRealDatasById.argtypes = c_int, POINTER(c_int), c_int, POINTER(POINTER(FloatRealData))
rdbLib.readFloatRealDatasById.restype = c_int

rdbLib.rdbLogin.restype = c_char_p


class RdbClient:
	mHandle = -1

	def connect(self, ip, port):
		ipStr = c_char_p(ip.encode('utf-8'))
		self.mHandle = rdbLib.rdbConnect(ipStr, c_int(port))
		return (self.mHandle > 0)

	def login(self, user, password):
		userStr = c_char_p(user.encode('utf-8'))
		passStr = c_char_p(password.encode('utf-8'))
		retStr = rdbLib.rdbLogin(self.mHandle, userStr, passStr)
		return retStr;

	def readFloatRealDatasById(self, idList):
		if self.mHandle <= 0:
			return None
		idCount = len(idList)
		idArr = (c_int * idCount)(*idList)
		retDatas = POINTER(FloatRealData)()

		dataCount = rdbLib.readFloatRealDatasById(self.mHandle, idArr, idCount, byref(retDatas))

		dataList = [retDatas[i] for i in range(dataCount)]
		return dataList

	def readBoolRealDatasById(self, idList):
		if self.mHandle <= 0:
			return None
		idCount = len(idList)
		idArr = (c_int * idCount)(*idList)
		retDatas = POINTER(BoolRealData)()

		dataCount = rdbLib.readBoolRealDatasById(self.mHandle, idArr, idCount, byref(retDatas))

		dataList = [retDatas[i] for i in range(dataCount)]
		return dataList

	def readIntRealDatasById(self, idList):
		if self.mHandle <= 0:
			return None
		idCount = len(idList)
		idArr = (c_int * idCount)(*idList)
		retDatas = POINTER(IntRealData)()

		dataCount = rdbLib.readIntRealDatasById(self.mHandle, idArr, idCount, byref(retDatas))

		dataList = [retDatas[i] for i in range(dataCount)]
		return dataList

	def readBoolHisData(self, group, id, tag, startTm, startMs, endTm, endMs, mode, interval):
		if self.mHandle <= 0:
			return None
		hisQuery = HisQuery(group, id, tag.encode(), startTm, startMs, endTm, endMs, mode, interval)

		retHisDatas = POINTER(BoolData)()
		hisDataCount = rdbLib.readBoolHisData(self.mHandle, byref(hisQuery), byref(retHisDatas))
		hisDataList = [retHisDatas[i] for i in range(hisDataCount)]
		return hisDataList

	def readIntHisData(self, group, id, tag, startTm, startMs, endTm, endMs, mode, interval):
		if self.mHandle <= 0:
			return None
		hisQuery = HisQuery(group, id, tag.encode(), startTm, startMs, endTm, endMs, mode, interval)

		retHisDatas = POINTER(IntData)()
		hisDataCount = rdbLib.readIntHisData(self.mHandle, byref(hisQuery), byref(retHisDatas))
		hisDataList = [retHisDatas[i] for i in range(hisDataCount)]
		return hisDataList

	def readFloatHisData(self, hisQuery):
		if self.mHandle <= 0:
			return None

		retHisDatas = POINTER(FloatData)()
		hisDataCount = rdbLib.readFloatHisData(self.mHandle, byref(hisQuery), byref(retHisDatas))
		hisDataList = [retHisDatas[i] for i in range(hisDataCount)]
		return hisDataList

	def readBoolHisDataByQueryParam(self, hisQuery):
		if self.mHandle <= 0:
			return None

		retHisDatas = POINTER(BoolData)()
		hisDataCount = rdbLib.readBoolHisData(self.mHandle, byref(hisQuery), byref(retHisDatas))
		hisDataList = [retHisDatas[i] for i in range(hisDataCount)]
		return hisDataList

	def readIntHisDataByQueryParam(self, hisQuery):
		if self.mHandle <= 0:
			return None

		retHisDatas = POINTER(IntData)()
		hisDataCount = rdbLib.readIntHisData(self.mHandle, byref(hisQuery), byref(retHisDatas))
		hisDataList = [retHisDatas[i] for i in range(hisDataCount)]
		return hisDataList

	def readBlobRealDatasById(self, idList):
		if self.mHandle <= 0:
			return None

		idCount = len(idList)
		idArr = (c_int * idCount)(*idList)
		retDatas = POINTER(BlobRealData)()

		dataCount = rdbLib.readBlobRealDatasById(self.mHandle, idArr, idCount, byref(retDatas))

		dataList = [retDatas[i] for i in range(dataCount)]
		return dataList

	def readBlobSecData(self, oneSecQuery):
		if self.mHandle <= 0:
			return None

		retHisDatas = POINTER(BlobRealData)()
		hisDataCount = rdbLib.readBlobSecData(self.mHandle, byref(oneSecQuery), byref(retHisDatas))
		hisDataList = [retHisDatas[i] for i in range(hisDataCount)]
		return hisDataList

	def readBlobHisInfo(self, hisQuery):
		if self.mHandle <= 0:
			return None

		retDatas = POINTER(BlobDataInfo)()

		dataCount = rdbLib.readBlobHisInfo(self.mHandle, hisQuery, byref(retDatas))
		dataList = [retDatas[i] for i in range(dataCount)]
		return dataList

	def readBlobHisData(self, blobDataInfo):
		if self.mHandle <= 0:
			return None

		retDatas = POINTER(BlobRealData)()
		dataCount = rdbLib.readBlobHisInfo(self.mHandle, byref(blobDataInfo), byref(retDatas))
		return retDatas

	def readWaveData(self, oneSecQuery):
		if self.mHandle <= 0:
			return None

		retDatas = POINTER(BlobWaveData)()
		dataCount = rdbLib.readBlobHisInfo(self.mHandle, byref(oneSecQuery), byref(retDatas))
		return retDatas

	def writeCtrlDataById(self, user, ctrlType, ctrlMode, token, realPointData):
		if self.mHandle <= 0:
			return None
		tokenStr = c_char_p(token.encode('utf-8'))
		return rdbLib.writeCtrlDataById(self.mHandle, user, ctrlType, ctrlMode, tokenStr, realPointData)

	def subscribeEevntInfo(self, callbackFunc):
		if self.mHandle <= 0:
			return None

		return rdbLib.subscribeEventInfo(self.mHandle, callbackFunc)

	def subscribePointRealData(self, callbackFunc):
		if self.mHandle <= 0:
			return None

		return rdbLib.subscribePointRealData(self.mHandle, callbackFunc)

	def subscribeBlobRealData(self, callbackFunc):
		if self.mHandle <= 0:
			return None

		return rdbLib.subscribeBlobRealData(self.mHandle, callbackFunc)

	def evtConnect(self, port):
		if self.mHandle <= 0:
			return None
		return rdbLib.evtConnect(self.mHandle, port)

	def getPointIdAll(self, group):
		if self.mHandle <= 0:
			return None

		retDatas = POINTER(c_int)()
		count = rdbLib.getPointIdAll(self.mHandle, group, byref(retDatas))
		allIdList = [retDatas[i] for i in range(count)]
		return allIdList

	def getPointInfos(self, group, idList):
		if self.mHandle <= 0:
			return None

		idCount = len(idList)
		idArr = (c_int * idCount)(*idList)
		retDatas = POINTER(PointInfo)()

		count = rdbLib.getPointInfos(self.mHandle, group, idArr, idCount, byref(retDatas))
		pointInfoList = [retDatas[i] for i in range(count)]
		return pointInfoList

	def readPointHisData(self, hisQuery):
		if self.mHandle <= 0:
			return None

		retHisDatas = POINTER(PointData)()
		hisDataCount = rdbLib.readPointHisData(self.mHandle, byref(hisQuery), byref(retHisDatas))
		hisDataList = [retHisDatas[i] for i in range(hisDataCount)]
		return hisDataList

	# 将hisQuery参数展开
	def readPointHisDataFlat(self, group, id, tag, startTm, startMs, endTm, endMs, mode, interval):
		if self.mHandle <= 0:
			return None
		hisQuery = HisQuery(group, id, tag.encode(), startTm, startMs, endTm, endMs, mode, interval)

		retHisDatas = POINTER(PointData)()
		hisDataCount = rdbLib.readPointHisData(self.mHandle, byref(hisQuery), byref(retHisDatas))
		hisDataList = [retHisDatas[i] for i in range(hisDataCount)]
		return hisDataList

	def readPointHisDatas(self, hisQueryList):
		if self.mHandle <= 0:
			return None

		hisResultList = [];
		for hisQuery in hisQueryList:
			hisRet = self.readPointHisData(hisQuery)
			hisResultList.append(hisRet)
		return hisResultList;

	def disconnect(self):
		rdbLib.rdbClose()

