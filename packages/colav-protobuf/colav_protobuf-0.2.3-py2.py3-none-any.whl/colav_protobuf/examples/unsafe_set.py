from colav_protobuf import UnsafeSet

# Mock an unsafe set proto message
unsafe_set = UnsafeSet()
unsafe_set.mission_tag = "COLAV_MISSION_NORTH_BELFAST_TO_SOUTH_FRANCE"
unsafe_set.stamp.sec = 1234
unsafe_set.stamp.nanosec = 1235

# Define meaningful polygon coordinates (example: a simple rectangle)
coordinates = [(10, 5), (15, 5), (15, 10), (10, 10)]

# Add coordinates to the proto message
for x, y in coordinates:
    coord = unsafe_set.vertices.add()
    coord.x = x
    coord.y = y
    coord.z = 0