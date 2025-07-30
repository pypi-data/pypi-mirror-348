import random
import string

class ExtIdentity():

    @staticmethod
    def get_random_string(length:int):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
    
    @staticmethod
    def check_valid_jwt(authorization):
        if hasattr(authorization, 'type') and hasattr(authorization, 'token'):
            match authorization.type:
                case 'bearer':
                    return True
                case _:
                    return False