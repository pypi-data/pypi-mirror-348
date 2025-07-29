"""Models"""

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Union
from pathlib import Path
from s3async.utils import snake_to_pascal_case


OptionalPathLike = Union[Optional[Path], Optional[str]]
KeyVersionInfo = Tuple[str, str, datetime, bool]


@dataclass
class ObjectMetadata:
    """Additional S3 object metadata"""

    cache_control: Optional[str] = None
    content_type: Optional[str] = None
    content_encoding: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        """Convert to boto3 compatible dictionary while omitting None values"""
        dct = asdict(self)
        return {snake_to_pascal_case(key): value for key, value in dct.items() if value is not None}
