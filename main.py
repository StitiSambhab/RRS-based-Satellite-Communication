import numpy as np
from scipy.spatial import distance

# Constants
EARTH_RADIUS = 6371  # Radius of Earth in km

# Function to convert lat, lon, and height to Cartesian coordinates
def lat_lon_to_xyz(lat, lon, height):
    lat, lon = np.radians(lat), np.radians(lon)
    r = EARTH_RADIUS + height
    x = r * np.cos(lat) * np.cos(lon)
    y = r * np.cos(lat) * np.sin(lon)
    z = r * np.sin(lat)
    return np.array([x, y, z])

# Check line-of-sight between two points
def has_los(p1, p2):
    mid = (p1 + p2) / 2
    return np.linalg.norm(mid) > EARTH_RADIUS

# Check if an RRS node can help redirect the signal between two points
def has_rrs_path(p1, p2, rrs_nodes):
    for rrs in rrs_nodes:
        if has_los(p1, rrs) and has_los(rrs, p2):
            return True
    return False

# Generate satellite constellation
def generate_satellites(num_planes, sats_per_plane, altitude):
    satellites = []
    for plane in range(num_planes):
        lon_offset = 360 / num_planes * plane
        for sat in range(sats_per_plane):
            lat = np.arcsin(2 * (sat / sats_per_plane) - 1) * 180 / np.pi
            lon = lon_offset + (360 / sats_per_plane) * sat
            satellites.append(lat_lon_to_xyz(lat, lon, altitude))
    return np.array(satellites)

# Generate RRS nodes in space (strategic orbital positions)
def generate_rrs_nodes(satellites, num_rrs):
    rrs_nodes = []
    for i in range(num_rrs):
        # Place RRS nodes randomly in the space between satellites or at strategic points
        random_sat_idx = np.random.choice(len(satellites))
        sat1 = satellites[random_sat_idx]
        
        # Randomize offsets to simulate RRS placed in orbit (between satellite constellations)
        lat_offset = np.random.uniform(-5, 5)  # RRS offset in latitude
        lon_offset = np.random.uniform(-5, 5)  # RRS offset in longitude
        
        new_lat = sat1[0] + lat_offset
        new_lon = sat1[1] + lon_offset
        rrs_nodes.append(lat_lon_to_xyz(new_lat, new_lon, sat1[2]))
    
    return np.array(rrs_nodes)

# Find closest satellite with LOS or RRS assistance
def find_closest_satellite_with_rrs(point, satellites, rrs_nodes):
    distances = []
    for sat in satellites:
        if has_los(point, sat) or has_rrs_path(point, sat, rrs_nodes):
            dist = distance.euclidean(point, sat)
        else:
            dist = np.inf
        distances.append(dist)
    closest_idx = np.argmin(distances)
    return closest_idx if distances[closest_idx] != np.inf else None

# BFS to find the shortest satellite path using LOS or RRS-assisted links
def find_min_satellites_with_rrs(satellites, start_idx, end_idx, rrs_nodes):
    queue = [(start_idx, 0, [])]
    visited = set()

    while queue:
        current, hops, path = queue.pop(0)
        path = path + [current]

        if current == end_idx:
            return hops, path

        visited.add(current)

        for i in range(len(satellites)):
            if i not in visited:
                # Check if there's LOS or RRS path between satellites
                if has_los(satellites[current], satellites[i]) or has_rrs_path(satellites[current], satellites[i], rrs_nodes):
                    queue.append((i, hops + 1, path))

    return -1, []

# ---------- INPUT SECTION ----------
lat1, lon1, h1 = map(float, input("Enter lat, lon, height for Point 1: ").split())
lat2, lon2, h2 = map(float, input("Enter lat, lon, height for Point 2: ").split())
sat_altitude = float(input("Enter satellite altitude (km): "))

num_planes = 4  # Fewer planes for testing
sats_per_plane = 10  # Fewer satellites per plane
num_rrs = 20  # Number of RRS nodes to be placed

# Convert points to Cartesian coordinates
point1 = lat_lon_to_xyz(lat1, lon1, h1)
point2 = lat_lon_to_xyz(lat2, lon2, h2)

# Generate satellites and RRS nodes
satellites = generate_satellites(num_planes, sats_per_plane, sat_altitude)
rrs_nodes = generate_rrs_nodes(satellites, num_rrs)

# Find closest satellites with or without RRS assistance
sat1_idx = find_closest_satellite_with_rrs(point1, satellites, rrs_nodes)
sat2_idx = find_closest_satellite_with_rrs(point2, satellites, rrs_nodes)

print("\n--- WITHOUT RRS ---")
if sat1_idx is None or sat2_idx is None:
    print("No satellite with direct LOS to one or both points.")
else:
    hops, path = find_min_satellites_with_rrs(satellites, sat1_idx, sat2_idx, [])
    print(f"Minimum satellites used (without RRS): {hops}")
    if hops != -1:
        print(f"Path (satellite indices): {path}")
    else:
        print("No valid path found.")

print("\n--- WITH RRS ---")
sat1_idx = find_closest_satellite_with_rrs(point1, satellites, rrs_nodes)
sat2_idx = find_closest_satellite_with_rrs(point2, satellites, rrs_nodes)

if sat1_idx is None or sat2_idx is None:
    print("Even with RRS, no satellite connection possible.")
else:
    hops, path = find_min_satellites_with_rrs(satellites, sat1_idx, sat2_idx, rrs_nodes)
    print(f"Minimum satellites used (with RRS): {hops}")
    if hops != -1:
        print(f"Path (satellite indices): {path}")
    else:
        print("No valid path found.")
