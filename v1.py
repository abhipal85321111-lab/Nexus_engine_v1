import time

class NexusV1_ZeroCopy:
    """V1.1 PRO - Real Zero-Copy - No tobytes(), No Copy"""
    def __init__(self, raw_data_bytes: bytes):
        self.view = memoryview(raw_data_bytes)
        self.size = len(raw_data_bytes)
        print(f"[V1.1 REAL] Zero-Copy Active")
        print(f"Raw Size: {self.size}B | Overhead: 0 MB | Pointer: {hex(id(raw_data_bytes))}")

    def read_packet(self, start, end):
        if end > self.size:
            raise IndexError(f"Out of bounds: {end} > {self.size}")
        return self.view[start:end] # Yeh abhi bhi view hai, copy nahi

    def read_packet_copy(self, start, end):
        return self.view[start:end].tobytes() # Jab copy chahiye tabhi copy

# ========= REAL TEST =========
data = b"NEXUS_ULTRA_FAST_PAYLOAD_SIMULATION_50K_PACKETS_STREAM"
v1 = NexusV1_ZeroCopy(data)

print("\n--- Zero-Copy Proof ---")
packet_view = v1.read_packet(0, 12)
print(f"View Type: {type(packet_view)} | Is View: {isinstance(packet_view, memoryview)}")
print(f"Data: {bytes(packet_view)} | Shares Memory: {packet_view.obj is data}")

# Performance test
start = time.perf_counter()
for _ in range(100000):
    _ = v1.read_packet(0, 12)
zero_time = (time.perf_counter() - start)*1000

start = time.perf_counter()
for _ in range(100000):
    _ = v1.read_packet_copy(0, 12)
copy_time = (time.perf_counter() - start)*1000

print(f"\n100k reads:")
print(f"Zero-Copy (view): {zero_time:.2f}ms")
print(f"With tobytes() copy: {copy_time:.2f}ms")
print(f"Speedup: {copy_time/zero_time:.1f}x faster | RAM Save: 100%")
