import random
import string


class OTP:
    '''One Time Password'''

    def __init__(self):
        self._otp = None

    def __repr__(self):
        return f'<OTP object with code: {self._otp}>'

    def __str__(self):
        return f'<OTP object with code: {self._otp}>'

    def generate_digit(self, digit: int = 4):
        '''Generate number type OTP '''
        numbers = string.digits
        self._otp = ''.join(random.sample(numbers, digit))

    def generate_character(self, digit: int = 4):
        '''Generate character type OTP '''
        char = string.ascii_letters
        self._otp = ''.join(random.sample(char, digit))

    def generate_mix(self, digit: int = 4):
        '''Generate mix type OTP '''
        mix = string.ascii_letters + string.digits
        self._otp = ''.join(random.sample(mix, digit))

    def verify(self, data: str) -> bool:
        '''Verify user data with OTP '''
        __otp = ''.join(self._otp)

        if __otp == data:
            return True
        else:
            return False

    def get_otp(self) -> str:
        '''Get OTP '''
        return self._otp

    def set_otp(self, otp: str):
        '''Set cutom logical OTP '''
        self._otp = otp
