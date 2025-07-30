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
#   * This file includes the teradatgenai exceptions.
#
# ##################################################################
from teradatagenai.common.messages import Messages
from teradatagenai.common.message_codes import MessageCodes

class TeradataGenAIException(Exception):
    """
    Base class for all custom exceptions in the teradatagenai package.
    """

    @staticmethod
    def validate_method(instance, method_name, api_type):
        """
        Validates if the specified method is implemented in the given instance.

        PARAMETERS:
            instance:
                The object instance to check for the method.
                Types: object

            method_name:
                The name of the method to validate.
                Types: str

            api_type:
                The API type for which the method is being validated.
                Types: str

        RAISES:
            NotImplementedError
            
        EXAMPLES:
            TeradataGenAIException.validate_method(instance, "ask", "api_type")
        """
        if not hasattr(instance, method_name):
            raise NotImplementedError(
                Messages.get_message(MessageCodes.METHOD_NOT_IMPLEMENTED, api_type=api_type)
            )