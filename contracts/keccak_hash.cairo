%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin, BitwiseBuiltin
from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.uint256 import Uint256
from starkware.cairo.common.math_cmp import is_nn
from starkware.cairo.common.cairo_keccak.keccak import (
    keccak_felts_bigend, keccak_uint256s_bigend, finalize_keccak, keccak_bigend)

@view
func keccak{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, bitwise_ptr : BitwiseBuiltin*,
        range_check_ptr}(input_len : felt, input : felt*, n_bytes : felt) -> (res : Uint256):
    # expand message via SHA256XMD,
    alloc_locals
    let (local keccak_ptr_start) = alloc()
    let keccak_ptr = keccak_ptr_start

    # append bytes to final string based on desired length, can be fixed for our purposes
    let (res) = keccak_bigend{keccak_ptr=keccak_ptr}(inputs=input, n_bytes=n_bytes)

    # Call finalize once at the end to verify the soundness of the execution
    finalize_keccak(keccak_ptr_start=keccak_ptr_start, keccak_ptr_end=keccak_ptr)

    return (res)
end

@view
func keccak_felt{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, bitwise_ptr : BitwiseBuiltin*,
        range_check_ptr}(input_len : felt, input : felt*) -> (res : Uint256):
    # expand message via SHA256XMD,
    alloc_locals
    let (local keccak_ptr_start) = alloc()
    let keccak_ptr = keccak_ptr_start

    # append bytes to final string based on desired length, can be fixed for our purposes
    let (res) = keccak_felts_bigend{keccak_ptr=keccak_ptr}(n_elements=input_len, elements=input)

    # Call finalize once at the end to verify the soundness of the execution
    finalize_keccak(keccak_ptr_start=keccak_ptr_start, keccak_ptr_end=keccak_ptr)

    return (res)
end

@view
func keccak_uint256{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, bitwise_ptr : BitwiseBuiltin*,
        range_check_ptr}(input_len : felt, input : Uint256*) -> (res : Uint256):
    # expand message via SHA256XMD,
    alloc_locals
    let (local keccak_ptr_start) = alloc()
    let keccak_ptr = keccak_ptr_start

    # append bytes to final string based on desired length, can be fixed for our purposes
    let (res) = keccak_uint256s_bigend{keccak_ptr=keccak_ptr}(n_elements=input_len, elements=input)

    # Call finalize once at the end to verify the soundness of the execution
    finalize_keccak(keccak_ptr_start=keccak_ptr_start, keccak_ptr_end=keccak_ptr)

    return (res)
end