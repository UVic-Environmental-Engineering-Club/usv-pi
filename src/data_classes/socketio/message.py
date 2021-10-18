""" Contains all dataclasses for socketio messages to/from ground control"""

from dataclasses import dataclass


@dataclass
class Message:
    """Base socketio Message"""
