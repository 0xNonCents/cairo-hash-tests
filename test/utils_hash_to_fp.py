from utils import bytes_as_int_arr

# These utils are for getting the inputs that we know beforehand for our hash to fp functions
def get_d0_parts():
    
    z_pad =  bytes.fromhex("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    msg = bytes.fromhex("27c77ad9814f4e33e9d640482ccb7996eb095b0027384948140597fb9901ad63")
    l_i_b_str =  bytes.fromhex("0100")
    I20SP = bytes.fromhex("00")
    domain = bytes.fromhex("424c535f5349475f424c53313233383147325f584d443a5348412d3235365f535357555f524f5f4e554c5f")
    domainLen = bytes.fromhex("2b")


    print( "z_pad  " + str(bytes_as_int_arr(z_pad)))
    print("l_i_b_str...domainLen  " + str(bytes_as_int_arr( l_i_b_str + I20SP + domain + domainLen)))

    print ("length bytes = " + str(len(z_pad + msg +l_i_b_str + I20SP + domain + domainLen)))
    
get_d0_parts()