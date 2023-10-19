"""
File: Roles.py
Author: Danyal Mohaddes
Description: This file contains the Roles enumeration.
"""

from enum import Enum

class Roles(Enum):
     """Enumeration containing the `role` attributes permitted by the OpenAI API for the GPT models."""
     system = 0
     user = 1
     assistant = 2
     
