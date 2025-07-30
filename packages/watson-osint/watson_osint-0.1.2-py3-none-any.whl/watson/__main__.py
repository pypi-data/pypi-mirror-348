#!/usr/bin/env python3
"""
Point d'entrée principal pour l'application Watson OSINT
"""

import os
import sys
from core.watson import main

if __name__ == "__main__":
    # Appel direct à la fonction main de watson.py
    main()