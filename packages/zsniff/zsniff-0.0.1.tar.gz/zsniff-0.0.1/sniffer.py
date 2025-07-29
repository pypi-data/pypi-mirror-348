import argparse
import json
import re
import sys
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Dict, List, NamedTuple, Optional, Set, Tuple

import demjson3
from pydantic import BaseModel, Field, model_validator
from rich.console import Console
from rich.json import JSON as RichJSON
from rich.panel import Panel
from rich.table import Table
from scapy.all import TCP, sniff


# ZeroMQ Socket Types as Enum
class SocketType(str, Enum):
    PUSH = "PUSH"
    PULL = "PULL" 
    PUB = "PUB"
    SUB = "SUB"
    REQ = "REQ"
    REP = "REP"
    DEALER = "DEALER"
    ROUTER = "ROUTER"
    PAIR = "PAIR"
    UNKNOWN = "UNKNOWN"
    
    @classmethod
    def get_description(cls, socket_type: str) -> str:
        descriptions = {
            cls.PUSH: "outgoing message distribution",
            cls.PULL: "incoming message collection",
            cls.PUB: "publisher",
            cls.SUB: "subscriber",
            cls.REQ: "request",
            cls.REP: "reply",
            cls.DEALER: "async request",
            cls.ROUTER: "async reply",
            cls.PAIR: "exclusive pair",
            cls.UNKNOWN: "unknown socket type"
        }
        return f"{socket_type} ({descriptions.get(socket_type, 'unknown type')})"

# ZeroMQ Pattern Types
class PatternType(str, Enum):
    PUBSUB = "PUB-SUB"
    REQREP = "REQ-REP"
    PUSHPULL = "PUSH-PULL"
    PAIRPAIR = "PAIR-PAIR"
    DEALERROUTER = "DEALER-ROUTER"
    UNKNOWN = "UNKNOWN"

# Data class to track a ZeroMQ message correlated by ID
class CorrelatedMessage(NamedTuple):
    request_id: str
    timestamp: datetime
    request_msg: Optional[Dict] = None
    response_msg: Optional[Dict] = None
    
# Data class to track a ZeroMQ Topic
class Topic(NamedTuple):
    name: str
    count: int = 0
    last_seen: datetime = field(default_factory=datetime.now)

# Data class to track a ZeroMQ connection session
@dataclass
class Session:
    session_id: str
    src: str
    src_port: int
    dst: str
    dst_port: int
    start_time: datetime
    end_time: Optional[datetime] = None
    protocol: str = ""
    mechanism: str = ""
    role: str = ""
    socket_type: str = ""
    peer_socket_type: str = ""
    pattern: PatternType = PatternType.UNKNOWN
    messages: List[Dict] = field(default_factory=list)
    last_activity: datetime = field(default_factory=datetime.now)
    total_bytes: int = 0
    topics: Dict[str, Topic] = field(default_factory=dict)
    correlated_msgs: Dict[str, CorrelatedMessage] = field(default_factory=dict)
    summary: Dict[str, Any] = field(default_factory=dict)
    
    def add_message(self, msg: Dict, msg_bytes: int = 0):
        """Add a message to the session with metrics tracking."""
        self.messages.append(msg)
        self.total_bytes += msg_bytes
        self.last_activity = datetime.now()
        
        # Update topics for PUB/SUB pattern detection
        if 'topic' in msg:
            topic_name = msg['topic']
            if topic_name in self.topics:
                topic = self.topics[topic_name]
                self.topics[topic_name] = Topic(
                    name=topic_name, 
                    count=topic.count + 1,
                    last_seen=datetime.now()
                )
            else:
                self.topics[topic_name] = Topic(
                    name=topic_name, 
                    count=1,
                    last_seen=datetime.now()
                )
        
        # Update correlated messages for REQ/REP pattern detection
        if 'request_id' in msg:
            req_id = msg.get('request_id')
            if req_id and req_id != 'null':
                if 'message_type' in msg:
                    msg_type = msg.get('message_type', '').lower()
                    if 'request' in msg_type or 'cmd' in msg_type or 'query' in msg_type:
                        # This is likely a request
                        self.correlated_msgs[req_id] = CorrelatedMessage(
                            request_id=req_id,
                            timestamp=datetime.now(),
                            request_msg=msg
                        )
                    elif 'response' in msg_type or 'reply' in msg_type or 'result' in msg_type:
                        # This is likely a response
                        if req_id in self.correlated_msgs:
                            # Update existing correlation
                            corr = self.correlated_msgs[req_id]
                            self.correlated_msgs[req_id] = CorrelatedMessage(
                                request_id=req_id,
                                timestamp=corr.timestamp,
                                request_msg=corr.request_msg,
                                response_msg=msg
                            )
                        else:
                            # Create new correlation with just response
                            self.correlated_msgs[req_id] = CorrelatedMessage(
                                request_id=req_id,
                                timestamp=datetime.now(),
                                response_msg=msg
                            )
    
    def detect_pattern(self) -> PatternType:
        """Detect the ZeroMQ message pattern based on socket types and message flow."""
        if not self.socket_type:
            return PatternType.UNKNOWN
            
        # Direct socket type pattern matching
        if self.socket_type == SocketType.PUB and self.peer_socket_type == SocketType.SUB:
            return PatternType.PUBSUB
        elif self.socket_type == SocketType.SUB and self.peer_socket_type == SocketType.PUB:
            return PatternType.PUBSUB
        elif self.socket_type == SocketType.PUSH and self.peer_socket_type == SocketType.PULL:
            return PatternType.PUSHPULL
        elif self.socket_type == SocketType.PULL and self.peer_socket_type == SocketType.PUSH:
            return PatternType.PUSHPULL
        elif self.socket_type == SocketType.REQ and self.peer_socket_type == SocketType.REP:
            return PatternType.REQREP
        elif self.socket_type == SocketType.REP and self.peer_socket_type == SocketType.REQ:
            return PatternType.REQREP
        elif self.socket_type == SocketType.PAIR and self.peer_socket_type == SocketType.PAIR:
            return PatternType.PAIRPAIR
        elif self.socket_type == SocketType.DEALER and self.peer_socket_type == SocketType.ROUTER:
            return PatternType.DEALERROUTER
        elif self.socket_type == SocketType.ROUTER and self.peer_socket_type == SocketType.DEALER:
            return PatternType.DEALERROUTER
        
        # Heuristic detection based on message characteristics
        if len(self.topics) > 0:
            return PatternType.PUBSUB
        elif len(self.correlated_msgs) > 0:
            return PatternType.REQREP
            
        # Default to unknown
        return PatternType.UNKNOWN
        
    def update_summary(self):
        """Update the session summary statistics."""
        self.summary = {
            "messages": len(self.messages),
            "total_bytes": self.total_bytes,
            "topics": len(self.topics),
            "req_resp_pairs": sum(1 for v in self.correlated_msgs.values() if v.request_msg and v.response_msg),
            "duration": (self.end_time or datetime.now()) - self.start_time,
            "msgs_per_sec": len(self.messages) / max(1, (self.end_time or datetime.now() - self.start_time).total_seconds()),
            "bytes_per_sec": self.total_bytes / max(1, (self.end_time or datetime.now() - self.start_time).total_seconds()),
            "pattern": self.detect_pattern()
        }
        
        # Store the pattern for later reference
        self.pattern = self.summary["pattern"]
        
        return self.summary

# Pydantic model for a ZeroMQ frame (wire format)
class ZeroMQFrame(BaseModel):
    flags: int
    more: bool
    long: bool
    command: bool
    length: int
    body: bytes
    non_standard: bool = False
    invalid: bool = False

    @model_validator(mode='after')
    def validate_frame(cls, instance):
        # Reserved bits 7-3 must be 0 in standard ZMTP
        if instance.flags >> 3 != 0:
            instance.non_standard = True
        # Command frames cannot have MORE flag in standard ZMTP
        if instance.command and instance.more:
            instance.invalid = True
            instance.non_standard = True
        # The length field must match the body size
        if instance.length != len(instance.body):
            raise ValueError(f"Frame length {instance.length} does not match body size {len(instance.body)}")
        return instance

