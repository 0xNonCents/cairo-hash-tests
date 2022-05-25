"""contract.cairo test file."""
import pytest
from web3 import Web3
from utils import  concat_arr, bytes_to_int_big,int_to_uint_256, bytes_to_uint256, bytes_as_int_arr

async def compare_hashes(keccak_input, contract):
    web3_computed_hash = Web3.keccak(keccak_input).hex()
    
    input_as_64_bit = bytes_as_int_arr(keccak_input)

    test_keccak_call = await contract.keccak(
       input_as_64_bit, len(keccak_input)
    ).call()

    hash = test_keccak_call.result.res
    
    output = '0x' + hash.high.to_bytes(16, 'big').hex() + hash.low.to_bytes(16, 'big').hex()
    
    assert output == web3_computed_hash


@pytest.mark.asyncio
async def test_hash_64_bit(hash_factory):
    contract = hash_factory
    
    short_input = [
        b'\x84'
    ]

    await compare_hashes(concat_arr(short_input), contract)

    standard = [
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    ]

    await compare_hashes(concat_arr(standard), contract)

    large = [
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
        b'\x84'
    ]

    await compare_hashes(concat_arr(large), contract)

@pytest.mark.asyncio
async def test_hash_big_multiple_parts_odd_bytes(hash_factory):
    contract = hash_factory
    # Test the function

    ## Hex input
    z_pad =  bytes.fromhex("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    msg = bytes.fromhex("27c77ad9814f4e33e9d640482ccb7996eb095b0027384948140597fb9901ad63")
    l_i_b_str =  bytes.fromhex("0100")
    I20SP = bytes.fromhex("00")
    domain = bytes.fromhex("424c535f5349475f424c53313233383147325f584d443a5348412d3235365f535357555f524f5f4e554c5f")
    domainLen = bytes.fromhex("2b")
    
    full_bytes = z_pad + msg + l_i_b_str + I20SP + domain + domainLen
    
    web3_computed_hash = Web3.keccak(full_bytes).hex()

    input_as_64_bit = bytes_as_int_arr(full_bytes)
    
    test_keccak_call = await contract.keccak(
       input_as_64_bit, len(full_bytes)
    ).call()

    hash = test_keccak_call.result.res
    output = '0x' + hash.high.to_bytes(16, 'big').hex() + hash.low.to_bytes(16, 'big').hex()

    assert output == web3_computed_hash



@pytest.mark.asyncio
async def test_hash_uint256(hash_factory):
    contract = hash_factory

    keccak_input = [
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    ]
    
    web3_computed_hash = Web3.keccak(concat_arr(keccak_input)).hex()

    input_as_uint256 = bytes_to_uint256(keccak_input[0])
    test_keccak_call = await contract.keccak_uint256(
       input_as_uint256
    ).call()

    hash = test_keccak_call.result.res
    
    output = '0x' + hash.high.to_bytes(16, 'big').hex() + hash.low.to_bytes(16, 'big').hex()

    assert output == web3_computed_hash


@pytest.mark.asyncio
async def test_hash_uint256_big(hash_factory):
    contract = hash_factory
    # Test the function

    ## Hex input
    sig = bytes.fromhex('8434e45af135f363b04b792c1d77b83e36ef66829b0a09f7eed058103429f0e7f759ebf6d001cf73e9138f5b7a7f04b602c4167390c323432562d6367e09169422707a9778eba260c4d6434ea5e1d2c81462a4e3cd430990aebc593f4ae7517c')
    
    web3_computed_hash = Web3.keccak(sig).hex()

    keccak_input = [sig[:32], sig[32:64], sig[64:]]
    input = list(map(bytes_to_int_big, keccak_input))
    
    input_as_uint256 = list(map(int_to_uint_256,input)) 
    test_keccak_call = await contract.keccak_uint256(
       input_as_uint256
    ).call()

    hash = test_keccak_call.result.res
    output = '0x' + hash.high.to_bytes(16, 'big').hex() + hash.low.to_bytes(16, 'big').hex()
    assert output == web3_computed_hash

@pytest.mark.asyncio
async def test_hash_multi_part(hash_factory):
    contract = hash_factory

    num = 0

    keccak_input = [
        b'\xf9\x02\x18\xa0\x03\xb0\x16\xcc',
        b'\x93\x87\xcb\x3c\xef\x86\xd9\xd4',
        b'\xaf\xb5\x2c\x37\x89\x52\x8c\x53',
        b'\x0c\x00\x20\x87\x95\xac\x93\x7c'
    ]
    
    web3_computed_hash = Web3.keccak(concat_arr(keccak_input)).hex()
    
    input_as_uint256 = bytes_to_uint256(concat_arr(keccak_input))
    
    test_keccak_call = await contract.keccak_uint256(
       input_as_uint256
    ).call()

    hash = test_keccak_call.result.res
    output = '0x' + hash.high.to_bytes(16, 'big').hex() + hash.low.to_bytes(16, 'big').hex()
    assert output == web3_computed_hash


