import pytest
import math
import time
from backend.spatial_utils import haversine_distance, equirectangular_distance

def test_haversine_distance_correctness():
    # New York to London
    lat1, lon1 = 40.7128, -74.0060
    lat2, lon2 = 51.5074, -0.1278

    expected_km = 5570
    calculated_m = haversine_distance(lat1, lon1, lat2, lon2)
    calculated_km = calculated_m / 1000

    # Allow 1% error margin
    assert abs(calculated_km - expected_km) < 56

def test_haversine_distance_small_distance():
    # Two points close to each other (approx 111m apart in latitude)
    lat1, lon1 = 40.000, -74.000
    lat2, lon2 = 40.001, -74.000

    calculated_m = haversine_distance(lat1, lon1, lat2, lon2)

    # 0.001 degree lat is approx 111.32 meters
    expected_m = 111.32
    assert abs(calculated_m - expected_m) < 1

def test_equirectangular_distance_correctness_small():
    # Two points close to each other (approx 111m apart in latitude)
    lat1, lon1 = 40.000, -74.000
    lat2, lon2 = 40.001, -74.000

    calculated_m = equirectangular_distance(lat1, lon1, lat2, lon2)

    # 0.001 degree lat is approx 111.32 meters
    expected_m = 111.32
    # Should be very close for small distances
    assert abs(calculated_m - expected_m) < 1

def benchmark_distance_functions():
    lat1, lon1 = 40.7128, -74.0060
    lat2, lon2 = 40.7138, -74.0050 # Close points

    iterations = 1000000

    start_time = time.time()
    for _ in range(iterations):
        haversine_distance(lat1, lon1, lat2, lon2)
    haversine_time = time.time() - start_time

    start_time = time.time()
    for _ in range(iterations):
        equirectangular_distance(lat1, lon1, lat2, lon2)
    equirectangular_time = time.time() - start_time

    print(f"Haversine 1M calls: {haversine_time:.4f}s")
    print(f"Equirectangular 1M calls: {equirectangular_time:.4f}s")
    print(f"Speedup: {haversine_time / equirectangular_time:.2f}x")

if __name__ == "__main__":
    benchmark_distance_functions()
