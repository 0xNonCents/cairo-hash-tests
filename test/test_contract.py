"""contract.cairo test file."""
import os

import pytest
from starkware.starknet.testing.starknet import Starknet
from starkware.starknet.compiler.compile import compile_starknet_files
from utils import toUint256, splitToTwoUint256, fromUint256

# The path to the contract source code.
CONTRACT_FILE = os.path.join("HashToXMD", "hash_to_field.cairo")


# The testing library uses python's asyncio. So the following
# decorator and the ``async`` keyword are needed.
@pytest.mark.asyncio
async def test_hash():
    # Create a new Starknet class that simulates the StarkNet
    # system.
    starknet = await Starknet.empty()

    # Deploy the contract.

    contract_def = compile_starknet_files(
        files=[CONTRACT_FILE], disable_hint_validation=True
    )
    
    contract = await starknet.deploy(
        contract_def=contract_def
    )
    
    # Test the function
    sig = int('0x8434e45af135f363b04b792c1d77b83e36ef66829b0a09f7eed058103429f0e7f759ebf6d001cf73e9138f5b7a7f04b602c4167390c323432562d6367e09169422707a9778eba260c4d6434ea5e1d2c81462a4e3cd430990aebc593f4ae7517c')
    round = 1657527

    one, two, three = splitToTwoUint256(sig)
    round_256 = toUint256(round)

    execution_info = await contract.hash_to_fp_XMDSHA256([one, two, three]).invoke()
    result_1 = execution_info.result[0]

    print(hex(fromUint256(result_1)))
    assert fromUint256(result_1) == 1

    # assert Uint256(low=41007414709178760838645821390777687163, high=66617985427134803333752300516846126658) == 1
    #assert Uint256(low=248013529167620302498023360658101621533, high=86566658547474989050353495005084945854) == 1

