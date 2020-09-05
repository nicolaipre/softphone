
class PhoneCallNotInProgress(Exception):
    """
    A SIP phone call has been referenced, but the phone call does not exist or has ended.
    """