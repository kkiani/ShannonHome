from enum import Enum

class SecurityEvent(Enum):
    MOTION_SENSE = 'motion.sense'
    LOGIN_FAIL_ATTEMPT = 'login.fail'
    BAD_TOKEN_ATTEMPT = 'token.fail'
    SECURITY_OFF = 'security.off'
    SECURITY_ON = 'security.on'