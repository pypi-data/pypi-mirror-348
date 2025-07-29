from __future__ import annotations

import json
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import demjson3


def format_bytes_count(bytes_count: int) -> str:
    """Format byte count to human-readable string with appropriate units."""
    if bytes_count < 1024:
        return f"{bytes_count} B"
    elif bytes_count < 1024 * 1024:
        return f"{bytes_count / 1024:.1f} KB"
    elif bytes_count < 1024 * 1024 * 1024:
        return f"{bytes_count / (1024 * 1024):.1f} MB"
    else:
        return f"{bytes_count / (1024 * 1024 * 1024):.1f} GB"


def format_duration(duration: timedelta) -> str:
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


def format_bytes(data: bytes) -> str:
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


def fix_json(data_str: str) -> str:
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
    except Exception:
        # If we can't parse it with demjson3, return the fixed string 
        # for standard libraries to try
        return data_str


def try_parse_json(data_str: str, debug: bool = False) -> str:
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
    fixed_data_str = fix_json(data_str)
    
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
        if debug:
            # Show detailed error message in debug mode
            if '{' in data_str and '}' not in data_str:
                return f"{data_str}... [dim](truncated JSON)[/dim]"
            
            # Show parsing error details
            return f"{data_str} [dim](JSON parse error: {e})[/dim]"
            
        return data_str


def try_extract_topic(data: bytes) -> Optional[str]:
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


def analyze_flags(flags: int, known_flag_extensions: Dict[int, str]) -> Dict[str, Any]:
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
    for bit_mask, name in known_flag_extensions.items():
        if flags & bit_mask:
            result["extensions"].append(name)
    
    # Command frames with MORE flag are invalid in standard ZMTP
    if result["command"] and result["more"]:
        result["valid"] = False
    
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


def looks_like_valid_data(data: bytes) -> bool:
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


def normalize_zmtp_version(major: int, minor: int, debug: bool = False) -> Tuple[int, int]:
    """Normalize and validate ZMTP version numbers."""
    # ZMTP has valid versions: 1.0, 2.0, 3.0, 3.1
    if major > 3:
        # Invalid major version, default to latest standard version
        if debug:
            print(f"[yellow]Warning:[/yellow] Invalid ZMTP major version {major}, normalizing to 3")
        major = 3
        minor = 0
    elif major == 3 and minor > 1:
        # Invalid minor version for ZMTP 3.x
        if debug:
            print(f"[yellow]Warning:[/yellow] Invalid ZMTP 3.x minor version {minor}, normalizing to 0")
        minor = 0
    elif major < 1:
        # Invalid major version too low
        if debug:
            print(f"[yellow]Warning:[/yellow] Invalid ZMTP major version {major}, normalizing to 1")
        major = 1
        minor = 0
        
    return major, minor


def detect_zmtp_mechanism(mech_bytes: bytes, debug: bool = False) -> str:
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
                    if debug:
                        print(f"[yellow]Warning:[/yellow] Found JSON-like data in security mechanism field: '{mech[:20]}...', assuming NULL")
                    return "NULL"
                    
                    # If empty, assume NULL
                    if not mech or mech.isspace():
                        return "NULL"
                    
                    # Unknown but text-like mechanism
                    if debug:
                        print(f"[yellow]Warning:[/yellow] Unrecognized security mechanism '{mech}', assuming custom extension")
                    return f"CUSTOM:{mech}"
            
            return mech
    except Exception as e:
        if debug:
            print(f"[yellow]Warning:[/yellow] Could not decode security mechanism: {e}, assuming NULL")
        return "NULL"


def detect_zmtp_role(role_byte: int, debug: bool = False) -> str:
    """Detect and validate ZMTP peer role."""
    if role_byte == 1:
        return "Server"
    elif role_byte == 0:
        return "Client" 
    else:
        # Invalid role byte
        if debug:
            print(f"[yellow]Warning:[/yellow] Invalid role byte {role_byte}, assuming Client")
        return "Client" 