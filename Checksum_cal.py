def calculate_checksum(data_bytes):
    """
    Calculate the checksum for a given list of data bytes using 16-bit (2-byte) checksum.

    :param data_bytes: List of integers (bytes) to calculate checksum for
    :return: Calculated checksum as a 2-byte integer
    """
    total = sum(data_bytes)  # Sum all the bytes
    checksum = 0xFFFF - total + 1  # Apply 16-bit 2's complement
    checksum &= 0xFFFF  # Ensure it's within 2 bytes (16 bits)
    return checksum

# Example data packet (excluding Frame start (0x7A), Frame end (0x7F), and checksum itself)
data_packet = [
    0x16, 0x01, 0x00, 0x0A, 0x01, 0x23, 0x28, 0xFF,
    0x00, 0x05, 0x00, 0x08, 0x04, 0x2C, 0x0D, 0xB5,
    0x30, 0xD4
]

# Calculate the checksum
calculated_checksum = calculate_checksum(data_packet)

# Convert to hex for readability
print(f"Calculated checksum: {calculated_checksum:04X}")
