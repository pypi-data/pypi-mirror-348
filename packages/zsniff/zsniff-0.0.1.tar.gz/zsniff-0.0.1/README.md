# ZSniff - ZeroMQ Protocol Analyzer and Traffic Sniffer

ZSniff is a passive network protocol analyzer for ZeroMQ (ØMQ) that lets you inspect, debug, and understand the traffic between ZeroMQ applications without modifying the target systems.

## Features

- **Live Traffic Capture**: Capture and analyze ZeroMQ traffic in real-time
- **Protocol Detection**: Automatically detects ZMTP/1.0, 2.0, and 3.x protocols
- **Message Patterns**: Identifies ZeroMQ messaging patterns (PUB-SUB, REQ-REP, PUSH-PULL, etc.)
- **Message Visualization**: Human-readable display of message contents
- **Smart JSON Parsing**: Automatically formats and displays JSON payloads
- **Topic Analysis**: Identifies and tracks topics in PUB-SUB patterns
- **Request-Response Correlation**: Matches requests with their responses
- **Error Recovery**: Robust error handling for partial or malformed streams
- **Statistics**: Real-time statistics about socket types, bytes transferred, etc.

## Installation

ZSniff requires Python 3.8 or newer.

### From PyPI

```bash
pip install zsniff
```

### From Source

```bash
git clone https://github.com/yourusername/zsniff.git
cd zsniff
pip install -e .
```

## Usage

ZSniff needs access to the network traffic to analyze it, so it requires root privileges to use packet capture capabilities.

Basic usage:

```bash
sudo zsniff -i eth0 -p 5555
```

Where:
- `-i eth0` specifies the network interface to capture on
- `-p 5555` specifies the ZeroMQ port to monitor (can specify multiple ports)

### Command-line Options

```
usage: zsniff [-h] -i INTERFACE [-p PORTS [PORTS ...]] [--raw-hex] [--debug]
              [--session-timeout SESSION_TIMEOUT]
              [--cleanup-interval CLEANUP_INTERVAL]
              [--max-buffer-size MAX_BUFFER_SIZE]
              [--tolerance {low,medium,high}]
              [--stats-interval STATS_INTERVAL]

Passive ZeroMQ TCP sniffer

required arguments:
  -i INTERFACE, --interface INTERFACE
                        Network interface to sniff on (e.g., eth0)

optional arguments:
  -h, --help            show this help message and exit
  -p PORTS [PORTS ...], --ports PORTS [PORTS ...]
                        TCP port(s) to filter (e.g., 5555 6000)
  --raw-hex             Show raw frame bytes in hex alongside decoded output
  --debug               Enable debug mode
  --session-timeout SESSION_TIMEOUT
                        Session timeout in seconds (default: 300)
  --cleanup-interval CLEANUP_INTERVAL
                        Cleanup interval in seconds (default: 60)
  --max-buffer-size MAX_BUFFER_SIZE
                        Maximum buffer size per connection in bytes (default: 1MB)
  --tolerance {low,medium,high}
                        Protocol tolerance level (default: medium)
  --stats-interval STATS_INTERVAL
                        Display statistics every N seconds (0 to disable, default: 0)
```

## Example Output

When capturing ZeroMQ traffic, ZSniff will display the detected messages in a structured way:

```
[Session 3a2b1c4d] [PUB-SUB/PUB] 192.168.1.10:5555 -> 192.168.1.20:49152
Envelope: updates | Content: {"temperature": 22.5, "humidity": 45, "timestamp": 1632481582}

[Session 3a2b1c4d] [PUB-SUB/PUB] 192.168.1.10:5555 -> 192.168.1.21:49153
Envelope: updates | Content: {"temperature": 22.6, "humidity": 46, "timestamp": 1632481583}
```

For REQ-REP patterns:

```
[Session 9f8e7d6c] [REQ-REP/REQ] 192.168.1.30:49254 -> 192.168.1.10:5556
Content: [bold magenta]get_data[/bold magenta] | req: 123abc45...

[Session 9f8e7d6c] [REQ-REP/REP] 192.168.1.10:5556 -> 192.168.1.30:49254
Content: [bold magenta]get_data_response[/bold magenta] | req: 123abc45... | status: success
```

## Architecture

ZSniff is composed of several components:

1. **Packet Capture**: Uses the scapy library to capture network packets
2. **Protocol Parsing**: Detects and parses ZeroMQ frames and messages
3. **Session Tracking**: Maintains state for each ZeroMQ connection
4. **Message Analysis**: Interprets message contents and patterns
5. **Visualization**: Renders analyzed messages in a human-readable format

## How It Works

ZSniff passively monitors network traffic, looking for ZeroMQ communication patterns. It:

1. Captures TCP packets on specified ports
2. Reassembles them into byte streams for each connection
3. Identifies ZMTP protocol versions from handshake
4. Detects and parses frame boundaries
5. Interprets frame contents and message patterns
6. Displays messages in a human-readable format with context
7. Tracks statistics about traffic patterns and volumes

## Security Considerations

ZSniff analyzes traffic in memory and does not store or transmit the captured data. However, it does have access to all the data being transferred over ZeroMQ, which may include sensitive information. Use it only in environments where you have authorization to monitor the network traffic.

## Limitations

- ZSniff can only analyze cleartext (unencrypted) ZeroMQ communications. It will identify but cannot decode CURVE or GSSAPI encrypted traffic.
- It must see both directions of traffic to fully analyze connection patterns.
- Some advanced ZeroMQ patterns or custom extensions may not be fully recognized.
- Performance may be affected when analyzing high-throughput ZeroMQ communications.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The ZeroMQ project (https://zeromq.org/)
- The scapy project for packet capturing capabilities
- The rich library for beautiful terminal output 