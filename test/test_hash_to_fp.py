import pytest
from web3 import Web3
from utils import bytes_32_to_uint_256_little, bytes_as_int_arr

@pytest.mark.asyncio
async def test_hash_uint256(hash_to_fp_factory):
    contract = hash_to_fp_factory

    z_pad =  bytes.fromhex("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    msg = bytes.fromhex("27c77ad9814f4e33e9d640482ccb7996eb095b0027384948140597fb9901ad63")
    l_i_b_str =  bytes.fromhex("0100")
    I20SP = bytes.fromhex("00")
    domain = bytes.fromhex("424c535f5349475f424c53313233383147325f584d443a5348412d3235365f535357555f524f5f4e554c5f")
    domainLen = bytes.fromhex("2b")


    full_bytes = z_pad + msg + l_i_b_str + I20SP + domain + domainLen
    print(len(full_bytes))
    web3_computed_hash = Web3.keccak(full_bytes).hex()
    
    print(bytes_as_int_arr(full_bytes))
    msg_uint256 = bytes_32_to_uint_256_little(msg)

    test_keccak_call = await contract.hash_to_fp(
       msg_uint256
    ).call()

    hash = test_keccak_call.result.res
    
    output = '0x' + hash.high.to_bytes(16, 'big').hex() + hash.low.to_bytes(16, 'big').hex()

    assert output == web3_computed_hash