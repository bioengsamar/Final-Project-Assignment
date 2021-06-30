from ctypes import c_void_p,c_int,c_char_p,c_ulong,POINTER,byref,cdll,c_ubyte,cast,Structure
from ctypes.util import find_library
import platform
import numpy as np
import os

TJPF_BGR = 1

class CroppingRegion(Structure):
    _fields_ = [("x", c_int), ("y", c_int), ("w", c_int), ("h", c_int)]
    
class TransformStruct(Structure):
    _fields_ = [("r", CroppingRegion), ("op", c_int), ("options", c_int), ("data", c_void_p),
        ("customFilter", c_void_p)]

class TurboJPEG(object):
    """A Python wrapper of libjpeg-turbo for decoding and encoding JPEG image."""
    def __init__(self):
        turbo_jpeg = cdll.LoadLibrary(
            self.__find_turbojpeg() )
        self.__init_decompress = turbo_jpeg.tjInitDecompress
        self.__init_decompress.restype = c_void_p
        self.__buffer_size = turbo_jpeg.tjBufSize
        self.__buffer_size.argtypes = [c_int, c_int, c_int]
        self.__buffer_size.restype = c_ulong
        self.__init_compress = turbo_jpeg.tjInitCompress
        self.__init_compress.restype = c_void_p
        self.__buffer_size_YUV2 = turbo_jpeg.tjBufSizeYUV2
        self.__buffer_size_YUV2.argtypes = [c_int, c_int, c_int, c_int]
        self.__buffer_size_YUV2.restype = c_ulong
        self.__destroy = turbo_jpeg.tjDestroy
        self.__destroy.argtypes = [c_void_p]
        self.__destroy.restype = c_int
        self.__decompress_header = turbo_jpeg.tjDecompressHeader3
        self.__decompress_header.argtypes = [
            c_void_p, POINTER(c_ubyte), c_ulong, POINTER(c_int),
            POINTER(c_int), POINTER(c_int), POINTER(c_int)]
        self.__decompress_header.restype = c_int
        self.__decompress = turbo_jpeg.tjDecompress2
        self.__decompress.argtypes = [
            c_void_p, POINTER(c_ubyte), c_ulong, POINTER(c_ubyte),
            c_int, c_int, c_int, c_int, c_int]
        self.__decompress.restype = c_int
        self.__decompressToYUV2 = turbo_jpeg.tjDecompressToYUV2
        self.__decompressToYUV2.argtypes = [
            c_void_p, POINTER(c_ubyte), c_ulong, POINTER(c_ubyte),
            c_int, c_int, c_int, c_int]
        self.__decompressToYUV2.restype = c_int
        self.__compress = turbo_jpeg.tjCompress2
        self.__compress.argtypes = [
            c_void_p, POINTER(c_ubyte), c_int, c_int, c_int, c_int,
            POINTER(c_void_p), POINTER(c_ulong), c_int, c_int, c_int]
        self.__compress.restype = c_int
        self.__compressFromYUV = turbo_jpeg.tjCompressFromYUV
        self.__compressFromYUV.argtypes = [
            c_void_p, POINTER(c_ubyte), c_int, c_int, c_int, c_int,
            POINTER(c_void_p), POINTER(c_ulong), c_int, c_int]
        self.__compressFromYUV.restype = c_int
        self.__init_transform = turbo_jpeg.tjInitTransform
        self.__init_transform.restype = c_void_p
        self.__transform = turbo_jpeg.tjTransform
        self.__transform.argtypes = [
            c_void_p, POINTER(c_ubyte), c_ulong, c_int, POINTER(c_void_p),
            POINTER(c_ulong), POINTER(TransformStruct), c_int]
        self.__transform.restype = c_int
        self.__free = turbo_jpeg.tjFree
        self.__free.argtypes = [c_void_p]
        self.__free.restype = None
        self.__get_error_str = turbo_jpeg.tjGetErrorStr
        self.__get_error_str.restype = c_char_p
        # tjGetErrorStr2 is only available in newer libjpeg-turbo
        self.__get_error_str2 = getattr(turbo_jpeg, 'tjGetErrorStr2', None)
        if self.__get_error_str2 is not None:
            self.__get_error_str2.argtypes = [c_void_p]
            self.__get_error_str2.restype = c_char_p
        # tjGetErrorCode is only available in newer libjpeg-turbo
        self.__get_error_code = getattr(turbo_jpeg, 'tjGetErrorCode', None)
        if self.__get_error_code is not None:
            self.__get_error_code.argtypes = [c_void_p]
            self.__get_error_code.restype = c_int
        self.__scaling_factors = []
        class ScalingFactor(Structure):
            _fields_ = ('num', c_int), ('denom', c_int)
        get_scaling_factors = turbo_jpeg.tjGetScalingFactors
        get_scaling_factors.argtypes = [POINTER(c_int)]
        get_scaling_factors.restype = POINTER(ScalingFactor)
        num_scaling_factors = c_int()
        scaling_factors = get_scaling_factors(byref(num_scaling_factors))
        for i in range(num_scaling_factors.value):
            self.__scaling_factors.append(
                (scaling_factors[i].num, scaling_factors[i].denom))

    

    def decode(self, jpeg_buf, block, pixel_format=TJPF_BGR, scaling_factor=None, flags=0):
        """decodes JPEG memory buffer to numpy array."""
        handle = self.__init_decompress()
        try:
            pixel_size = [3, 3, 4, 4, 4, 4, 1, 4, 4, 4, 4, 4]
            jpeg_array_original = np.frombuffer(jpeg_buf, dtype=np.uint8)
            jpeg_array = jpeg_array_original[:int(jpeg_array_original.shape[0])//block]
            src_addr = self.__getaddr(jpeg_array)
            scaled_width, scaled_height, _, _ = \
                self.__get_header_and_dimensions(handle, jpeg_array.size, src_addr, scaling_factor)
            img_array = np.empty(
                [scaled_height, scaled_width, pixel_size[pixel_format]],
                dtype=np.uint8)
            dest_addr = self.__getaddr(img_array)
            status = self.__decompress(
                handle, src_addr, jpeg_array.size, dest_addr, scaled_width,
                0, scaled_height, pixel_format, flags)
            return img_array
        finally:
            self.__destroy(handle)

    
    def __get_header_and_dimensions(self, handle, jpeg_array_size, src_addr, scaling_factor):
        """returns scaled image dimensions and header data"""
        if scaling_factor is not None and \
            scaling_factor not in self.__scaling_factors:
            raise ValueError('supported scaling factors are ' +
                str(self.__scaling_factors))
        width = c_int()
        height = c_int()
        jpeg_colorspace = c_int()
        jpeg_subsample = c_int()
        status = self.__decompress_header(
            handle, src_addr, jpeg_array_size, byref(width), byref(height),
            byref(jpeg_subsample), byref(jpeg_colorspace))
        scaled_width = width.value
        scaled_height = height.value
        if scaling_factor is not None:
            def get_scaled_value(dim, num, denom):
                return (dim * num + denom - 1) // denom
            scaled_width = get_scaled_value(
                scaled_width, scaling_factor[0], scaling_factor[1])
            scaled_height = get_scaled_value(
                scaled_height, scaling_factor[0], scaling_factor[1])
        return scaled_width, scaled_height, jpeg_subsample, jpeg_colorspace


    def __find_turbojpeg(self):
        """returns default turbojpeg library path if possible"""
        lib_path = find_library('turbojpeg')
        if lib_path is not None:
            return lib_path
        if platform.system() == 'Linux' and 'LD_LIBRARY_PATH' in os.environ:
            ld_library_path = os.environ['LD_LIBRARY_PATH']
            for path in ld_library_path.split(':'):
                lib_path = os.path.join(path, 'libturbojpeg.so.0')
                if os.path.exists(lib_path):
                    return lib_path
        raise RuntimeError(
            'Unable to locate turbojpeg library automatically. '
            'You may specify the turbojpeg library path manually.\n'
            'e.g. jpeg = TurboJPEG(lib_path)')

    def __getaddr(self, nda):
        """returns the memory address for a given ndarray"""
        return cast(nda.__array_interface__['data'][0], POINTER(c_ubyte))


