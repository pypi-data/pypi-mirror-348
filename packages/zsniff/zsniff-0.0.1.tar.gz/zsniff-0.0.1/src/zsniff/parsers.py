from __future__ import annotations

from typing import Dict, Optional, Tuple

from .models import ZeroMQFrame
from .utils import analyze_flags, looks_like_valid_data


class FrameParser:
    """Parser for ZeroMQ frames in various protocol versions."""
    
    def __init__(self, max_buffer_size: int = 1024 * 1024, debug: bool = False):
        """
        Initialize the frame parser.
        
        Args:
            max_buffer_size: Maximum buffer size for frames
            debug: Enable debug output
        """
        self.max_buffer_size = max_buffer_size
        self.debug = debug
        self.known_flag_extensions = {
            0x10: "ZMQ_MSG_COMMAND", # Command frame in some implementations
            0x20: "ZMQ_MSG_LARGE",   # Large message extension
            0x40: "ZMQ_MSG_SHARED",  # Shared storage
            0x80: "ZMQ_MSG_MASK"     # Mask for other extensions
        }
        
    def parse_zmtp3_frame(self, buf: bytearray) -> Tuple[Optional[ZeroMQFrame], int]:
        """
        Parse one ZMTP/3.x frame from the buffer.
        
        Args:
            buf: Buffer containing frame data
            
        Returns:
            Tuple of (ZeroMQFrame or None if incomplete, bytes consumed)
        """
        if len(buf) < 2:
            return None, 0  # not enough for flags+size
            
        flags = buf[0]
        flags_info = analyze_flags(flags, self.known_flag_extensions)
        
        # Check if flags are too non-standard to continue
        if not flags_info["valid"]:
            raise ValueError(f"Invalid flag combination: {bin(flags)} ({flags_info['description']})")
            
        long_frame = bool(flags & 0x02)
        if long_frame:
            if len(buf) < 9:
                return None, 0  # need 8-byte length
            size = int.from_bytes(buf[1:9], 'big')
            
            # Sanity check the size - implement intelligent size validation
            if size > self.max_buffer_size:
                # Before completely rejecting, check if this might be valid data
                if looks_like_valid_data(buf[1:min(17, len(buf))]):
                    # Try to continue with a truncated frame
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
        frame = ZeroMQFrame(
            flags=flags, 
            more=more_flag, 
            long=long_frame, 
            command=cmd_flag, 
            length=size, 
            body=body_bytes
        )
        
        # Set non-standard flag for abnormal flags
        if not flags_info["standard"]:
            frame.non_standard = True
            
        # Set invalid flag for invalid flag combinations
        if not flags_info["valid"]:
            frame.invalid = True
        
        return frame, header_len + size
        
    def parse_zmtp2_frame(self, buf: bytearray) -> Tuple[Optional[ZeroMQFrame], int]:
        """
        Parse one ZMTP/1.0 or 2.x frame (length-included format).
        
        Args:
            buf: Buffer containing frame data
            
        Returns:
            Tuple of (ZeroMQFrame or None if incomplete, bytes consumed)
        """
        if len(buf) < 1:
            return None, 0
            
        first = buf[0]
        if first < 0xFF:
            # Short frame (1-byte length includes flags)
            if first == 0:
                # Some implementations might send a zero-length frame indicator
                # Instead of failing, treat it as a special case with empty body
                if self.debug:
                    print("[yellow]Warning:[/yellow] Zero-length frame in ZMTP/1.0 stream - handling as empty frame")
                # Construct a minimal valid frame and consume the byte
                frame = ZeroMQFrame(flags=0, more=False, long=False, command=False, length=0, body=b'')
                return frame, 1
                
            total = first  # length of flags+body
            if len(buf) < 1 + total:
                return None, 0
                
            # Sanity check the size with improved validation
            if total > self.max_buffer_size:
                # Check if this looks like a valid frame despite the large size
                if looks_like_valid_data(buf[1:min(total+1, len(buf))]):
                    raise ValueError(f"Frame size {total} exceeds maximum allowed size {self.max_buffer_size}")
                else:
                    raise ValueError(f"Frame size {total} exceeds maximum allowed size {self.max_buffer_size}")
                
            flags = buf[1] if total >= 1 else 0
            flags_info = analyze_flags(flags, self.known_flag_extensions)
            
            body_len = total - 1
            body_bytes = bytes(buf[2 : 2 + body_len]) if body_len > 0 else b''
            more_flag = bool(flags & 0x01)
            cmd_flag = bool(flags & 0x04)
            long_flag = False
            
            frame = ZeroMQFrame(
                flags=flags, 
                more=more_flag, 
                long=long_flag, 
                command=cmd_flag, 
                length=body_len, 
                body=body_bytes
            )
            
            # Set non-standard flag for abnormal flags
            if not flags_info["standard"]:
                frame.non_standard = True
                
            # Set invalid flag for invalid flag combinations
            if not flags_info["valid"]:
                frame.invalid = True
            
            return frame, 1 + total
        else:
            # Long frame (0xFF marker followed by 8-byte length)
            if len(buf) < 9:
                return None, 0
                
            ext_size = int.from_bytes(buf[1:9], 'big')
            
            # Enhanced size validation
            if ext_size > self.max_buffer_size:
                # Check if this looks like valid data despite size
                if looks_like_valid_data(buf[9:min(9+ext_size, len(buf))]):
                    raise ValueError(f"Frame size {ext_size} exceeds maximum allowed size {self.max_buffer_size}")
                else:
                    raise ValueError(f"Frame size {ext_size} exceeds maximum allowed size {self.max_buffer_size}")
                
            if ext_size == 0:
                # Handle zero-length extended frames too
                if self.debug:
                    print("[yellow]Warning:[/yellow] Zero-length extended frame in ZMTP/1.0 stream - handling as empty frame")
                frame = ZeroMQFrame(flags=0, more=False, long=True, command=False, length=0, body=b'')
                return frame, 9
                
            if len(buf) < 1 + 8 + ext_size:
                return None, 0
                
            flags = buf[9]
            flags_info = analyze_flags(flags, self.known_flag_extensions)
            
            body_len = ext_size - 1
            body_bytes = bytes(buf[10 : 10 + body_len]) if body_len > 0 else b''
            more_flag = bool(flags & 0x01)
            cmd_flag = bool(flags & 0x04)
            long_flag = True
            
            frame = ZeroMQFrame(
                flags=flags, 
                more=more_flag,
                long=long_flag, 
                command=cmd_flag, 
                length=body_len, 
                body=body_bytes
            )
            
            # Set non-standard flag for abnormal flags
            if not flags_info["standard"]:
                frame.non_standard = True
                
            # Set invalid flag for invalid flag combinations
            if not flags_info["valid"]:
                frame.invalid = True
            
            return frame, 1 + 8 + ext_size
    
    def try_find_next_frame(self, buf: bytearray) -> int:
        """
        Try to find the next potential valid frame start after an error.
        
        Args:
            buf: Buffer to search through
            
        Returns:
            Number of bytes to skip, or 1 if no pattern is found
        """
        # Don't scan more than 1024 bytes ahead to avoid performance issues
        # but also make sure we scan enough to find valid frames
        scan_len = min(1024, len(buf))
        
        if self.debug:
            print(f"[dim]Debug: Scanning {scan_len} bytes for next frame: {bytes(buf[:min(64, scan_len)]).hex()}...[/dim]")
            
        # Skip at least 1 byte
        if scan_len <= 1:
            return 1
            
        # First, check for common ZeroMQ message patterns
        
        # 1. JSON data pattern - high priority since this is likely application data
        for i in range(1, min(scan_len - 2, 64)):  # Only scan the first 64 bytes for JSON
            # Check for common JSON object starts
            if buf[i:i+2] in [b'{"', b'[{', b'["', b'[]', b'{}']:
                if self.debug:
                    print(f"[dim]Debug: Found potential JSON start at offset {i}: {bytes(buf[i:i+10]).hex()}[/dim]")
                return i
        
        # 2. Check for ZMTP handshake signature (0xFF ... 0x7F) - very distinctive
        for i in range(1, scan_len - 10):
            if buf[i] == 0xFF and i+9 < scan_len and buf[i+9] == 0x7F:
                # Found ZMTP3 greeting signature
                if self.debug:
                    print(f"[dim]Debug: Found ZMTP3 greeting at offset {i}: {bytes(buf[i:i+16]).hex()}[/dim]")
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
                            print(f"[dim]Debug: Found potential ZMTP3 long frame at offset {i}: {bytes(buf[i:i+16]).hex()}[/dim]")
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
                                print(f"[dim]Debug: Found potential ZMTP3 short frame at offset {i}: {bytes(buf[i:i+min(16, 2+length)]).hex()}[/dim]")
                            return i
        
        # 4. Look for ZMTP2 frame patterns
        for i in range(1, scan_len - 9):
            # Check for extended frame marker (0xFF)
            if buf[i] == 0xFF and i + 9 < scan_len:
                length = int.from_bytes(buf[i+1:i+9], 'big')
                # Verify length is within reasonable bounds
                if 0 < length < 1_000_000:
                    if self.debug:
                        print(f"[dim]Debug: Found potential ZMTP2 extended frame at offset {i}: {bytes(buf[i:i+16]).hex()}[/dim]")
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
                            print(f"[dim]Debug: Found potential ZMTP2 short frame at offset {i}: {bytes(buf[i:i+min(16, 2+frame_len)]).hex()}[/dim]")
                        return i
        
        # 5. Look for null delimiter frames (common in ZeroMQ patterns)
        for i in range(1, scan_len - 2):
            # Check for a pattern like a flag byte followed by a zero length
            if (buf[i] & 0xF8) == 0 and buf[i+1] == 0:
                if self.debug:
                    print(f"[dim]Debug: Found potential null delimiter frame at offset {i}: {bytes(buf[i:i+4]).hex()}[/dim]")
                return i
                
        # 6. Fallback: look for strings or printable text that could be message content
        for i in range(1, min(scan_len - 8, 128)):  # Only scan first 128 bytes for this
            # Check for a sequence of printable ASCII characters (likely part of a message)
            if all(32 <= b <= 126 for b in buf[i:i+8]):
                if self.debug:
                    print(f"[dim]Debug: Found ASCII text at offset {i}: {bytes(buf[i:i+16]).hex()}[/dim]")
                return i
                
        # 7. If still not found, skip to next non-zero byte
        # This helps when we have padding or garbage bytes
        for i in range(1, min(scan_len, 64)):  # Limit this search to avoid getting stuck
            if buf[i] != 0:
                if self.debug:
                    print(f"[dim]Debug: Skipping to first non-zero byte at offset {i}[/dim]")
                return i
                
        # 8. Last resort - just skip one byte and try again
        if self.debug:
            print("[dim]Debug: No recovery pattern found, skipping one byte[/dim]")
        return 1
        
    def reconstruct_raw_frame(self, frame: ZeroMQFrame, proto: str) -> bytes:
        """
        Reconstruct raw frame bytes for display.
        
        Args:
            frame: ZeroMQ frame
            proto: Protocol type (zmtp3 or zmtp2)
            
        Returns:
            Raw frame bytes
        """
        if proto == "zmtp3":
            size_field = frame.length.to_bytes(8, 'big') if frame.long else bytes([frame.length])
            raw_frame = bytes([frame.flags]) + size_field + frame.body
        elif proto == "zmtp2":
            if frame.long:
                # Old extended frame: 0xFF + 8-byte length + flags + body
                ext_length = frame.length + 1
                raw_frame = b'\xFF' + ext_length.to_bytes(8, 'big') + bytes([frame.flags]) + frame.body
            else:
                # Old short frame: 1-byte length + flags + body
                total_len = frame.length + 1
                raw_frame = bytes([total_len]) + bytes([frame.flags]) + frame.body
        else:
            # Default (should not happen): assume ZMTP3 format
            size_field = frame.length.to_bytes(8, 'big') if frame.long else bytes([frame.length])
            raw_frame = bytes([frame.flags]) + size_field + frame.body
            
        return raw_frame 