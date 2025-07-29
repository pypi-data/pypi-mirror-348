"""ZeroMQ message processor module"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import demjson3
from rich.console import Console
from rich.json import JSON as RichJSON

from .models import CorrelatedMessage, PatternType, Session, SocketType, Topic, ZeroMQFrame
from .parsers import FrameParser
from .utils import (
    format_bytes,
    format_bytes_count,
    try_extract_topic,
    try_parse_json,
)


class MessageProcessor:
    """
    Processes ZeroMQ messages and sessions, handling visualization and analysis.
    """
    
    def __init__(
        self,
        debug: bool = False,
        raw_hex: bool = False,
        tolerance_level: str = "medium",
        console: Optional[Console] = None,
    ):
        """
        Initialize the message processor.
        
        Args:
            debug: Enable debug output
            raw_hex: Show raw frame bytes in hex
            tolerance_level: Protocol tolerance level (low, medium, high)
            console: Rich console for output (or create new one if None)
        """
        self.debug = debug
        self.raw_hex = raw_hex
        self.tolerance_level = tolerance_level
        self.console = console or Console()
        
        # Statistics tracking
        self.stats = {
            "socket_types": defaultdict(int),
            "pattern_types": defaultdict(int),
        }
    
    def process_command_frame(self, prefix: str, frame: ZeroMQFrame, session: Session, msg_size: int,
                              protocol: Optional[str] = None, sessions: Optional[Dict] = None,
                              conn_sessions: Optional[Dict] = None, session_peers: Optional[Dict] = None):
        """
        Process a command frame (like READY, SUBSCRIBE, etc.)
        
        Args:
            prefix: Message prefix for display
            frame: The ZeroMQ frame
            session: Session object
            msg_size: Message size in bytes
            protocol: Protocol type (zmtp2/zmtp3)
            sessions: Session dict for peer updates
            conn_sessions: Connection to session mapping
            session_peers: Session peer relationships
        """
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
            
        data_info = format_bytes(data_bytes) if data_bytes else ""
        
        # Handle READY command specially to extract socket type
        if cmd_name == "READY":
            socket_type, data_info = self._extract_socket_type(
                data_bytes, data_info, session, sessions, conn_sessions, session_peers
            )
            
            # Update the socket type counts for statistics
            self.stats["socket_types"][socket_type] += 1
        
        # Print command (yellow name, magenta content if any)
        self.console.print(f"{prefix} [bold yellow]Command[/bold yellow] [magenta]{cmd_name}[/magenta] {data_info}")
        if self.raw_hex:
            # Get the protocol type
            proto = protocol or "zmtp3"
            
            # Get the frame parser for reconstructing raw frames
            parser = FrameParser(debug=self.debug)
            
            # Reconstruct raw frame bytes (including header)
            raw_frame = parser.reconstruct_raw_frame(frame, proto)
            self.console.print(f"{prefix} [dim]Raw:[/dim] {raw_frame.hex()}")
            
        # After command processing, try to pretty-print any JSON in the command data
        try:
            if data_bytes:
                text = data_bytes.decode('utf-8', errors='replace')
                fixed_text = try_parse_json(text)
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
            
    def _extract_socket_type(self, data_bytes: bytes, data_info: str, session: Session, 
                             sessions: Optional[Dict] = None, conn_sessions: Optional[Dict] = None, 
                             session_peers: Optional[Dict] = None) -> Tuple[str, str]:
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
                    if sessions and conn_sessions and session_peers:
                        peer_conn = (session.dst, session.dst_port, session.src, session.src_port)
                        peer_session_id = conn_sessions.get(peer_conn)
                        if peer_session_id and peer_session_id in sessions:
                            peer_session = sessions[peer_session_id]
                            peer_session.peer_socket_type = socket_type
                            session.peer_socket_type = peer_session.socket_type
                            
                            # Record peer relationship
                            session_peers[session.session_id] = peer_session_id
                            session_peers[peer_session_id] = session.session_id
                            
                            # Update pattern types for both sessions
                            pattern = session.detect_pattern()
                            if pattern != PatternType.UNKNOWN:
                                session.pattern = pattern
                                peer_session.pattern = pattern
                                self.stats["pattern_types"][pattern] += 1
            except Exception:
                pass
                
        return socket_type, data_info
        
    def process_multiframe_message(self, prefix: str, frames: List[ZeroMQFrame], session: Session, 
                                   protocol: str = "zmtp3", msg_size: int = 0, 
                                   sessions: Optional[Dict] = None, session_peers: Optional[Dict] = None):
        """
        Process a multi-frame ZeroMQ message.
        
        Args:
            prefix: Message prefix for display
            frames: List of ZeroMQ frames
            session: Session object
            protocol: Protocol type (zmtp2/zmtp3)
            msg_size: Message size in bytes
            sessions: Session dict for peer updates
            session_peers: Session peer relationships
        """
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
                envelope_parts.append(format_bytes(topic_bytes))
        else:
            # Generic envelope handling - try to parse each frame
            for frame_idx, frame in envelope_frames:
                raw_text = format_bytes(frame.body)
                envelope_parts.append(raw_text)
                
        if envelope_parts:
            ids = ", ".join(envelope_parts)
            envelope_str = f"[cyan]Envelope: {ids}[/cyan]"
            
        # Process content frames
        content_parts = []
        for frame_idx, frame in content_frames:
            raw_text = format_bytes(frame.body)
            
            # Try to parse JSON in content frames
            if raw_text.startswith('"') and (raw_text.endswith('"') or ' chars)' in raw_text):
                json_str = raw_text.strip('"')
                if ' (truncated,' in json_str:
                    json_str = json_str.split(' (truncated,')[0]
                parsed = try_parse_json(json_str)
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
            parser = FrameParser(debug=self.debug)
            raw_parts = []
            for fr in frames:
                raw_frame = parser.reconstruct_raw_frame(fr, protocol)
                raw_parts.append(raw_frame.hex())
            self.console.print(f"{prefix} [dim]Raw:[/dim] " + " | ".join(raw_parts))
            
        # Check for JSON payloads to pretty print
        for i, fr in content_frames:
            try:
                text = fr.body.decode('utf-8', errors='replace')
                fixed_text = try_parse_json(text)
                parsed = demjson3.decode(fixed_text, strict=False)
                self.console.print(RichJSON(json.dumps(parsed, indent=2)))
                
                # Track request/response pattern
                if isinstance(parsed, dict) and 'request_id' in parsed:
                    self._track_request_response(session, parsed, sessions, session_peers)
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
        
    def _track_request_response(self, session: Session, msg: Dict, 
                               sessions: Optional[Dict] = None, session_peers: Optional[Dict] = None):
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
                    if sessions and session_peers:
                        peer_session_id = session_peers.get(session.session_id)
                        if peer_session_id and peer_session_id in sessions:
                            peer_session = sessions[peer_session_id]
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