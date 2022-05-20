from starkware.starknet.testing.starknet import Starknet
from starkware.starknet.compiler.compile import compile_starknet_files
import pytest
import os
import asyncio

@pytest.fixture(scope="module")
def event_loop():
    return asyncio.new_event_loop()


@pytest.fixture(scope="module")
async def starknet_factory():
    starknet = await Starknet.empty()
    return starknet


# The path to the contract source code.
CONTRACT_FILE = os.path.join("HashToXMD", "hash_to_field.cairo")

@pytest.fixture(scope="module")
async def hash_factory(starknet_factory):
    # Create a new Starknet class that simulates the StarkNet
    # system.
    starknet = starknet_factory

    # Deploy the contract.

    contract_def = compile_starknet_files(
        files=[CONTRACT_FILE], disable_hint_validation=True
    )
    
    contract = await starknet.deploy(
        contract_def=contract_def
    )

    return contract
    
