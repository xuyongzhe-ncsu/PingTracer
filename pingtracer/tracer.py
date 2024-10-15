import scapy.all as sa
from concurrent.futures import ThreadPoolExecutor


class PingTracer:
    def __init__(self, address_list: list[str]) -> None:
        """
        Initializes the PingTracer instance with a list of addresses.
        Args:
            address_list (list[str]): List of IP addresses to ping and trace.
        """
        self.address_list = address_list
        self.responsive_addr = []  # Stores responsive addresses
        self.un_responsive_addr = []  # Stores unresponsive addresses
        self.max_hops = 30  # Maximum number of hops for traceroute
        self.timeout = 2  # Timeout for responses in seconds

    def ping_addresses(self) -> None:
        """
        Pings the addresses in the address_list and categorizes them as
        responsive or unresponsive.
        """
        # Use ThreadPoolExecutor for concurrent pinging
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit ping tasks for each address
            future_to_host = {executor.submit(self._ping_host, addr): addr for addr in self.address_list}

            for future in future_to_host:
                host = future_to_host[future]
                try:
                    if future.result():  # If the result is True, it's responsive
                        self.responsive_addr.append(host)
                    else:
                        self.un_responsive_addr.append(host)
                except Exception as e:
                    print(f"Error pinging {host}: {e}")

    def _ping_host(self, address: str) -> bool:
        """
        Pings a single address and returns True if it's responsive, else False.
        Args:
            address (str): The IP address to ping.
        Returns:
            bool: True if the host is responsive, False otherwise.
        """
        # Create an ICMP Echo Request packet
        packet = sa.IP(dst=address) / sa.ICMP()

        # Send the packet and wait for a response
        reply = sa.sr1(packet, timeout=self.timeout, verbose=0)

        return reply is not None  # Returns True if a reply is received

    # TODO: make it async
    def trace_route_of_responsive_addr(self) -> None:
        """
        Traces the route to each responsive address and prints the results.
        """
        for addr in self.responsive_addr:
            print(f"Tracing route to {addr}:")
            for ttl in range(1, self.max_hops + 1):
                packet = sa.IP(dst=addr, ttl=ttl) / sa.ICMP()

                # Send the packet and wait for a response
                reply = sa.sr1(packet, verbose=0, timeout=self.timeout)

                if reply is None:
                    print(f"{ttl}: Request timed out")
                elif reply.type == 11:  # ICMP Time Exceeded
                    print(f"{ttl}: {reply.src}")
                elif reply.type == 0:  # ICMP Echo Reply (means we reached the destination)
                    print(f"{ttl}: {reply.src} (Destination reached)")
                    break
