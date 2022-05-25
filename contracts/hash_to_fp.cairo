%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin, BitwiseBuiltin
from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.uint256 import Uint256, split_64
from starkware.cairo.common.cairo_keccak.keccak import keccak_bigend, finalize_keccak
from lib.utils import Uint256_to_32bit

func Uint256_to_64bit{range_check_ptr}(input : Uint256) -> (
        one : felt, two : felt, three : felt, four : felt):
    alloc_locals

    let (lowest : felt, second_lowest : felt) = split_64(input.high)
    let (second_highest : felt, highest : felt) = split_64(input.low)

    return (one=second_highest, two=highest, three=lowest, four=second_lowest)
end

# follows hash_to_fp_XMDSHA256 except we use keccak pending a SHA256 builtin
# expects msg to be big endian
@view
func hash_to_fp{
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

    let (first, second, third, fourth) = Uint256_to_64bit(msg)
    let b_0 : felt* = alloc()

    # b_0 = H(Z_pad || msg || l_i_b_str || I2OSP(0, 1) || DST_prime)
    assert [b_0] = 0
    assert [b_0 + 1] = 0
    assert [b_0 + 2] = 0
    assert [b_0 + 3] = 0
    assert [b_0 + 4] = 0
    assert [b_0 + 5] = 0
    assert [b_0 + 6] = 0
    assert [b_0 + 7] = 0
    assert [b_0 + 8] = first
    assert [b_0 + 9] = second
    assert [b_0 + 10] = third
    assert [b_0 + 11] = fourth
    assert [b_0 + 12] = 6007612014925447169
    assert [b_0 + 13] = 3616763562751379273
    assert [b_0 + 14] = 5573309208418400307
    assert [b_0 + 15] = 3833175991255251524
    assert [b_0 + 16] = 5935556667446091574
    assert [b_0 + 17] = 12208205451910991

    # append bytes to final string based on desired length, can be fixed for our purposes
    let (res) = keccak_bigend{keccak_ptr=keccak_ptr}(inputs=b_0, n_bytes=143)

    # Call finalize once at the end to verify the soundness of the execution
    finalize_keccak(keccak_ptr_start=keccak_ptr_start, keccak_ptr_end=keccak_ptr)

    return (res)
end
