"""
Core ZeroMQ sniffer implementation.
"""
from __future__ import annotations

import time
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from scapy.all import sniff, TCP

from .models import Session, PatternType
from .parsers import FrameParser
from .processor import MessageProcessor
from .utils import (
    format_bytes_count,
    format_duration,
    detect_zmtp_mechanism,
    detect_zmtp_role,
    normalize_zmtp_version,
    format_bytes
)


class ZeroMQSniffer:
    """Main ZeroMQ sniffer class for capturing and analyzing network traffic."""
    
    def __init__(
        self,
        interface: str,
        ports: List[int],
        raw_hex: bool = False,
        debug: bool = False,
        session_timeout: int = 300,  # Session timeout in seconds
        cleanup_interval: int = 60,  # Cleanup interval in seconds
        max_buffer_size: int = 1024 * 1024,  # 1MB max buffer size per connection
        tolerance_level: str = "medium",  # How tolerant of non-standard behavior
        group_related_messages: bool = True,  # Group related messages (request/response pairs)
    ):
        """
        Initialize the ZeroMQ sniffer.
        
        Args:
            interface: Network interface to capture on
            ports: TCP ports to filter
            raw_hex: Show raw frame bytes in hex
            debug: Enable debug output
            session_timeout: Session timeout in seconds
            cleanup_interval: Cleanup interval in seconds
            max_buffer_size: Maximum buffer size per connection in bytes
            tolerance_level: Protocol tolerance level (low, medium, high)
            group_related_messages: Group related messages (request/response pairs)
        """
        self.interface = interface
        self.ports = ports
        self.raw_hex = raw_hex
        self.debug = debug
        self.session_timeout = session_timeout
        self.cleanup_interval = cleanup_interval
        self.max_buffer_size = max_buffer_size
        self.tolerance_level = tolerance_level
        self.group_related_messages = group_related_messages
        
        # Connection tracking
        self.buffers: Dict[Tuple[str, int, str, int], bytearray] = {}
        self.protocol: Dict[Tuple[str, int, str, int], str] = {}
        self.current_message: Dict[Tuple[str, int, str, int], List] = {}
        self.conn_sessions: Dict[Tuple[str, int, str, int], str] = {}
        self.sessions: Dict[str, Session] = {}
        
        # Track peer relations between sessions
        self.session_peers: Dict[str, str] = {}
        
        # Console for rich output
        self.console = Console()
        
        # Create frame parser and message processor
        self.frame_parser = FrameParser(max_buffer_size=max_buffer_size, debug=debug)
        self.message_processor = MessageProcessor(
            debug=debug,
            raw_hex=raw_hex,
            tolerance_level=tolerance_level,
            console=self.console
        )
        
        # Statistics and error tracking
        self.last_cleanup_time = time.time()
        self.last_stats_time = time.time()
        self.stats = {
            "total_packets": 0,
            "total_frames": 0,
            "valid_frames": 0,
            "parse_errors": 0,
            "recovery_attempts": 0,
            "dropped_bytes": 0,
            "current_throughput": 0,
            "peak_throughput": 0,
            "bytes_processed": 0,
            "start_time": datetime.now(),
            "socket_types": defaultdict(int),
            "pattern_types": defaultdict(int)
        }
        
        # Recovery cache to avoid repeating same errors
        self.recovery_cache: Dict[bytes, int] = {}
        self.recovery_cache_size = 100  # Max number of patterns to remember
        
        # Store stale connection keys for cleanup
        self.stale_connections: Set[Tuple[str, int, str, int]] = set()
        
        # Known flag bit patterns for extensions
        self.known_flag_extensions = {
            0x10: "ZMQ_MSG_COMMAND", # Command frame in some implementations
            0x20: "ZMQ_MSG_LARGE",   # Large message extension
            0x40: "ZMQ_MSG_SHARED",  # Shared storage
            0x80: "ZMQ_MSG_MASK"     # Mask for other extensions
        }
        
        # Performance tracking
        self.throughput_history: List[int] = []
        self.max_history_points = 60  # 1 minute history at 1s intervals

    def start(self):
        """Start the ZeroMQ sniffer to capture and analyze traffic."""
        port_filters = [f"port {p}" for p in self.ports]
        filter_str = "tcp and (" + " or ".join(port_filters) + ")" if self.ports else "tcp"
        self.console.print(f"[bold green]Starting ZeroMQ sniffer on interface {self.interface}[/bold green] (filter: {filter_str})")
        if self.debug:
            self.console.print("[yellow]Debug mode enabled - detailed protocol debugging information will be shown[/yellow]")
        self.console.print(f"[dim]Session timeout: {self.session_timeout}s, Cleanup interval: {self.cleanup_interval}s[/dim]")
        self.console.print(f"[dim]Protocol tolerance: {self.tolerance_level}, Group related messages: {self.group_related_messages}[/dim]")
        sniff(iface=self.interface, filter=filter_str, store=False, prn=self.process_packet)

    def process_packet(self, pkt):
        """Process a captured packet for ZeroMQ analysis."""
        if not pkt.haslayer(TCP):
            return
            
        # Track statistics
        self.stats["total_packets"] += 1
        
        # Periodically cleanup stale connections
        self.cleanup_stale_connections()
        
        ip = pkt.payload
        tcp = pkt[TCP]
        data = bytes(tcp.payload)
        conn_key = (ip.src, tcp.sport, ip.dst, tcp.dport)

        # Skip if this is a connection we've already marked as stale
        if conn_key in self.stale_connections:
            return

        # Detect TCP connection close
        if not data and (tcp.flags & 0x01 or tcp.flags & 0x04):  # FIN or RST
            session_id = self.conn_sessions.get(conn_key)
            if session_id:
                session = self.sessions.get(session_id)
                if session:
                    session.end_time = datetime.now()
                    self.console.print(f"[bold blue]Session {session_id[:8]} ended[/bold blue] messages: {len(session.messages)} duration: {session.end_time - session.start_time}")
            self.buffers.pop(conn_key, None)
            self.protocol.pop(conn_key, None)
            self.current_message.pop(conn_key, None)
            self.conn_sessions.pop(conn_key, None)
            self.stale_connections.add(conn_key)
            return

        # Initialize new connection
        if conn_key not in self.buffers:
            self.buffers[conn_key] = bytearray()
            self.protocol[conn_key] = "unknown"
            self.current_message[conn_key] = []
            session_id = str(uuid.uuid4())
            self.conn_sessions[conn_key] = session_id
            self.sessions[session_id] = Session(
                session_id=session_id,
                src=ip.src,
                src_port=tcp.sport,
                dst=ip.dst,
                dst_port=tcp.dport,
                start_time=datetime.now(),
                last_activity=datetime.now()
            )
        elif self.protocol.get(conn_key) == "unsupported":
            return

        # Update session activity time
        session_id = self.conn_sessions.get(conn_key)
        if session_id and session_id in self.sessions:
            self.sessions[session_id].last_activity = datetime.now()

        if self.debug and data:
            self.console.print(f"[dim]Debug: Received {len(data)} bytes from {conn_key}: {data.hex()}[/dim]")
            
        # Check if buffer exceeds maximum size
        if len(self.buffers[conn_key]) + len(data) > self.max_buffer_size:
            overflow = len(self.buffers[conn_key]) + len(data) - self.max_buffer_size
            self.console.print(f"[bold yellow]Warning:[/bold yellow] Buffer overflow for {conn_key}, dropping {overflow} bytes")
            self.stats["dropped_bytes"] += overflow
            # Try to keep the most recent data instead of just truncating
            if len(data) < self.max_buffer_size:
                # Keep most recent data and add new data
                new_size = self.max_buffer_size - len(data)
                self.buffers[conn_key] = self.buffers[conn_key][-new_size:]
            else:
                # Only keep the most recent data
                self.buffers[conn_key].clear()
                data = data[-self.max_buffer_size:]
                
        self.buffers[conn_key].extend(data)
        try:
            self._parse_buffer(conn_key)
        except Exception as e:
            self.stats["parse_errors"] += 1
            self.console.print(f"[bold red]Error:[/bold red] Failed to parse data from {conn_key}: {e}")
            if self.debug:
                import traceback
                self.console.print(f"[dim]Debug: Exception: {traceback.format_exc()}[/dim]")

    def _parse_buffer(self, conn_key):
        """Parse as many complete frames as possible from the buffer for a given connection."""
        buf = self.buffers[conn_key]
        
        # Don't process empty buffers
        if not buf:
            return
            
        # Handle handshake if not done yet
        if self.protocol[conn_key] == "unknown":
            if len(buf) >= 10:
                # Detect ZMTP v3.x greeting signature (0xFF ... 0x7F)
                if buf[0] == 0xFF and buf[9] == 0x7F:
                    if len(buf) < 64:
                        return  # wait for full 64-byte greeting
                        
                    major = buf[10]
                    minor = buf[11]
                    
                    # Validate and normalize the version numbers
                    major, minor = normalize_zmtp_version(major, minor, self.debug)
                    
                    # Extract and validate security mechanism
                    mech_bytes = bytes(buf[12:32])
                    mech = detect_zmtp_mechanism(mech_bytes, self.debug)
                    
                    # Extract and validate role
                    as_server = buf[32]
                    role = detect_zmtp_role(as_server, self.debug)
                    
                    # Remove greeting bytes from buffer
                    del buf[:64]
                    self.protocol[conn_key] = "zmtp3"
                    self.console.print(f"[bold blue]Handshake:[/bold blue] ZMTP {major}.{minor} ({mech} mechanism, {role})")
                    
                    # Update session information
                    session_id = self.conn_sessions.get(conn_key)
                    if session_id:
                        session = self.sessions.get(session_id)
                        if session:
                            session.protocol = f"ZMTP {major}.{minor}"
                            session.mechanism = mech
                            session.role = role
                            
                    if mech and mech != "NULL" and not mech.startswith("CUSTOM:"):
                        # Non-NULL security (e.g. PLAIN, CURVE) – content may be encrypted
                        self.console.print(f"[yellow]Note:[/yellow] Security mechanism is {mech}, content might be encrypted or unsupported")
                else:
                    # Possibly ZMTP/1.0 or 2.0 (identity frame greeting)
                    try:
                        frame, consumed = self.frame_parser.parse_zmtp2_frame(buf)
                    except Exception as e:
                        self.console.print(f"[bold red]Error:[/bold red] Failed to parse ZMTP 1.0/2.0 handshake: {e}")
                        # Try to find a valid frame start if we failed
                        skip_bytes = self.frame_parser.try_find_next_frame(buf)
                        if skip_bytes > 0:
                            self.console.print(f"[yellow]Recovery:[/yellow] Skipping {skip_bytes} bytes to find valid handshake")
                            del buf[:skip_bytes]
                        return
                        
                    if frame is None:
                        return
                    del buf[:consumed]
                    self.protocol[conn_key] = "zmtp2"
                    
                    # Update session information
                    session_id = self.conn_sessions.get(conn_key)
                    if session_id:
                        session = self.sessions.get(session_id)
                        if session:
                            session.protocol = "ZMTP 2.x"
                            
                    if frame.body == b'':
                        self.console.print("[bold blue]Handshake:[/bold blue] ZMTP 2.x anonymous identity (no identity)")
                    else:
                        ident = format_bytes(frame.body)
                        self.console.print(f"[bold blue]Handshake:[/bold blue] ZMTP 2.x identity = {ident}")
        
        # Parse all available frames from buffer
        consecutive_errors = 0  # Track consecutive errors to avoid infinite loop
        max_consecutive_errors = 3  # Maximum allowed consecutive errors before marking as unsupported
        max_frames_per_batch = 100  # Limit frames processed in one batch to prevent blocking
        frames_processed = 0
        
        while frames_processed < max_frames_per_batch:
            if consecutive_errors >= max_consecutive_errors:
                # Too many consecutive errors, mark as unsupported
                self.console.print(f"[bold red]Error:[/bold red] Too many parse errors on {conn_key}, marking as unsupported")
                self.protocol[conn_key] = "unsupported"
                buf.clear()
                return
                
            if self.protocol.get(conn_key) == "unsupported":
                buf.clear()
                return  # stop parsing this connection
                
            # Sanity check: minimum buffer size for any valid frame
            if len(buf) < 2:
                return  # need more data
                
            # Choose appropriate frame parser based on protocol
            if self.protocol.get(conn_key) == "zmtp3":
                parse_func = self.frame_parser.parse_zmtp3_frame
            elif self.protocol.get(conn_key) == "zmtp2":
                parse_func = self.frame_parser.parse_zmtp2_frame
            else:
                # Protocol still unknown (no handshake seen, possibly attached mid-stream)
                # Try to autodetect the protocol based on what the buffer looks like
                if len(buf) >= 10 and buf[0] == 0xFF and buf[9] == 0x7F:
                    # This looks like a ZMTP 3.x greeting
                    if self.debug:
                        self.console.print(f"[dim]Debug: Auto-detected ZMTP 3.x greeting at buffer start[/dim]")
                    self.protocol[conn_key] = "zmtp3"
                    continue
                    
                # Try parsing with ZMTP3, if fails then ZMTP2
                try:
                    frame, consumed = self.frame_parser.parse_zmtp3_frame(buf)
                except Exception:
                    try:
                        frame, consumed = self.frame_parser.parse_zmtp2_frame(buf)
                    except Exception:
                        self.console.print(f"[bold red]Error:[/bold red] Unrecognized data on {conn_key} (not valid ZMTP)")
                        self.protocol[conn_key] = "unsupported"
                        buf.clear()
                        return
                    if frame is None:
                        return  # incomplete old frame
                    self.protocol[conn_key] = "zmtp2"
                    
                    # Update session information
                    session_id = self.conn_sessions.get(conn_key)
                    if session_id:
                        session = self.sessions.get(session_id)
                        if session:
                            session.protocol = "ZMTP 2.x"
                else:
                    if frame is None:
                        return  # incomplete new frame
                    self.protocol[conn_key] = "zmtp3"
                    
                    # Update session information for auto-detected protocol
                    session_id = self.conn_sessions.get(conn_key)
                    if session_id:
                        session = self.sessions.get(session_id)
                        if session:
                            session.protocol = "ZMTP 3.x"
                # Loop back now that protocol is set
                continue
                
            # Parse one frame using the selected protocol
            try:
                frame, consumed = parse_func(buf)
                consecutive_errors = 0  # Reset on success
            except Exception as e:
                # Try to recover - find next potential frame start
                self.stats["parse_errors"] += 1
                self.console.print(f"[bold red]Error:[/bold red] Invalid frame on {conn_key}: {e}")
                consecutive_errors += 1
                
                if len(buf) > 0:
                    # Try to find the next valid frame start
                    skip_bytes = self.frame_parser.try_find_next_frame(buf)
                    if skip_bytes > 0:
                        self.console.print(f"[yellow]Recovery:[/yellow] Skipping {skip_bytes} bytes to find next valid frame")
                        self.stats["dropped_bytes"] += skip_bytes
                        del buf[:skip_bytes]
                    else:
                        # Fallback to skipping one byte
                        self.stats["dropped_bytes"] += 1
                        del buf[0]
                    continue
                else:
                    return
                
            if frame is None:
                # Incomplete frame, wait for more data
                return
                
            # Remove parsed bytes and append the frame to the current message
            del buf[:consumed]
            self.current_message[conn_key].append(frame)
            frames_processed += 1
            
            # If we've processed a lot of frames, update the session activity time
            if frames_processed % 10 == 0:
                session_id = self.conn_sessions.get(conn_key)
                if session_id and session_id in self.sessions:
                    self.sessions[session_id].last_activity = datetime.now()
            
            if not frame.more:
                # End of message reached
                frames = self.current_message[conn_key][:]
                self._output_message(conn_key, frames)
                self.current_message[conn_key] = []
                
    def _output_message(self, conn_key, frames):
        """Display a complete ZeroMQ message (possibly multi-frame) to the console."""
        session_id = self.conn_sessions.get(conn_key)
        if not session_id:
            # This shouldn't happen, but just in case
            self.console.print(f"[bold red]Error:[/bold red] No session found for connection {conn_key}")
            return
            
        session = self.sessions.get(session_id)
        if not session:
            # Another edge case
            self.console.print(f"[bold red]Error:[/bold red] Session {session_id} not found")
            return
            
        # Build prefix including session and socket type
        src = f"{conn_key[0]}:{conn_key[1]}"
        dst = f"{conn_key[2]}:{conn_key[3]}"
        
        # Add socket type info if available
        socket_info = ""
        if session.socket_type:
            if session.pattern != PatternType.UNKNOWN:
                socket_info = f"[{session.pattern}/{session.socket_type}]"
            else:
                socket_info = f"[{session.socket_type}]"
                
        # Create the message prefix
        prefix = f"[grey58][Session {session_id[:8]}]{socket_info} {src} -> {dst}[/grey58]"
        
        # Track message size for statistics
        total_msg_size = sum(len(frame.body) for frame in frames)
        session.total_bytes += total_msg_size
        
        # Update throughput statistics
        self.stats["bytes_processed"] += total_msg_size
        current_time = time.time()
        time_diff = current_time - self.last_stats_time
        if time_diff >= 1.0:  # Update throughput every second
            self.stats["current_throughput"] = self.stats["bytes_processed"] / time_diff
            if self.stats["current_throughput"] > self.stats["peak_throughput"]:
                self.stats["peak_throughput"] = self.stats["current_throughput"]
            self.stats["bytes_processed"] = 0
            self.last_stats_time = current_time
            # Add to history
            self.throughput_history.append(int(self.stats["current_throughput"]))
            if len(self.throughput_history) > self.max_history_points:
                self.throughput_history.pop(0)
        
        # Better handle the common single-frame case
        if len(frames) == 1:
            frame = frames[0]
            
            # Special case: empty frame is common in ZeroMQ for heartbeats/keepalives
            if frame.length == 0:
                self.console.print(f"{prefix} [dim]Empty frame[/dim] (likely heartbeat/keepalive)")
                # Record message in session
                message_data = {
                    'timestamp': datetime.now(),
                    'type': 'heartbeat',
                    'size': 0,
                    'frames': [{'flags': frame.flags, 'body': frame.body.hex(), 'command': False}]
                }
                session.add_message(message_data, total_msg_size)
                return
                
            # Handle command frame (like READY commands with socket info)
            if frame.command:
                self.message_processor.process_command_frame(
                    prefix, frame, session, total_msg_size,
                    self.protocol.get(conn_key, "zmtp3"),
                    self.sessions, self.conn_sessions, self.session_peers
                )
                return
        
        # Multi-frame message - handle it with the processor
        self.message_processor.process_multiframe_message(
            prefix, frames, session,
            self.protocol.get(conn_key, "zmtp3"),
            total_msg_size, self.sessions, self.session_peers
        )
        
    def cleanup_stale_connections(self):
        """Remove stale connections and sessions based on timeout."""
        current_time = time.time()
        # Only run cleanup periodically to avoid unnecessary overhead
        if current_time - self.last_cleanup_time < self.cleanup_interval:
            return
            
        self.last_cleanup_time = current_time
        current_datetime = datetime.now()
        
        # Find stale connections
        stale_keys = []
        for conn_key, session_id in self.conn_sessions.items():
            session = self.sessions.get(session_id)
            if session:
                # Check if session is stale
                inactive_time = (current_datetime - session.last_activity).total_seconds()
                if inactive_time > self.session_timeout:
                    # Mark this connection as stale
                    stale_keys.append(conn_key)
                    
                    # Mark session as ended if not already
                    if not session.end_time:
                        session.end_time = current_datetime
                        
                    # Final pattern detection and summary
                    session.update_summary()
                    
                    # Log session closing
                    if self.debug:
                        self.console.print(f"[dim]Debug: Closed session {session_id} due to inactivity ({inactive_time:.1f}s)[/dim]")
                        
        # Clean up stale connections
        for key in stale_keys:
            if key in self.buffers:
                del self.buffers[key]
            if key in self.protocol:
                del self.protocol[key]
            if key in self.current_message:
                del self.current_message[key]
            if key in self.conn_sessions:
                del self.conn_sessions[key]
                
        # Keep sessions for historical analysis but limit the total
        max_sessions = 1000  # Reasonable limit to prevent memory issues
        if len(self.sessions) > max_sessions:
            # Sort by activity time and remove oldest
            session_age = sorted(
                [(id, s.last_activity) for id, s in self.sessions.items()],
                key=lambda x: x[1]
            )
            # Remove oldest sessions until we're under the limit
            for session_id, _ in session_age[:len(self.sessions) - max_sessions]:
                if session_id in self.sessions:
                    del self.sessions[session_id]
                    # Also clean up peer references
                    if session_id in self.session_peers:
                        peer_id = self.session_peers[session_id]
                        if peer_id in self.session_peers:
                            del self.session_peers[peer_id]
                        del self.session_peers[session_id]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the sniffer's operation."""
        stats = self.stats.copy()
        
        # Add current session counts
        stats["active_sessions"] = sum(1 for s in self.sessions.values() if not s.end_time)
        stats["total_sessions"] = len(self.sessions)
        stats["active_connections"] = len(self.buffers)
        
        # Add pattern statistics
        stats["socket_types"] = dict(stats["socket_types"])
        stats["pattern_types"] = dict(stats["pattern_types"])
        
        # Add throughput statistics
        if stats["current_throughput"] > 0:
            stats["throughput_human"] = f"{format_bytes_count(stats['current_throughput'])}/s"
        else:
            stats["throughput_human"] = "0 B/s"
            
        if stats["peak_throughput"] > 0:
            stats["peak_throughput_human"] = f"{format_bytes_count(stats['peak_throughput'])}/s"
        else:
            stats["peak_throughput_human"] = "0 B/s"
            
        # Calculate uptime
        uptime = datetime.now() - stats["start_time"]
        stats["uptime_seconds"] = uptime.total_seconds()
        stats["uptime_human"] = format_duration(uptime)
        
        # Add recovery ratio
        if stats["parse_errors"] > 0:
            stats["recovery_ratio"] = stats["recovery_attempts"] / stats["parse_errors"]
            stats["dropped_bytes_human"] = format_bytes_count(stats["dropped_bytes"])
        else:
            stats["recovery_ratio"] = 0
            stats["dropped_bytes_human"] = "0 B"
            
        return stats
        
    def display_statistics(self):
        """Display detailed statistics in tabular format."""
        stats = self.get_stats()
        
        # Create a table for display
        table = Table(title="ZeroMQ Sniffer Statistics")
        
        # Add core statistics columns
        table.add_column("Category", style="cyan")
        table.add_column("Stat", style="green")
        table.add_column("Value", style="yellow")
        
        # Core stats
        table.add_row("General", "Uptime", stats["uptime_human"])
        table.add_row("General", "Total Packets", str(stats["total_packets"]))
        table.add_row("General", "Total Frames", str(stats["total_frames"]))
        table.add_row("General", "Valid Frames", str(stats["valid_frames"]))
        table.add_row("General", "Parse Errors", str(stats["parse_errors"]))
        
        # Throughput
        table.add_row("Throughput", "Current", stats["throughput_human"])
        table.add_row("Throughput", "Peak", stats["peak_throughput_human"])
        
        # Error recovery
        if stats["parse_errors"] > 0:
            recovery_pct = (stats["recovery_attempts"] / stats["parse_errors"]) * 100
            table.add_row("Recovery", "Attempts", f"{stats['recovery_attempts']} ({recovery_pct:.1f}%)")
            table.add_row("Recovery", "Dropped Bytes", stats["dropped_bytes_human"])
        
        # Sessions
        table.add_row("Sessions", "Active", str(stats["active_sessions"]))
        table.add_row("Sessions", "Total", str(stats["total_sessions"]))
        table.add_row("Sessions", "Connections", str(stats["active_connections"]))
        
        # Socket types statistics
        if stats["socket_types"]:
            for socket_type, count in sorted(stats["socket_types"].items(), key=lambda x: x[1], reverse=True):
                if count > 0:
                    table.add_row("Socket Types", str(socket_type), str(count))
                    
        # Pattern types statistics
        if stats["pattern_types"]:
            for pattern, count in sorted(stats["pattern_types"].items(), key=lambda x: x[1], reverse=True):
                if count > 0:
                    table.add_row("Patterns", str(pattern), str(count))
                    
        self.console.print(table)
        
        # Print throughput history chart if available
        if self.throughput_history:
            max_val = max(self.throughput_history)
            if max_val > 0:
                # Scale for display
                scale = 50 / max_val  # 50 characters max width
                chart = "Throughput History (bytes/s):\n"
                for val in self.throughput_history:
                    bar_len = max(1, int(val * scale))
                    chart += f"{val:8d} | " + "█" * bar_len + "\n"
                self.console.print(Panel(chart, title="Throughput History")) 