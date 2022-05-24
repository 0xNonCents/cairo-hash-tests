# Cairo Hash tests

This is a collection of contracts, tests and utilites that are being developed as I learn about the builtin hash libraries in cairo. The current hash alorithm being used is keccak however sha256 will be added when that is made available.

`tests/test_contract.py` demonstrates how to hash various input types (felt, uint256, 64 bit integers) using the different available functions. From exploring these different functions I have concluded that keccak/keccak_bigend are the most flexible for inputs the hash algorithm that are of odd length. Also it is important to mind the endianess of your input! For example keccak_bigend returns a big endian variable the input is still expected as little endian!

Lastly please take advantage of `test/utils.py`for usefull methods to handle the input.
