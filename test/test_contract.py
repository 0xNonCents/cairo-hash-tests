"""contract.cairo test file."""
import pytest
from web3 import Web3
from utils import toUint256, splitToTwoUint256, fromUint256,  concat_arr, bytes_to_int_big,int_to_uint_256

@pytest.mark.asyncio
async def test_hash_uint256(hash_factory):
    contract = hash_factory

    keccak_input = [
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    ]
    
    web3_computed_hash = Web3.keccak(concat_arr(keccak_input)).hex()
    
    input = list(map(bytes_to_int_big, keccak_input))
    print(input)
    input_as_uint256 = list(map(int_to_uint_256,input)) 
    test_keccak_call = await contract.keccak_uint256(
       input_as_uint256
    ).call()

    hash = test_keccak_call.result.res
    
    output = '0x' + hash.high.to_bytes(16, 'big').hex() + hash.low.to_bytes(16, 'big').hex()

    assert output == web3_computed_hash

@pytest.mark.asyncio
async def test_hash_felt(hash_factory):
    contract = hash_factory

    num = 0

    keccak_input = [
        b'\xf9\x02\x18\xa0\x03\xb0\x16\xcc',
        b'\x93\x87\xcb\x3c\xef\x86\xd9\xd4',
        b'\xaf\xb5\x2c\x37\x89\x52\x8c\x53',
        b'\x0c\x00\x20\x87\x95\xac\x93\x7c',
        b'\x00\x00\x00\x00\x00\x00\x00\x77',
    ]
    
    web3_computed_hash = Web3.keccak(concat_arr(keccak_input)).hex()
    
    input = list(map(bytes_to_int_big, keccak_input))
    test_keccak_call = await contract.keccak_felt(
       input
    ).call()

    hash = test_keccak_call.result.res
    
    output = '0x' + hash.low.to_bytes(16, 'big').hex() + hash.high.to_bytes(16, 'big').hex()

    assert output == web3_computed_hash

@pytest.mark.asyncio
async def test_hash(hash_factory):
    contract = hash_factory
    # Test the function
    sig = int('0x8434e45af135f363b04b792c1d77b83e36ef66829b0a09f7eed058103429f0e7f759ebf6d001cf73e9138f5b7a7f04b602c4167390c323432562d6367e09169422707a9778eba260c4d6434ea5e1d2c81462a4e3cd430990aebc593f4ae7517c')
    round = 1657527

    one, two, three = splitToTwoUint256(sig)
    round_256 = toUint256(round)

    execution_info = await contract.hash([one, two, three]).invoke()
    result_1 = execution_info.result[0]

    print(result_1)
    assert fromUint256(result_1) == 1

    # assert Uint256(low=41007414709178760838645821390777687163, high=66617985427134803333752300516846126658) == 1
    #assert Uint256(low=248013529167620302498023360658101621533, high=86566658547474989050353495005084945854) == 1

