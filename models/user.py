from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    role: str = ""
    created_at: Optional[str] = None