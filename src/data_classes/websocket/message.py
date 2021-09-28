""" Contains all dataclasses for websocket messages to/from ground control"""

from dataclasses import dataclass


@dataclass
class Message:
    """Base websocket Message"""
