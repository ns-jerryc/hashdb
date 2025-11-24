#!/usr/bin/env python

DESCRIPTION = """
LockBit 5 hash algorithm with character normalization (case-insensitive for A-Z).
Uses XOR, multiplication with index-based modifiers (0x9599), and iterative hash updates.
"""
TYPE = 'GetModuleFileNameW'
TEST_1 = 0x7FE92CAF  # Add your test value here if you have one


def hash(data):
    """
    Calculates the 32-bit hash based on the LockBit 5 assembly routine.

    Args:
        data: The string or bytes to hash (e.g., "LoadLibraryA").

    Returns:
        The final 32-bit hash value.
    """
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    
    # Initialize 32-bit registers (using Python integers)
    eax = 0x9599  # initial_hash
    ecx = 0  # Loop counter

    # Loop through the characters of the API name
    for char in data:
        # Get the ASCII value of the current character
        r8d = ord(char)

        # --- Character Normalization (Case-Insensitivity for 'A'-'Z') ---
        # r9d = r8d - 0x41 ('A')
        r9d = (r8d - 0x41) & 0xFFFFFFFF
        # r10d = r8d + 0x20
        r10d = (r8d + 0x20) & 0xFFFFFFFF

        # cmp r9b, 1Ah (Check if 0 <= r9d < 0x1A, i.e., 'A' <= r8d <= 'Z')
        # We only care about the lower 8 bits (r9b) for the comparison
        r9b = r9d & 0xFF

        # cmovnb r10d, r8d: If NOT below (i.e., not 'A'-'Z'), r10d = r8d
        if r9b >= 0x1A:
            r10d = r8d
        # If it IS 'A'-'Z', r10d remains the lowercase version (r8d + 0x20)
        # r10d now holds the case-normalized character's ASCII value

        # --- Hash Update 1 ---
        # xor eax, r10d
        eax = (eax ^ r10d) & 0xFFFFFFFF

        # lea r8d, [rcx+9599h]
        r8d = (ecx + 0x9599) & 0xFFFFFFFF

        # imul r8d, r10d
        r8d = (r8d * r10d) & 0xFFFFFFFF

        # add r8d, eax
        r8d = (r8d + eax) & 0xFFFFFFFF

        # --- Hash Update 2 ---
        # mov eax, ecx
        eax_temp = ecx

        # xor eax, 9599h
        eax_temp = (eax_temp ^ 0x9599) & 0xFFFFFFFF

        # test ecx, ecx / cmovz eax, ecx
        # If ecx is 0 (first iteration), set eax_temp to 0, effectively overriding the XOR.
        if ecx == 0:
            eax_temp = ecx  # eax_temp becomes 0

        # imul eax, r8d
        eax = (eax_temp * r8d) & 0xFFFFFFFF

        # add eax, r10d
        eax = (eax + r10d) & 0xFFFFFFFF

        # --- Loop Increment ---
        # inc ecx
        ecx = (ecx + 1) & 0xFFFFFFFF

    return eax