class ZeroMQSniffer:
    def __init__(
        self,
        interface: str,
        ports: List[int],
        raw_hex: bool,
        debug: bool = False,
        session_timeout: int = 300,  # Session timeout in seconds
        cleanup_interval: int = 60,  # Cleanup interval in seconds
        max_buffer_size: int = 1024 * 1024,  # 1MB max buffer size per connection
        tolerance_level: str = "medium",  # How tolerant of non-standard protocol behavior: low, medium, high
        group_related_messages: bool = True,  # Group related messages (request/response pairs)
    ):
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
        self.current_message: Dict[Tuple[str, int, str, int], List[ZeroMQFrame]] = {}
        self.conn_sessions: Dict[Tuple[str, int, str, int], str] = {}
        self.sessions: Dict[str, Session] = {}
        
        # Track peer relations between sessions
        self.session_peers: Dict[str, str] = {}
        
        # Console for rich output
        self.console = Console()
        
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
        
        # Frame recovery cache to avoid repeating same errors
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
        
        # Topic hierarchy tracking
        self.topics: Dict[str, Dict[str, Any]] = defaultdict(dict)
        
        # Request-response correlation
        self.pending_requests: Dict[str, Dict[str, Any]] = {}
        
        # Performance tracking
        self.throughput_history: List[int] = []
        self.max_history_points = 60  # 1 minute history at 1s intervals

    def start(self):
        port_filters = [f"port {p}" for p in self.ports]
        filter_str = "tcp and (" + " or ".join(port_filters) + ")" if self.ports else "tcp"
        self.console.print(f"[bold green]Starting ZeroMQ sniffer on interface {self.interface}[/bold green] (filter: {filter_str})")
        if self.debug:
            self.console.print("[yellow]Debug mode enabled - detailed protocol debugging information will be shown[/yellow]")
        self.console.print(f"[dim]Session timeout: {self.session_timeout}s, Cleanup interval: {self.cleanup_interval}s[/dim]")
        self.console.print(f"[dim]Protocol tolerance: {self.tolerance_level}, Group related messages: {self.group_related_messages}[/dim]")
        sniff(iface=self.interface, filter=filter_str, store=False, prn=self.process_packet)

    def _try_find_next_frame(self, buf: bytearray) -> int:
        """Try to find the next potential valid frame start after an error.
        Returns the number of bytes to skip, or 1 if no pattern is found."""
        # Look for patterns that might indicate frame starts in ZMTP
        
        # Track recovery attempts
        self.stats["recovery_attempts"] += 1
        
        # Don't scan more than 1024 bytes ahead to avoid performance issues
        # but also make sure we scan enough to find valid frames
        scan_len = min(1024, len(buf))
        
        if self.debug:
            self.console.print(f"[dim]Debug: Scanning {scan_len} bytes for next frame: {bytes(buf[:min(64, scan_len)]).hex()}...[/dim]")
            
        # Skip at least 1 byte
        if scan_len <= 1:
            return 1
            
        # Generate a signature of the first 16 bytes for recovery cache lookup
        if scan_len >= 16:
            signature = bytes(buf[:16])
            if signature in self.recovery_cache:
                offset = self.recovery_cache[signature]
                if self.debug:
                    self.console.print(f"[dim]Debug: Using cached recovery offset {offset} for signature[/dim]")
                return offset
        
        # First, check for common ZeroMQ message patterns
        
        # 1. JSON data pattern - high priority since this is likely application data
        for i in range(1, min(scan_len - 2, 64)):  # Only scan the first 64 bytes for JSON
            # Check for common JSON object starts
            if buf[i:i+2] in [b'{"', b'[{', b'["', b'[]', b'{}']:
                if self.debug:
                    self.console.print(f"[dim]Debug: Found potential JSON start at offset {i}: {bytes(buf[i:i+10]).hex()}[/dim]")
                # Cache this pattern for future recovery
                if scan_len >= 16:
                    self.recovery_cache[signature] = i
                return i
        
        # 2. Check for ZMTP handshake signature (0xFF ... 0x7F) - very distinctive
        for i in range(1, scan_len - 10):
            if buf[i] == 0xFF and i+9 < scan_len and buf[i+9] == 0x7F:
                # Found ZMTP3 greeting signature
                if self.debug:
                    self.console.print(f"[dim]Debug: Found ZMTP3 greeting at offset {i}: {bytes(buf[i:i+16]).hex()}[/dim]")
                # Cache this pattern
                if scan_len >= 16:
                    self.recovery_cache[signature] = i
                return i
        
        # 3. Look for ZMTP3 frame patterns (flag byte with valid pattern)
        for i in range(1, scan_len - 9):
            flags = buf[i]
            # Check if high bits 7-3 are all zero (standard ZMTP3)
            if (flags & 0xF8) == 0:
                long_frame = bool(flags & 0x02)
                # For long frames, verify 8-byte length field makes sense
                if long_frame and i + 9 < scan_len:
                    length = int.from_bytes(buf[i+1:i+9], 'big')
                    # Verify length is within reasonable bounds
                    if 0 <= length < 1_000_000:
                        if self.debug:
                            self.console.print(f"[dim]Debug: Found potential ZMTP3 long frame at offset {i}: {bytes(buf[i:i+16]).hex()}[/dim]")
                        if scan_len >= 16:
                            self.recovery_cache[signature] = i
                        return i
                # For short frames, verify the size byte
                elif not long_frame and i + 2 < scan_len:
                    length = buf[i+1]
                    # Short frames with reasonable length
                    if length < 256:
                        # Now verify there's enough data or this is likely a real frame
                        if i + 2 + length <= scan_len or length < 64:
                            # For small frames, also check if the content looks like valid data
                            if length < 64 and i + 2 + length <= scan_len:
                                content = buf[i+2:i+2+length]
                                # If it contains control chars, it's less likely to be a valid frame
                                control_chars = sum(1 for b in content if b < 32 and b not in (9, 10, 13))
                                if control_chars > length / 3:
                                    # Too many control chars, probably not valid data
                                    continue
                            if self.debug:
                                self.console.print(f"[dim]Debug: Found potential ZMTP3 short frame at offset {i}: {bytes(buf[i:i+min(16, 2+length)]).hex()}[/dim]")
                            if scan_len >= 16:
                                self.recovery_cache[signature] = i
                            return i
        
        # 4. Look for ZMTP2 frame patterns
        for i in range(1, scan_len - 9):
            # Check for extended frame marker (0xFF)
            if buf[i] == 0xFF and i + 9 < scan_len:
                length = int.from_bytes(buf[i+1:i+9], 'big')
                # Verify length is within reasonable bounds
                if 0 < length < 1_000_000:
                    if self.debug:
                        self.console.print(f"[dim]Debug: Found potential ZMTP2 extended frame at offset {i}: {bytes(buf[i:i+16]).hex()}[/dim]")
                    if scan_len >= 16:
                        self.recovery_cache[signature] = i
                    return i
            # Check for short frame pattern (length byte followed by flags and content)
            elif 1 <= buf[i] < 255:
                frame_len = buf[i]
                # Make sure there's enough data to have a complete short frame
                if i + 1 + frame_len <= scan_len:
                    # The byte after length should be a reasonable flags value
                    flags = buf[i+1]
                    if flags < 32:  # Flags should be small values
                        if self.debug:
                            self.console.print(f"[dim]Debug: Found potential ZMTP2 short frame at offset {i}: {bytes(buf[i:i+min(16, 2+frame_len)]).hex()}[/dim]")
                        if scan_len >= 16:
                            self.recovery_cache[signature] = i
                        return i
        
        # 5. Look for null delimiter frames (common in ZeroMQ patterns)
        for i in range(1, scan_len - 2):
            # Check for a pattern like a flag byte followed by a zero length
            if (buf[i] & 0xF8) == 0 and buf[i+1] == 0:
                if self.debug:
                    self.console.print(f"[dim]Debug: Found potential null delimiter frame at offset {i}: {bytes(buf[i:i+4]).hex()}[/dim]")
                if scan_len >= 16:
                    self.recovery_cache[signature] = i
                return i
                
        # 6. Fallback: look for strings or printable text that could be message content
        for i in range(1, min(scan_len - 8, 128)):  # Only scan first 128 bytes for this
            # Check for a sequence of printable ASCII characters (likely part of a message)
            if all(32 <= b <= 126 for b in buf[i:i+8]):
                if self.debug:
                    self.console.print(f"[dim]Debug: Found ASCII text at offset {i}: {bytes(buf[i:i+16]).hex()}[/dim]")
                if scan_len >= 16:
                    self.recovery_cache[signature] = i
                return i
                
        # 7. If still not found, skip to next non-zero byte
        # This helps when we have padding or garbage bytes
        for i in range(1, min(scan_len, 64)):  # Limit this search to avoid getting stuck
            if buf[i] != 0:
                if self.debug:
                    self.console.print(f"[dim]Debug: Skipping to first non-zero byte at offset {i}[/dim]")
                return i
                
        # 8. Last resort - just skip one byte and try again
        if self.debug:
            self.console.print("[dim]Debug: No recovery pattern found, skipping one byte[/dim]")
        return 1
    
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
            stats["throughput_human"] = f"{self._format_bytes_count(stats['current_throughput'])}/s"
        else:
            stats["throughput_human"] = "0 B/s"
            
        if stats["peak_throughput"] > 0:
            stats["peak_throughput_human"] = f"{self._format_bytes_count(stats['peak_throughput'])}/s"
        else:
            stats["peak_throughput_human"] = "0 B/s"
            
        # Calculate uptime
        uptime = datetime.now() - stats["start_time"]
        stats["uptime_seconds"] = uptime.total_seconds()
        stats["uptime_human"] = self._format_duration(uptime)
        
        # Add recovery ratio
        if stats["parse_errors"] > 0:
            stats["recovery_ratio"] = stats["recovery_attempts"] / stats["parse_errors"]
            stats["dropped_bytes_human"] = self._format_bytes_count(stats["dropped_bytes"])
        else:
            stats["recovery_ratio"] = 0
            stats["dropped_bytes_human"] = "0 B"
            
        return stats
        
    def _format_bytes_count(self, bytes_count: int) -> str:
        """Format byte count to human-readable string with appropriate units."""
        if bytes_count < 1024:
            return f"{bytes_count} B"
        elif bytes_count < 1024 * 1024:
            return f"{bytes_count / 1024:.1f} KB"
        elif bytes_count < 1024 * 1024 * 1024:
            return f"{bytes_count / (1024 * 1024):.1f} MB"
        else:
            return f"{bytes_count / (1024 * 1024 * 1024):.1f} GB"
            
    def _format_duration(self, duration: timedelta) -> str:
        """Format a timedelta to a human-readable string."""
        total_seconds = int(duration.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0 or days > 0:
            parts.append(f"{hours}h")
        if minutes > 0 or hours > 0 or days > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        
        return " ".join(parts)
    
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

    def process_packet(self, pkt):
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
                    major, minor = self._normalize_zmtp_version(major, minor)
                    
                    # Extract and validate security mechanism
                    mech_bytes = bytes(buf[12:32])
                    mech = self._detect_zmtp_mechanism(mech_bytes)
                    
                    # Extract and validate role
                    as_server = buf[32]
                    role = self._detect_zmtp_role(as_server)
                    
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
                        frame, consumed = self._parse_one_frame_old(buf)
                    except Exception as e:
                        self.console.print(f"[bold red]Error:[/bold red] Failed to parse ZMTP 1.0/2.0 handshake: {e}")
                        # Try to find a valid frame start if we failed
                        skip_bytes = self._try_find_next_frame(buf)
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
                        ident = self._format_bytes(frame.body)
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
                parse_func = self._parse_one_frame_new
            elif self.protocol.get(conn_key) == "zmtp2":
                parse_func = self._parse_one_frame_old
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
                    frame, consumed = self._parse_one_frame_new(buf)
                except Exception:
                    try:
                        frame, consumed = self._parse_one_frame_old(buf)
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
                    skip_bytes = self._try_find_next_frame(buf)
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
        
    def _parse_one_frame_new(self, buf: bytearray):
        """Parse one ZMTP/3.x frame from the buffer (returns frame and bytes consumed)."""
        if len(buf) < 2:
            return None, 0  # not enough for flags+size
            
        flags = buf[0]
        flags_info = self._analyze_flags(flags)
        
        # Log non-standard flag bits at debug level if appropriate
        if self.debug and not flags_info["standard"] and self._should_warn_for_flags(flags_info):
            self.console.print(f"[yellow]Warning:[/yellow] Non-standard flag bits: {bin(flags)} ({flags_info['description']})")
        
        # Check if flags are too non-standard to continue
        if not flags_info["valid"] and self.tolerance_level == "low":
            raise ValueError(f"Invalid flag combination: {bin(flags)} ({flags_info['description']})")
            
        long_frame = bool(flags & 0x02)
        if long_frame:
            if len(buf) < 9:
                return None, 0  # need 8-byte length
            size = int.from_bytes(buf[1:9], 'big')
            
            # Sanity check the size - implement intelligent size validation
            if size > self.max_buffer_size:
                # Before completely rejecting, check if this might be valid data
                if self._looks_like_valid_data(buf[1:min(17, len(buf))]):
                    # For high tolerance, try to continue with a truncated frame
                    if self.tolerance_level == "high":
                        self.console.print(f"[yellow]Warning:[/yellow] Frame size {size} exceeds maximum, truncating to {self.max_buffer_size}")
                        size = self.max_buffer_size
                    else:
                        raise ValueError(f"Frame size {size} exceeds maximum allowed size {self.max_buffer_size}")
                else:
                    raise ValueError(f"Frame size {size} exceeds maximum allowed size {self.max_buffer_size}")
                
            header_len = 9
        else:
            size = buf[1]
            header_len = 2
            
        # Check if we have the complete frame
        if len(buf) < header_len + size:
            return None, 0  # wait for full frame
            
        body_bytes = bytes(buf[header_len : header_len + size])
        more_flag = bool(flags & 0x01)
        cmd_flag = bool(flags & 0x04)
        
        # Create and validate the frame
        frame = ZeroMQFrame(flags=flags, more=more_flag, long=long_frame, command=cmd_flag, 
                            length=size, body=body_bytes)
        
        # Set non-standard flag for abnormal flags
        if not flags_info["standard"]:
            frame.non_standard = True
            
        # Set invalid flag for invalid flag combinations
        if not flags_info["valid"]:
            frame.invalid = True
        
        # Track statistics
        self.stats["total_frames"] += 1
        if flags_info["standard"]:
            self.stats["valid_frames"] += 1
        
        return frame, header_len + size
        
    def _parse_one_frame_old(self, buf: bytearray):
        """Parse one ZMTP/1.0 or 2.x frame (length-included format)."""
        if len(buf) < 1:
            return None, 0
            
        first = buf[0]
        if first < 0xFF:
            # Short frame (1-byte length includes flags)
            if first == 0:
                # Some implementations might send a zero-length frame indicator
                # Instead of failing, treat it as a special case with empty body
                if self.debug:
                    self.console.print("[yellow]Warning:[/yellow] Zero-length frame in ZMTP/1.0 stream - handling as empty frame")
                # Construct a minimal valid frame and consume the byte
                frame = ZeroMQFrame(flags=0, more=False, long=False, command=False, length=0, body=b'')
                
                # Track statistics
                self.stats["total_frames"] += 1
                self.stats["valid_frames"] += 1
                
                return frame, 1
                
            total = first  # length of flags+body
            if len(buf) < 1 + total:
                return None, 0
                
            # Sanity check the size with improved validation
            if total > self.max_buffer_size:
                # Check if this looks like a valid frame despite the large size
                if self._looks_like_valid_data(buf[1:min(total+1, len(buf))]):
                    if self.tolerance_level == "high":
                        self.console.print(f"[yellow]Warning:[/yellow] Frame size {total} exceeds maximum, truncating to {self.max_buffer_size}")
                        total = self.max_buffer_size
                    else:
                        raise ValueError(f"Frame size {total} exceeds maximum allowed size {self.max_buffer_size}")
                else:
                    raise ValueError(f"Frame size {total} exceeds maximum allowed size {self.max_buffer_size}")
                
            flags = buf[1] if total >= 1 else 0
            flags_info = self._analyze_flags(flags)
            
            # Log non-standard flag bits if appropriate
            if self.debug and not flags_info["standard"] and self._should_warn_for_flags(flags_info):
                self.console.print(f"[yellow]Warning:[/yellow] Non-standard flag bits: {bin(flags)} ({flags_info['description']})")
                
            body_len = total - 1
            body_bytes = bytes(buf[2 : 2 + body_len]) if body_len > 0 else b''
            more_flag = bool(flags & 0x01)
            cmd_flag = bool(flags & 0x04)
            long_flag = False
            
            frame = ZeroMQFrame(flags=flags, more=more_flag, long=long_flag, command=cmd_flag, 
                                length=body_len, body=body_bytes)
            
            # Set non-standard flag for abnormal flags
            if not flags_info["standard"]:
                frame.non_standard = True
                
            # Set invalid flag for invalid flag combinations
            if not flags_info["valid"]:
                frame.invalid = True
            
            # Track statistics
            self.stats["total_frames"] += 1
            if flags_info["standard"]:
                self.stats["valid_frames"] += 1
            
            return frame, 1 + total
        else:
            # Long frame (0xFF marker followed by 8-byte length)
            if len(buf) < 9:
                return None, 0
                
            ext_size = int.from_bytes(buf[1:9], 'big')
            
            # Enhanced size validation
            if ext_size > self.max_buffer_size:
                # Check if this looks like valid data despite size
                if self._looks_like_valid_data(buf[9:min(9+ext_size, len(buf))]):
                    if self.tolerance_level == "high":
                        self.console.print(f"[yellow]Warning:[/yellow] Extended frame size {ext_size} exceeds maximum, truncating to {self.max_buffer_size}")
                        ext_size = self.max_buffer_size
                    else:
                        raise ValueError(f"Frame size {ext_size} exceeds maximum allowed size {self.max_buffer_size}")
                else:
                    raise ValueError(f"Frame size {ext_size} exceeds maximum allowed size {self.max_buffer_size}")
                
            if ext_size == 0:
                # Handle zero-length extended frames too
                if self.debug:
                    self.console.print("[yellow]Warning:[/yellow] Zero-length extended frame in ZMTP/1.0 stream - handling as empty frame")
                frame = ZeroMQFrame(flags=0, more=False, long=True, command=False, length=0, body=b'')
                
                # Track statistics
                self.stats["total_frames"] += 1
                self.stats["valid_frames"] += 1
                
                return frame, 9
                
            if len(buf) < 1 + 8 + ext_size:
                return None, 0
                
            flags = buf[9]
            flags_info = self._analyze_flags(flags)
            
            # Log non-standard flag bits if appropriate
            if self.debug and not flags_info["standard"] and self._should_warn_for_flags(flags_info):
                self.console.print(f"[yellow]Warning:[/yellow] Non-standard flag bits: {bin(flags)} ({flags_info['description']})")
            
            body_len = ext_size - 1
            body_bytes = bytes(buf[10 : 10 + body_len]) if body_len > 0 else b''
            more_flag = bool(flags & 0x01)
            cmd_flag = bool(flags & 0x04)
            long_flag = True
            
            frame = ZeroMQFrame(flags=flags, more=more_flag, long=long_flag, command=cmd_flag, 
                                length=body_len, body=body_bytes)
            
            # Set non-standard flag for abnormal flags
            if not flags_info["standard"]:
                frame.non_standard = True
                
            # Set invalid flag for invalid flag combinations
            if not flags_info["valid"]:
                frame.invalid = True
            
            # Track statistics
            self.stats["total_frames"] += 1
            if flags_info["standard"]:
                self.stats["valid_frames"] += 1
            
            return frame, 1 + 8 + ext_size
            
    def _looks_like_valid_data(self, data: bytes) -> bool:
        """Heuristic check if data looks valid despite size validation failures."""
        if not data or len(data) < 4:
            return False
            
        # Check if it looks like printable text
        printable_ratio = sum(32 <= b <= 126 for b in data) / len(data)
        if printable_ratio > 0.7:  # If more than 70% is printable ASCII, likely valid
            return True
            
        # Check for JSON-like patterns
        if data.startswith(b'{') or data.startswith(b'[') or b':"' in data or b'":' in data:
            return True
            
        # Check for ZMTP command patterns
        if b'\0' in data and sum(32 <= b <= 126 for b in data[:data.find(b'\0')]) > 0.8 * data.find(b'\0'):
            return True
            
        # Check for binary but structured data (not just random bytes)
        # This is a rough heuristic for binary protocols - more zeros than you'd expect randomly
        zero_ratio = sum(1 for b in data if b == 0) / len(data)
        if zero_ratio > 0.1:  # More than 10% zeros, could be structured
            return True
            
        return False

    def _format_bytes(self, data: bytes) -> str:
        """Format bytes as ASCII if printable, else hex (with truncation for long data)."""
        if not data:
            return '""'
            
        # Check if it might be partial JSON data
        json_start = False
        if data.startswith(b'{') or data.startswith(b'\"') or b',"' in data[:20]:
            json_start = True
            
        # Try to decode as UTF-8 text
        try:
            text = data.decode('utf-8', errors='replace')
        except Exception:
            text = None
            
        # Check if it's a reasonable text string
        if text is not None and (all(ch.isprintable() or ch in '\n\r\t' for ch in text) or json_start):
            # Escape newlines/carriage returns
            text = text.replace("\r", "\\r").replace("\n", "\\n")
            if len(text) > 64:
                # Show a bit more context for potential JSON data
                if json_start:
                    # Try to find a sensible cutoff point for JSON
                    cutoff = min(200, len(text))
                    truncated = text[:cutoff]
                    if '"' in truncated[-10:] and ',' not in truncated[-10:]:
                        # Try to cut at a reasonable point (after a quoted string)
                        last_quote = truncated.rfind('"') + 1
                        if last_quote > len(truncated) - 10:
                            truncated = truncated[:last_quote]
                        
                    return f"\"{truncated}...\" (truncated, {len(text)} chars)"
                return f"\"{text[:64]}...\" (truncated, {len(text)} chars)"
            return f"\"{text}\""
            
        # Otherwise, return hex string
        hex_str = data.hex()
        if len(hex_str) > 128:
            return hex_str[:128] + "..." + f" (truncated, {len(data)} bytes)"
        return hex_str

    def _fix_json(self, data_str: str) -> str:
        """
        Comprehensive JSON fixer to handle various malformed or partial JSON.
        Returns a best-effort fixed JSON string.
        """
        if not data_str:
            return "{}"
            
        # 1. Handle simple non-JSON cases quickly
        if not any(c in data_str for c in '{["'):
            if data_str.lower() in ('true', 'false', 'null'):
                return data_str
            try:
                # Check if it's a number
                float(data_str)
                return data_str
            except ValueError:
                # If not JSON-like at all, wrap as string
                return f'"{data_str}"'
                
        # 2. Clean up whitespace and control characters
        data_str = re.sub(r'[\x00-\x1F\x7F]', ' ', data_str)
        
        # 3. Fix common missing brace/quote patterns
        # Check for missing opening brace pattern: service_id":"value" (missing opening { and first ")
        if '"' in data_str and ':' in data_str and not data_str.startswith('{'):
            # If it starts with a key-like pattern, wrap it in braces
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*[\":]', data_str):
                # Add opening brace and quote if needed
                if not data_str.startswith('"'):
                    data_str = '{"' + data_str
                else:
                    data_str = '{' + data_str
            # If it looks like we're missing an opening brace but not inside an array
            elif '"' in data_str[:20] and ':' in data_str[:30] and '[' not in data_str[:10]:
                data_str = '{' + data_str
                
        # 4. Fix unquoted field names (before json5 lib)
        # Handle unquoted field names at beginning of object or after comma
        field_pattern = re.compile(r'(\{|\,)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:')
        data_str = field_pattern.sub(r'\1"\2":', data_str)
        
        # 5. Fix unclosed/unbalanced brackets
        open_curly = data_str.count('{')
        close_curly = data_str.count('}')
        if open_curly > close_curly:
            data_str += '}' * (open_curly - close_curly)
        elif close_curly > open_curly:
            # Too many closing braces - add matching opening braces at beginning
            # But make sure we're not trying to fix an array element
            if not data_str.startswith('['):
                data_str = '{' * (close_curly - open_curly) + data_str
            
        open_square = data_str.count('[')
        close_square = data_str.count(']')
        if open_square > close_square:
            data_str += ']' * (open_square - close_square)
        elif close_square > open_square:
            # Too many closing brackets - add matching opening brackets at beginning
            data_str = '[' * (close_square - open_square) + data_str
            
        # 6. Fix trailing commas which are invalid in standard JSON
        data_str = re.sub(r',\s*(\}|\])', r'\1', data_str)
        
        # 7. Fix missing commas between array elements or objects that look like JSON
        data_str = re.sub(r'(\}|\]|\")(\s*)(\{|\[|\")', r'\1,\3', data_str)
        
        # 8. Attempt to parse with a more tolerant approach first
        try:
            # Try to use demjson3 which is more tolerant of malformed JSON
            parsed = demjson3.decode(data_str, strict=False)
            # Successfully parsed, return standard JSON format
            return json.dumps(parsed, separators=(',', ':'))
        except Exception as e:
            if self.debug:
                self.console.print(f"[dim]Debug: Failed to parse with demjson3: {e}, trying json5[/dim]")

            # Try another approach with json5 if available
            try:
                # Only import json5 when needed (requires separate pip install)
                import json5
                parsed = json5.loads(data_str)
                return json.dumps(parsed, separators=(',', ':'))
            except Exception:
                # If we can't parse it with json5 either, return the fixed string 
                # for standard libraries to try
                return data_str

    def _try_parse_json(self, data_str: str) -> str:
        """Attempt to parse and format JSON data for better display."""
        # If it doesn't look like JSON, return as is
        if not data_str or len(data_str) < 2:
            return data_str
            
        # Quick check if it might be JSON
        might_be_json = False
        if data_str.startswith('{') and (data_str.endswith('}') or '"}' in data_str):
            might_be_json = True
        elif data_str.startswith('[') and (data_str.endswith(']') or '"]' in data_str):
            might_be_json = True
        elif '":"' in data_str or '":' in data_str or ',"' in data_str:
            might_be_json = True
            
        if not might_be_json:
            return data_str
        
        # Apply the robust JSON fixer to handle various edge cases
        fixed_data_str = self._fix_json(data_str)
        
        try:
            # Try parsing with the standard json library first
            try:
                parsed = json.loads(fixed_data_str)
            except json.JSONDecodeError:
                # Fall back to demjson3 which is more tolerant
                parsed = demjson3.decode(fixed_data_str, strict=False)
            
            # Check for common ZeroMQ message patterns
            if isinstance(parsed, dict):
                # Extract key fields for summary
                message_type = None
                service_id = parsed.get('service_id')
                timestamp = parsed.get('timestamp')
                request_id = parsed.get('request_id')
                
                # Look for message type in common locations
                if 'message_type' in parsed:
                    message_type = parsed['message_type']
                elif 'type' in parsed:
                    message_type = parsed['type']
                elif 'payload' in parsed and isinstance(parsed['payload'], dict):
                    message_type = parsed['payload'].get('message_type') or parsed['payload'].get('type')
                elif 'method' in parsed:
                    message_type = parsed['method']
                elif 'cmd' in parsed:
                    message_type = parsed['cmd']
                
                # Format a compact representation for display
                parts = []
                if message_type:
                    parts.append(f"[bold magenta]{message_type}[/bold magenta]")
                if service_id:
                    # Show first 8 chars of service_id (usually UUID) for brevity
                    if isinstance(service_id, str) and len(service_id) > 12:
                        parts.append(f"service: [blue]{service_id[:8]}...[/blue]")
                    else:
                        parts.append(f"service: [blue]{service_id}[/blue]")
                        
                if request_id:
                    if request_id == 'null' or request_id is None:
                        parts.append("no request_id")
                    else:
                        # Truncate long request IDs
                        if isinstance(request_id, str) and len(request_id) > 8:
                            parts.append(f"req: {request_id[:8]}...")
                        else:
                            parts.append(f"req: {request_id}")
                            
                if timestamp:
                    # Convert timestamp to readable format if it looks like a unix timestamp
                    if isinstance(timestamp, (int, float)):
                        if timestamp > 1000000000000:
                            # This is likely a microsecond or nanosecond timestamp
                            try:
                                ts_seconds = timestamp / 1000000000 if timestamp > 1000000000000000 else timestamp / 1000
                                dt = datetime.fromtimestamp(ts_seconds)
                                parts.append(f"time: {dt.strftime('%H:%M:%S.%f')[:-3]}")
                            except Exception:
                                parts.append(f"ts: {timestamp}")
                        else:
                            parts.append(f"ts: {timestamp}")
                    else:
                        parts.append(f"ts: {timestamp}")
                
                # Add payload summary if available and interesting
                if 'payload' in parsed and isinstance(parsed['payload'], dict):
                    payload = parsed['payload']
                    # Extract additional payload fields that might be interesting
                    interesting_fields = ['status', 'action', 'command', 'error', 'state', 'result', 'topic']
                    for key in interesting_fields:
                        if key in payload and payload[key] not in [None, '']:
                            # Truncate long values
                            val = payload[key]
                            if isinstance(val, str) and len(val) > 15:
                                val = val[:15] + "..."
                            parts.append(f"{key}: {val}")
                
                if parts:
                    # Return the summary
                    return " | ".join(parts)
            
            # For arrays, show length and first few items
            if isinstance(parsed, list):
                if len(parsed) == 0:
                    return "[] (empty array)"
                elif len(parsed) <= 3:
                    # For small arrays, show all items
                    items = []
                    for item in parsed:
                        if isinstance(item, dict):
                            items.append("{...}")
                        elif isinstance(item, list):
                            items.append(f"[...] ({len(item)} items)")
                        else:
                            items.append(str(item))
                    return f"[{', '.join(items)}]"
                else:
                    # For larger arrays, show length and first item
                    first = parsed[0]
                    if isinstance(first, dict):
                        return f"[{...}, ...] ({len(parsed)} items)"
                    elif isinstance(first, list):
                        return f"[[...], ...] ({len(parsed)} items)"
                    else:
                        return f"[{first}, ...] ({len(parsed)} items)"
            
            # If no special handling worked, just display the JSON in a compact format
            formatted = json.dumps(parsed, separators=(',', ':'))
            
            # For extremely long JSON, truncate
            if len(formatted) > 100:
                return f"{formatted[:97]}..." 
            
            return formatted
        except Exception as e:
            # Not valid JSON or other issue, return as is or with error info
            if self.debug:
                # Show detailed error message in debug mode
                if '{' in data_str and '}' not in data_str:
                    return f"{data_str}... [dim](truncated JSON)[/dim]"
                
                # Show parsing error details
                return f"{data_str} [dim](JSON parse error: {e})[/dim]"
                
            return data_str

    def _output_message(self, conn_key, frames: List[ZeroMQFrame]):
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
        
        # Check for non-standard frames but avoid excessive warnings
        non_standard_frames = [i for i, fr in enumerate(frames) if fr.non_standard]
        if non_standard_frames and len(non_standard_frames) <= 3:  # Limit warnings for clarity
            frame_nums = ", ".join(map(str, non_standard_frames))
            # Use a complete flags_info dictionary with all required keys
            if self._should_warn_for_flags({"standard": False, "extensions": [], "valid": True}):
                self.console.print(f"{prefix} [yellow]Warning:[/yellow] Message contains non-standard flag bits in frame(s) {frame_nums}")
            
        # Check for invalid frames (like command frames with MORE bit)
        invalid_frames = [i for i, fr in enumerate(frames) if fr.invalid]
        if invalid_frames:
            frame_nums = ", ".join(map(str, invalid_frames))
            self.console.print(f"{prefix} [yellow]Warning:[/yellow] Message contains invalid frame(s) {frame_nums} but processing anyway")
        
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
                self._process_command_frame(prefix, frame, session, total_msg_size)
                return
                
            # Handle single-frame message with data
            body_str = self._format_bytes(frame.body)
            
            # Try to detect if this is a topic-based message for PUB/SUB pattern
            topic = self._try_extract_topic(frame.body)
            if topic:
                json_part = body_str.split('"', 2)[-1] if '"' in body_str else body_str
                content_str = f"[green]Topic: [bold]{topic}[/bold] | Content: {json_part}[/green]"
                
                # Track the topic for pattern detection
                if topic not in session.topics:
                    session.topics[topic] = Topic(name=topic, count=1, last_seen=datetime.now())
                else:
                    old_topic = session.topics[topic]
                    session.topics[topic] = Topic(
                        name=topic, 
                        count=old_topic.count + 1, 
                        last_seen=datetime.now()
                    )
                
                # Update socket type based on topic presence (likely PUB or SUB)
                if not session.socket_type:
                    session.socket_type = "PUB" if src.split(':')[0] != dst.split(':')[0] else "SUB"
                    self.stats["socket_types"][session.socket_type] += 1
                
                # Process the message data
                try:
                    # Try to parse any JSON in the message after the topic
                    body_parts = frame.body.split(b'\0', 1)
                    if len(body_parts) > 1:
                        try:
                            data_str = body_parts[1].decode('utf-8', errors='ignore')
                            data_processed = self._try_parse_json(data_str)
                            self.console.print(f"{prefix} {content_str}")
                            
                            # Show the prettified JSON if it could be parsed
                            try:
                                parsed = json.loads(self._fix_json(data_str))
                                self.console.print(RichJSON(json.dumps(parsed, indent=2)))
                            except Exception:
                                # Not JSON, that's fine
                                pass
                                
                            # Record message in session with topic
                            message_data = {
                                'timestamp': datetime.now(),
                                'topic': topic,
                                'content': data_processed,
                                'size': total_msg_size,
                                'frames': [{'flags': frame.flags, 'body': frame.body.hex(), 'command': False}]
                            }
                            session.add_message(message_data, total_msg_size)
                        except Exception:
                            # If parsing fails, just show the raw format
                            self.console.print(f"{prefix} {content_str}")
                            
                            # Record message in session with topic
                            message_data = {
                                'timestamp': datetime.now(),
                                'topic': topic,
                                'size': total_msg_size,
                                'frames': [{'flags': frame.flags, 'body': frame.body.hex(), 'command': False}]
                            }
                            session.add_message(message_data, total_msg_size)
                    else:
                        # Just a topic without data
                        self.console.print(f"{prefix} {content_str}")
                        
                        # Record message in session with topic only
                        message_data = {
                            'timestamp': datetime.now(),
                            'topic': topic,
                            'size': total_msg_size,
                            'frames': [{'flags': frame.flags, 'body': frame.body.hex(), 'command': False}]
                        }
                        session.add_message(message_data, total_msg_size)
                except Exception as e:
                    # Fallback for any errors
                    self.console.print(f"{prefix} {content_str}")
                    if self.debug:
                        self.console.print(f"[dim]Debug: Failed to process topic message: {e}[/dim]")
                        
                    # Record message in session
                    message_data = {
                        'timestamp': datetime.now(),
                        'topic': topic,
                        'size': total_msg_size,
                        'error': str(e),
                        'frames': [{'flags': frame.flags, 'body': frame.body.hex(), 'command': False}]
                    }
                    session.add_message(message_data, total_msg_size)
                return
            
            # Check if this looks like JSON and try to parse
            try:
                # Attempt to decode as UTF-8 text
                text = frame.body.decode('utf-8', errors='ignore')
                # Try to parse as JSON or format nicely
                if (text.startswith('{') and text.endswith('}')) or (text.startswith('[') and text.endswith(']')):
                    # This might be JSON
                    json_data = self._try_parse_json(text)
                    self.console.print(f"{prefix} [green]Content: {json_data}[/green]")
                    
                    # Try to display the JSON prettily
                    try:
                        parsed = json.loads(self._fix_json(text))
                        self.console.print(RichJSON(json.dumps(parsed, indent=2)))
                        
                        # Check for request/response pattern
                        if isinstance(parsed, dict) and 'request_id' in parsed:
                            self._track_request_response(session, parsed)
                    except Exception:
                        # Not valid JSON, that's okay
                        pass
                        
                    # Record message in session
                    message_data = {
                        'timestamp': datetime.now(),
                        'content': json_data,
                        'size': total_msg_size,
                        'frames': [{'flags': frame.flags, 'body': frame.body.hex(), 'command': False}]
                    }
                    session.add_message(message_data, total_msg_size)
                else:
                    # Regular text content
                    self.console.print(f"{prefix} [green]Content: {body_str}[/green]")
                    
                    # Record message in session
                    message_data = {
                        'timestamp': datetime.now(),
                        'content': body_str,
                        'size': total_msg_size,
                        'frames': [{'flags': frame.flags, 'body': frame.body.hex(), 'command': False}]
                    }
                    session.add_message(message_data, total_msg_size)
            except Exception:
                # Binary data or other non-text
                self.console.print(f"{prefix} [green]Content: {body_str}[/green]")
                
                # Record message in session
                message_data = {
                    'timestamp': datetime.now(),
                    'content': body_str,
                    'size': total_msg_size,
                    'frames': [{'flags': frame.flags, 'body': frame.body.hex(), 'command': False}]
                }
                session.add_message(message_data, total_msg_size)
            
            # Print raw hex if enabled
            if self.raw_hex:
                # Reconstruct raw frame bytes (including header)
                proto = self.protocol.get(conn_key, "zmtp3")
                raw_frame = self._reconstruct_raw_frame(frame, proto)
                self.console.print(f"{prefix} [dim]Raw:[/dim] {raw_frame.hex()}")
                
            return
        
        # Multi-frame message - handle envelope pattern (common in ZeroMQ)
        self._process_multiframe_message(prefix, frames, session, conn_key, total_msg_size)
        
    def _process_command_frame(self, prefix: str, frame: ZeroMQFrame, session: Session, msg_size: int):
        """Process a command frame (like READY, SUBSCRIBE, etc.)"""
        # Separate command name and data (command frames: "NAME\0DATA" format)
        if b'\x00' in frame.body:
            name_bytes, data_bytes = frame.body.split(b'\x00', 1)
        else:
            name_bytes, data_bytes = frame.body, b''
            
        # Try to decode the command name
        try:
            cmd_name = name_bytes.decode('ascii', errors='ignore').strip()
            # If it looks like JSON or other non-command data, use a generic name
            if cmd_name.startswith('{') or not cmd_name or len(cmd_name) > 20:
                cmd_name = "Data"
        except Exception:
            cmd_name = name_bytes.hex() if name_bytes else "Unknown"
            
        data_info = self._format_bytes(data_bytes) if data_bytes else ""
        
        # Handle READY command specially to extract socket type
        if cmd_name == "READY":
            socket_type, data_info = self._extract_socket_type(data_bytes, data_info, session)
            
            # Update the socket type counts for statistics
            self.stats["socket_types"][socket_type] += 1
        
        # Print command (yellow name, magenta content if any)
        self.console.print(f"{prefix} [bold yellow]Command[/bold yellow] [magenta]{cmd_name}[/magenta] {data_info}")
        if self.raw_hex:
            # Get the protocol type
            proto = self.protocol.get((session.src, session.src_port, session.dst, session.dst_port), "zmtp3")
            
            # Reconstruct raw frame bytes (including header)
            raw_frame = self._reconstruct_raw_frame(frame, proto)
            self.console.print(f"{prefix} [dim]Raw:[/dim] {raw_frame.hex()}")
            
        # After command processing, try to pretty-print any JSON in the command data
        try:
            if data_bytes:
                text = data_bytes.decode('utf-8', errors='replace')
                fixed_text = self._fix_json(text)
                parsed = demjson3.decode(fixed_text, strict=False)
                self.console.print(RichJSON(json.dumps(parsed, indent=2)))
        except Exception:
            pass
            
        # Record message in session
        message_data = {
            'timestamp': datetime.now(),
            'command': cmd_name,
            'data': data_info,
            'size': msg_size,
            'frames': [
                {'flags': frame.flags, 'body': frame.body.hex(), 'command': True}
            ]
        }
        session.add_message(message_data, msg_size)
            
    def _extract_socket_type(self, data_bytes: bytes, data_info: str, session: Session) -> Tuple[str, str]:
        """Extract the socket type from a READY command and update the session."""
        socket_type = "UNKNOWN"
        
        if b"Socket-Type" in data_bytes:
            try:
                socket_type_hex = data_bytes.split(b"Socket-Type")[1].strip()
                # Decode the socket type (hex to ASCII)
                if socket_type_hex.startswith(b"\x00\x00\x00"):
                    # Skip the size prefix (4 bytes)
                    socket_type_ascii = socket_type_hex[4:].decode('ascii', errors='ignore').strip()
                    
                    # Try to convert to enum value
                    try:
                        socket_type = SocketType(socket_type_ascii)
                    except ValueError:
                        # Not a standard type
                        socket_type = socket_type_ascii
                        
                    description = SocketType.get_description(socket_type)
                    data_info = f"Socket-Type: [bold cyan]{description}[/bold cyan]"
                    
                    # Update session socket type
                    session.socket_type = socket_type
                    
                    # Try to find and update the peer session socket type for pattern detection
                    peer_conn = (session.dst, session.dst_port, session.src, session.src_port)
                    peer_session_id = self.conn_sessions.get(peer_conn)
                    if peer_session_id and peer_session_id in self.sessions:
                        peer_session = self.sessions[peer_session_id]
                        peer_session.peer_socket_type = socket_type
                        session.peer_socket_type = peer_session.socket_type
                        
                        # Record peer relationship
                        self.session_peers[session.session_id] = peer_session_id
                        self.session_peers[peer_session_id] = session.session_id
                        
                        # Update pattern types for both sessions
                        pattern = session.detect_pattern()
                        if pattern != PatternType.UNKNOWN:
                            session.pattern = pattern
                            peer_session.pattern = pattern
                            self.stats["pattern_types"][pattern] += 1
            except Exception:
                pass
                
        return socket_type, data_info
        
    def _process_multiframe_message(self, prefix: str, frames: List[ZeroMQFrame], session: Session, 
                                   conn_key: Tuple[str, int, str, int], msg_size: int):
        """Process a multi-frame ZeroMQ message."""
        # Determine envelope vs content frames (look for empty delimiter frame)
        envelope_frames = []
        content_frames = []
        delimiter_found = False
        
        for i, fr in enumerate(frames):
            if fr.length == 0:  # empty frame
                delimiter_found = True
                continue  # skip adding delimiter to either list
            if not delimiter_found:
                envelope_frames.append((i, fr))
            else:
                content_frames.append((i, fr))
                
        # Format envelope and content parts
        envelope_str = ""
        envelope_parts = []
        
        # Check for topic-based pattern if we have exactly one envelope frame
        topic = None
        if len(envelope_frames) == 1 and envelope_frames[0][1].length < 255:
            # First frame is likely a topic/channel name
            frame_idx, frame = envelope_frames[0]
            topic_bytes = frame.body
            try:
                topic = topic_bytes.decode('utf-8', errors='ignore')
                envelope_parts.append(f"[bold green]{topic}[/bold green]")
                
                # Track the topic for pattern detection
                if topic not in session.topics:
                    session.topics[topic] = Topic(name=topic, count=1, last_seen=datetime.now())
                else:
                    old_topic = session.topics[topic]
                    session.topics[topic] = Topic(
                        name=topic, 
                        count=old_topic.count + 1, 
                        last_seen=datetime.now()
                    )
                    
                # Update socket type if not set - likely PUB/SUB pattern
                if not session.socket_type:
                    # Guess based on IP addresses - if external IP, likely a PUB
                    session.socket_type = "PUB" if session.src.split(':')[0] != session.dst.split(':')[0] else "SUB"
                    self.stats["socket_types"][session.socket_type] += 1
            except Exception:
                # Not a string topic
                envelope_parts.append(self._format_bytes(topic_bytes))
        else:
            # Generic envelope handling - try to parse each frame
            for frame_idx, frame in envelope_frames:
                raw_text = self._format_bytes(frame.body)
                envelope_parts.append(raw_text)
                
        if envelope_parts:
            ids = ", ".join(envelope_parts)
            envelope_str = f"[cyan]Envelope: {ids}[/cyan]"
            
        # Process content frames
        content_parts = []
        for frame_idx, frame in content_frames:
            raw_text = self._format_bytes(frame.body)
            
            # Try to parse JSON in content frames
            if raw_text.startswith('"') and (raw_text.endswith('"') or ' chars)' in raw_text):
                json_str = raw_text.strip('"')
                if ' (truncated,' in json_str:
                    json_str = json_str.split(' (truncated,')[0]
                parsed = self._try_parse_json(json_str)
                content_parts.append(parsed)
            else:
                content_parts.append(raw_text)
                
        content_str = "[green]Content: "
        if content_parts:
            content_str += ", ".join(content_parts)
        else:
            content_str += "(empty)"
        content_str += "[/green]"
            
        # Print the decoded message
        if envelope_frames:
            self.console.print(f"{prefix} {envelope_str} | {content_str}")
        else:
            self.console.print(f"{prefix} {content_str}")
            
        # If raw hex output is enabled, print raw frames in hex
        if self.raw_hex:
            proto = self.protocol.get(conn_key, "zmtp3")
            raw_parts = []
            for fr in frames:
                raw_frame = self._reconstruct_raw_frame(fr, proto)
                raw_parts.append(raw_frame.hex())
            self.console.print(f"{prefix} [dim]Raw:[/dim] " + " | ".join(raw_parts))
            
        # Check for JSON payloads to pretty print
        for i, fr in content_frames:
            try:
                text = fr.body.decode('utf-8', errors='replace')
                fixed_text = self._fix_json(text)
                parsed = demjson3.decode(fixed_text, strict=False)
                self.console.print(RichJSON(json.dumps(parsed, indent=2)))
                
                # Track request/response pattern
                if isinstance(parsed, dict) and 'request_id' in parsed:
                    self._track_request_response(session, parsed)
            except Exception:
                continue
                
        # Record message in session
        frame_data = []
        for fr in frames:
            frame_data.append({
                'flags': fr.flags,
                'body': fr.body.hex(),
                'command': fr.command,
                'more': fr.more
            })
            
        message_data = {
            'timestamp': datetime.now(),
            'size': msg_size,
            'frames': frame_data
        }
        
        # Add topic if detected
        if topic:
            message_data['topic'] = topic
            
        # Add envelope and content if present
        if envelope_parts:
            message_data['envelope'] = envelope_parts
        if content_parts:
            message_data['content'] = content_parts
            
        session.add_message(message_data, msg_size)
        
    def _reconstruct_raw_frame(self, fr: ZeroMQFrame, proto: str) -> bytes:
        """Reconstruct raw frame bytes for display."""
        if proto == "zmtp3":
            size_field = fr.length.to_bytes(8, 'big') if fr.long else bytes([fr.length])
            raw_frame = bytes([fr.flags]) + size_field + fr.body
        elif proto == "zmtp2":
            if fr.long:
                # Old extended frame: 0xFF + 8-byte length + flags + body
                ext_length = fr.length + 1
                raw_frame = b'\xFF' + ext_length.to_bytes(8, 'big') + bytes([fr.flags]) + fr.body
            else:
                # Old short frame: 1-byte length + flags + body
                total_len = fr.length + 1
                raw_frame = bytes([total_len]) + bytes([fr.flags]) + fr.body
        else:
            # Default (should not happen): assume ZMTP3 format
            size_field = fr.length.to_bytes(8, 'big') if fr.long else bytes([fr.length])
            raw_frame = bytes([fr.flags]) + size_field + fr.body
            
        return raw_frame
        
    def _try_extract_topic(self, data: bytes) -> Optional[str]:
        """Try to extract a topic from the first part of a message."""
        # Common ZeroMQ PUB/SUB topic formats:
        # 1. Null-terminated topic string: b"topic\0data..."
        # 2. Length-prefixed topic: b"\x05topic data..."
        # 3. Plain topic string (entire frame is the topic)
        
        # Check for null terminator (most common)
        null_pos = data.find(b'\0')
        if null_pos > 0 and null_pos < 64:  # Reasonable topic length
            try:
                topic = data[:null_pos].decode('utf-8', errors='ignore')
                if topic and all(32 <= ord(c) < 127 for c in topic):  # Printable ASCII
                    return topic
            except Exception:
                pass
                
        # Check if the entire frame looks like a topic
        if len(data) < 64:  # Reasonable topic size
            try:
                topic = data.decode('utf-8', errors='ignore')
                if topic and all(32 <= ord(c) < 127 for c in topic):  # Printable ASCII
                    return topic
            except Exception:
                pass
                
        # Check for length-prefixed topic
        if len(data) > 1:
            prefix_len = data[0]
            if 1 < prefix_len < 64 and len(data) > prefix_len + 1:
                try:
                    topic = data[1:prefix_len+1].decode('utf-8', errors='ignore')
                    if topic and all(32 <= ord(c) < 127 for c in topic):  # Printable ASCII
                        return topic
                except Exception:
                    pass
                    
        return None
        
    def _track_request_response(self, session: Session, msg: Dict):
        """Track request/response patterns for correlation."""
        # Extract request ID
        request_id = msg.get('request_id')
        if not request_id or request_id == 'null':
            return
            
        # Determine if this is a request or response
        msg_type = 'unknown'
        if 'message_type' in msg:
            msg_type = msg['message_type'].lower()
        elif 'type' in msg:
            msg_type = msg['type'].lower()
        elif 'method' in msg:
            msg_type = msg['method'].lower()
            
        is_request = ('request' in msg_type or 'cmd' in msg_type or 'query' in msg_type)
        is_response = ('response' in msg_type or 'reply' in msg_type or 'result' in msg_type)
        
        if not (is_request or is_response):
            return
            
        # Get existing correlation if any
        corr = session.correlated_msgs.get(request_id)
        
        if is_request:
            if corr and corr.response_msg:
                # We already have a response for this ID! This is likely a new request with the same ID
                # Just replace it
                session.correlated_msgs[request_id] = CorrelatedMessage(
                    request_id=request_id,
                    timestamp=datetime.now(),
                    request_msg=msg
                )
            elif not corr:
                # New request
                session.correlated_msgs[request_id] = CorrelatedMessage(
                    request_id=request_id,
                    timestamp=datetime.now(),
                    request_msg=msg
                )
        elif is_response:
            if corr and corr.request_msg:
                # Complete the correlation
                session.correlated_msgs[request_id] = CorrelatedMessage(
                    request_id=request_id,
                    timestamp=corr.timestamp,
                    request_msg=corr.request_msg,
                    response_msg=msg
                )
                
                # Calculate response time
                elapsed = (datetime.now() - corr.timestamp).total_seconds()
                if self.debug:
                    self.console.print(f"[dim]Debug: Request-response pair completed for {request_id}, elapsed time: {elapsed:.3f}s[/dim]")
                    
                # Infer socket type based on req/resp pattern if not already set
                if not session.socket_type:
                    session.socket_type = "REP"
                    self.stats["socket_types"][session.socket_type] += 1
                    
                    # Set peer socket type if possible
                    peer_session_id = self.session_peers.get(session.session_id)
                    if peer_session_id and peer_session_id in self.sessions:
                        peer_session = self.sessions[peer_session_id]
                        if not peer_session.socket_type:
                            peer_session.socket_type = "REQ"
                            self.stats["socket_types"][peer_session.socket_type] += 1
                            
                        # Update pattern types for both sessions
                        pattern = session.detect_pattern()
                        if pattern != PatternType.UNKNOWN:
                            session.pattern = pattern
                            peer_session.pattern = pattern
                            self.stats["pattern_types"][pattern] += 1
            else:
                # Response without a request - track it anyway
                session.correlated_msgs[request_id] = CorrelatedMessage(
                    request_id=request_id,
                    timestamp=datetime.now(),
                    response_msg=msg
                )

    def _normalize_zmtp_version(self, major: int, minor: int) -> Tuple[int, int]:
        """Normalize and validate ZMTP version numbers."""
        # ZMTP has valid versions: 1.0, 2.0, 3.0, 3.1
        if major > 3:
            # Invalid major version, default to latest standard version
            if self.debug:
                self.console.print(f"[yellow]Warning:[/yellow] Invalid ZMTP major version {major}, normalizing to 3")
            major = 3
            minor = 0
        elif major == 3 and minor > 1:
            # Invalid minor version for ZMTP 3.x
            if self.debug:
                self.console.print(f"[yellow]Warning:[/yellow] Invalid ZMTP 3.x minor version {minor}, normalizing to 0")
            minor = 0
        elif major < 1:
            # Invalid major version too low
            if self.debug:
                self.console.print(f"[yellow]Warning:[/yellow] Invalid ZMTP major version {major}, normalizing to 1")
            major = 1
            minor = 0
            
        return major, minor
        
    def _detect_zmtp_mechanism(self, mech_bytes: bytes) -> str:
        """Detect and validate ZMTP security mechanism."""
        # Standard ZMTP mechanisms
        valid_mechanisms = ['NULL', 'PLAIN', 'CURVE', 'GSSAPI']
        
        try:
            # Find null terminator for the mechanism name
            null_pos = mech_bytes.find(0)
            if null_pos != -1:
                mech = mech_bytes[:null_pos].decode('ascii', errors='ignore')
            else:
                mech = mech_bytes.rstrip(b'\x00').decode('ascii', errors='ignore')
                
                # Verify mechanism is valid (common ZMTP mechanisms)
                if mech not in valid_mechanisms:
                    # If it looks like JSON, it's probably application data
                    if '{' in mech and '"' in mech:
                        if self.debug:
                            self.console.print(f"[yellow]Warning:[/yellow] Found JSON-like data in security mechanism field: '{mech[:20]}...', assuming NULL")
                        return "NULL"
                        
                        # If empty, assume NULL
                        if not mech or mech.isspace():
                            return "NULL"
                        
                        # Unknown but text-like mechanism
                        if self.debug:
                            self.console.print(f"[yellow]Warning:[/yellow] Unrecognized security mechanism '{mech}', assuming custom extension")
                        return f"CUSTOM:{mech}"
                
                return mech
        except Exception as e:
            if self.debug:
                self.console.print(f"[yellow]Warning:[/yellow] Could not decode security mechanism: {e}, assuming NULL")
            return "NULL"
    
    def _detect_zmtp_role(self, role_byte: int) -> str:
        """Detect and validate ZMTP peer role."""
        if role_byte == 1:
            return "Server"
        elif role_byte == 0:
            return "Client" 
        else:
            # Invalid role byte
            if self.debug:
                self.console.print(f"[yellow]Warning:[/yellow] Invalid role byte {role_byte}, assuming Client")
            return "Client"

    def _analyze_flags(self, flags: int) -> Dict[str, Any]:
        """Analyze the frame flag bits to determine what extensions might be in use."""
        result = {
            "standard": (flags >> 3) == 0,  # Standard ZMTP has bits 7-3 as 0
            "more": bool(flags & 0x01),     # MORE flag (bit 0)
            "long": bool(flags & 0x02),     # LONG flag (bit 1)
            "command": bool(flags & 0x04),  # COMMAND flag (bit 2)
            "extensions": [],               # List of possible extensions in use
            "valid": True,                  # Whether the frame is likely valid despite non-standard bits
            "description": ""               # Human-readable description of the flag bits
        }
        
        # Check for known extensions in high bits
        for bit_mask, name in self.known_flag_extensions.items():
            if flags & bit_mask:
                result["extensions"].append(name)
        
        # Command frames with MORE flag are invalid in standard ZMTP
        if result["command"] and result["more"]:
            if self.tolerance_level == "low":
                result["valid"] = False
            else:
                # For medium/high tolerance, we'll still process these
                result["valid"] = True
        
        # Build a human-readable description of the flags
        flag_parts = []
        if result["more"]:
            flag_parts.append("MORE")
        if result["long"]:
            flag_parts.append("LONG")
        if result["command"]:
            flag_parts.append("COMMAND")
        if result["extensions"]:
            flag_parts.extend(result["extensions"])
            
        result["description"] = " | ".join(flag_parts) if flag_parts else "NONE"
        
        return result
        
    def _should_warn_for_flags(self, flags_info: Dict[str, Any]) -> bool:
        """Determine whether to warn about non-standard flag bits based on tolerance level."""
        if flags_info["standard"]:
            return False  # No warning for standard flags
            
        # Always warn for invalid flags at any tolerance level
        if not flags_info["valid"]:
            return True
            
        # For low tolerance, warn about any non-standard flags
        if self.tolerance_level == "low":
            return True
            
        # For medium tolerance, warn only if we don't recognize the extension
        if self.tolerance_level == "medium":
            return not flags_info["extensions"]
            
        # For high tolerance, don't warn about known extensions
        if self.tolerance_level == "high":
            return False
            
        # Default (shouldn't reach here)
        return not flags_info["standard"]

if __name__ == "__main__":
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
            import threading
            import signal
            
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
