%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin, BitwiseBuiltin
from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.uint256 import Uint256
from starkware.cairo.common.math_cmp import is_nn
from starkware.cairo.common.cairo_keccak.keccak import (
    keccak_felts_bigend, keccak_uint256s_bigend, finalize_keccak)

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

@view
func hash_to_fp_XMDSHA256{
        syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, bitwise_ptr : BitwiseBuiltin*,
        range_check_ptr}(msg : Uint256) -> (res : Uint256):
    # inputs
    # # msg of bytes, 32 byte string
    # # domain, string such as "BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_NUL_"
    # # count, 4

    # expand message via SHA256XMD,
    alloc_locals
    let (local keccak_ptr_start) = alloc()
    let keccak_ptr = keccak_ptr_start

    let b_0 : Uint256* = alloc()

    # b_0 = H(Z_pad || msg || l_i_b_str || I2OSP(0, 1) || DST_prime)
    assert [b_0] = Uint256(0, 0)
    assert [b_0 + 1] = Uint256(0, 0)
    assert [b_0 + 2] = msg
    assert [b_0 + 3] = Uint256(0, 0)

    # append bytes to final string based on desired length, can be fixed for our purposes
    let (res) = keccak_felts_bigend{keccak_ptr=keccak_ptr}(n_elements=1, elements=b_0)

    # Call finalize once at the end to verify the soundness of the execution
    finalize_keccak(keccak_ptr_start=keccak_ptr_start, keccak_ptr_end=keccak_ptr)

    return (res)
end
