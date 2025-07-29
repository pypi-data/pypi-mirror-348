#!/usr/bin/env python
"""
Inspect the fast_inverted_index module to debug the Arrow integration.
"""

import inspect
import sys
import fast_inverted_index as fii

def inspect_module(module, prefix=''):
    """Recursively inspect a module for attributes."""
    print(f"{prefix}Module: {module.__name__}")
    
    # Print all attributes
    attrs = sorted(dir(module))
    for attr in attrs:
        # Skip private attributes and special methods
        if attr.startswith('_') and attr != '__version__':
            continue
            
        try:
            value = getattr(module, attr)
            
            # Print the attribute and its type
            attr_type = type(value).__name__
            print(f"{prefix}  {attr}: {attr_type}")
            
            # If it's a module, recursively inspect it
            if attr_type == 'module':
                inspect_module(value, prefix + '  ')
                
        except Exception as e:
            print(f"{prefix}  Error inspecting {attr}: {e}")

def inspect_fast_inverted_index():
    """Inspect the fast_inverted_index module."""
    print("Inspecting fast_inverted_index module:")
    inspect_module(fii)
    
    # Print specific information about Arrow functions
    print("\nChecking for Arrow functions:")
    
    # Check in main module
    arrow_funcs = [attr for attr in dir(fii) if 'arrow' in attr.lower() or 'pyarrow' in attr.lower()]
    print(f"Arrow-related functions in main module: {arrow_funcs}")
    
    # Check in _fast_inverted_index
    if hasattr(fii, '_fast_inverted_index'):
        arrow_funcs = [attr for attr in dir(fii._fast_inverted_index) 
                      if 'arrow' in attr.lower() or 'pyarrow' in attr.lower()]
        print(f"Arrow-related functions in _fast_inverted_index: {arrow_funcs}")
        
        # Check add_documents_from_pyarrow specifically
        if hasattr(fii._fast_inverted_index, 'add_documents_from_pyarrow'):
            func = getattr(fii._fast_inverted_index, 'add_documents_from_pyarrow')
            print(f"add_documents_from_pyarrow: {func}")
            print(f"Type: {type(func)}")
            print(f"Signature: {inspect.signature(func)}")
        else:
            print("add_documents_from_pyarrow not found")

if __name__ == '__main__':
    inspect_fast_inverted_index()