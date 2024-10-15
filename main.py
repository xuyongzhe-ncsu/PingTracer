from pingtracer.tracer import PingTracer

if __name__ == "__main__":
    # Read IP addresses from the specified file, skipping the first line
    with open('./data/ipv4.txt', 'r') as file:
        address_list = [line.strip() for line in file.readlines()[1:]]  # Skip header line

    # Create an instance of PingTracer with the first 10 addresses
    ping_tracer = PingTracer(address_list[:10])  # Use slicing for clarity

    # Ping the addresses and categorize them
    ping_tracer.ping_addresses()

    # Print the number of responsive and unresponsive addresses
    print(f"Number of responsive addresses: {len(ping_tracer.responsive_addr)}")
    print(f"Number of unresponsive addresses: {len(ping_tracer.un_responsive_addr)}")

    # Trace the route to each responsive address
    ping_tracer.trace_route_of_responsive_addr()
