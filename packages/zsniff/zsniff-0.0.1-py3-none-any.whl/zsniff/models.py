from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional, Set

from pydantic import BaseModel, Field, model_validator


class SocketType(str, Enum):
    """ZeroMQ Socket Types as Enum"""
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
        """Get a human-readable description of the socket type."""
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


class PatternType(str, Enum):
    """ZeroMQ Pattern Types"""
    PUBSUB = "PUB-SUB"
    REQREP = "REQ-REP"
    PUSHPULL = "PUSH-PULL"
    PAIRPAIR = "PAIR-PAIR"
    DEALERROUTER = "DEALER-ROUTER"
    UNKNOWN = "UNKNOWN"


class CorrelatedMessage(NamedTuple):
    """Data class to track a ZeroMQ message correlated by ID"""
    request_id: str
    timestamp: datetime
    request_msg: Optional[Dict] = None
    response_msg: Optional[Dict] = None


class Topic(NamedTuple):
    """Data class to track a ZeroMQ Topic"""
    name: str
    count: int = 0
    last_seen: datetime = field(default_factory=datetime.now)


@dataclass
class Session:
    """Data class to track a ZeroMQ connection session"""
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


class ZeroMQFrame(BaseModel):
    """Pydantic model for a ZeroMQ frame (wire format)"""
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