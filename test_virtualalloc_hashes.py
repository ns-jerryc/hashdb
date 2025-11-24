#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test script to hash 'VirtualAlloc' using all available algorithms"""

import hashdb

def main():
    test_string = "GetModuleFileNameW"
    algorithms = hashdb.list_algorithms()
    
    print(f"Hashing '{test_string}' with {len(algorithms)} algorithms:\n")
    print("-" * 80)
    
    results = []
    for algo_name in sorted(algorithms):
        try:
            hash_result = hashdb.hash(algo_name, test_string)
            results.append((algo_name, hash_result))
            print(f"{algo_name:50s} : 0x{hash_result:08X} ({hash_result})")
        except Exception as e:
            print(f"{algo_name:50s} : ERROR - {str(e)}")
    
    print("-" * 80)
    print(f"\nTotal algorithms tested: {len(results)}")
    
    return results

if __name__ == "__main__":
    main()
