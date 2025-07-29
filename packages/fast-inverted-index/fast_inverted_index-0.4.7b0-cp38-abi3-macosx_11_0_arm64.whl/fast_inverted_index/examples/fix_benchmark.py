#!/usr/bin/env python
"""
Attempt to import the Arrow functions from fast_inverted_index and list available functions.
"""

import sys
import inspect
import fast_inverted_index as fii

# Print all available attributes in the module
print("Available attributes in fast_inverted_index:")
for attr in dir(fii):
    if not attr.startswith('_'):  # Skip private attributes
        print(f"- {attr}")
        
        # If it's a callable (function or method), print its signature
        if callable(getattr(fii, attr)):
            try:
                signature = inspect.signature(getattr(fii, attr))
                print(f"  Signature: {attr}{signature}")
            except (ValueError, TypeError):
                print(f"  (Could not determine signature)")
        
        # If it's a class, print its methods
        if inspect.isclass(getattr(fii, attr)):
            print(f"  (Class)")
            for method in dir(getattr(fii, attr)):
                if not method.startswith('_'):
                    print(f"    - {method}")