# ##################################################################
#
# Copyright 2025 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Snigdha Biswas (snigdha.biswas@teradata.com)
# Secondary Owner: Aanchal Kavedia (aanchal.kavedia@teradata.com)
#
# Notes:
#   * This code is only for internal use.
#   * This file includes the teradatgenai error messages.
#
# ##################################################################
from teradatagenai.common.message_codes import MessageCodes

class Messages:
    """
    Class to store and retrieve error messages for the teradatagenai package.
    """
    _messages = {
        MessageCodes.METHOD_NOT_IMPLEMENTED: "[Teradata][teradatagenai]({code}) Method is not supported for the api_type '{api_type}'",
    }

    @staticmethod
    def get_message(code, *args, **kwargs):
        """
        Retrieves and formats the error message for the given code.

        PARAMETERS:
            code:
                The message code to retrieve the message for.
                Types: str

            *args, **kwargs:
                Additional arguments to format the message.

        RETURNS:
            str
        """
        if code not in Messages._messages:
            raise ValueError(f"Message code '{code}' not found.")
        return Messages._messages[code].format(code=code, *args, **kwargs)