import zstandard as zstd


class ZstdCompressor:
    def __init__(self, level=9, zstd_dict=None):
        self.level = level
        if (zstd_dict is not None) and (not isinstance(zstd_dict, zstd.ZstdCompressionDict)):
            zstd_dict = zstd.ZstdCompressionDict(zstd_dict)

        self._compressor = zstd.ZstdCompressor(level=level, write_checksum=False, write_dict_id=False, dict_data=zstd_dict)
        self._decompressor = zstd.ZstdDecompressor(dict_data=zstd_dict)

    def compress(self, data: bytes):
        return self._compressor.compress(data)

    def decompress(self, data: bytes):
        return self._decompressor.decompress(data)

    @classmethod
    def optimize_dict(self, samples: list[bytes]):
        total_size = sum(map(len, samples))
        dict_size = max(total_size // 100, 256)
        dict_size = min(dict_size, int(109e3))
        zstd_dict = zstd.train_dictionary(dict_size, samples)
        return zstd_dict.as_bytes()
