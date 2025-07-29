from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class AttributeTreeElement:
    internalName: Optional[str] = ""
    order: Optional[str] = ""
    parentAttributeGroupInternalName: Optional[str] = ""
    metadataType: Optional[str] = ""
    id: Optional[str] = ""
    projectId: Optional[str] = ""
    tenant: Optional[str] = ""
    isCustom: Optional[bool] = False
    metadataClassificationInternalName: Optional[str] = ""

    def to_dict(self):
        """
        Converts the Application instance to a dictionary.

        Returns:
            dict: The dictionary representation of the Application instance.
        """
        return asdict(self)
