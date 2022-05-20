"""contract.cairo test file."""
import pytest
from utils import toUint256, splitToTwoUint256, fromUint256


@pytest.mark.asyncio
async def test_small_string(hash_factory):
    contract = hash_factory

    num = 0
    num_256 = toUint256(num)

    print(num_256)
    execution_info = await contract.hash_to_fp_XMDSHA256([num]).invoke()
    
    print(hex(execution_info.result[0].low))
    print(hex(execution_info.result[0].high))
    res = hex(fromUint256(execution_info.result[0]))
    assert res == '0xbc36789e7a1e281436464229828f817d6612f7b477d66591ff96a9e064bcc98a'

@pytest.mark.asyncio
async def test_hash(hash_factory):
    contract = hash_factory
    # Test the function
    sig = int('0x8434e45af135f363b04b792c1d77b83e36ef66829b0a09f7eed058103429f0e7f759ebf6d001cf73e9138f5b7a7f04b602c4167390c323432562d6367e09169422707a9778eba260c4d6434ea5e1d2c81462a4e3cd430990aebc593f4ae7517c')
    round = 1657527

    one, two, three = splitToTwoUint256(sig)
    round_256 = toUint256(round)

    execution_info = await contract.hash_to_fp_XMDSHA256([one, two, three]).invoke()
    result_1 = execution_info.result[0]

    print(result_1)
    assert fromUint256(result_1) == 1

    # assert Uint256(low=41007414709178760838645821390777687163, high=66617985427134803333752300516846126658) == 1
    #assert Uint256(low=248013529167620302498023360658101621533, high=86566658547474989050353495005084945854) == 1

