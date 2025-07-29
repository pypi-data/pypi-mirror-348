"""
Command-line interface for ZSniff.
"""
import argparse
import signal
import sys
import threading
import time
from typing import List

from .core import ZeroMQSniffer


def main():
    """Entry point for the ZSniff command-line interface."""
    parser = argparse.ArgumentParser(description="Passive ZeroMQ TCP sniffer")
    parser.add_argument("-i", "--interface", required=True, help="Network interface to sniff on (e.g., eth0)")
    parser.add_argument("-p", "--ports", type=int, nargs="+", default=[], help="TCP port(s) to filter (e.g., 5555 6000)")
    parser.add_argument("--raw-hex", action="store_true", help="Show raw frame bytes in hex alongside decoded output")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--session-timeout", type=int, default=300, help="Session timeout in seconds (default: 300)")
    parser.add_argument("--cleanup-interval", type=int, default=60, help="Cleanup interval in seconds (default: 60)")
    parser.add_argument("--max-buffer-size", type=int, default=1024*1024, help="Maximum buffer size per connection in bytes (default: 1MB)")
    parser.add_argument("--tolerance", choices=["low", "medium", "high"], default="medium", 
                      help="Protocol tolerance level (default: medium)")
    parser.add_argument("--stats-interval", type=int, default=0, 
                      help="Display statistics every N seconds (0 to disable, default: 0)")
    
    args = parser.parse_args()
    
    try:
        sniffer = ZeroMQSniffer(
            interface=args.interface,
            ports=args.ports,
            raw_hex=args.raw_hex,
            debug=args.debug,
            session_timeout=args.session_timeout,
            cleanup_interval=args.cleanup_interval,
            max_buffer_size=args.max_buffer_size,
            tolerance_level=args.tolerance
        )
        
        # Start stats display thread if requested
        if args.stats_interval > 0:
            # Flag to control the stats thread
            stop_event = threading.Event()
            
            def display_stats_periodically():
                while not stop_event.is_set():
                    time.sleep(args.stats_interval)
                    sniffer.display_statistics()
            
            # Start stats thread
            stats_thread = threading.Thread(target=display_stats_periodically, daemon=True)
            stats_thread.start()
            
            # Handle termination to display final stats
            def signal_handler(sig, frame):
                stop_event.set()
                print("\n\nFinal Statistics:")
                sniffer.display_statistics()
                sys.exit(0)
                
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
        
        sniffer.start()
    except KeyboardInterrupt:
        print("\n\nSniffer stopped, final statistics:")
        sniffer.display_statistics()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 