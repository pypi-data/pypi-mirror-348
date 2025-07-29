from dataclasses import dataclass, asdict, field
from nemo_library.utils.utils import get_internal_name

@dataclass
class AttributeLink:
    """
    Represents a link between attributes with various properties and settings.
    """

    sourceAttributeId: str = ""
    order: str = ""
    parentAttributeGroupInternalName: str = ""
    displayNameTranslations: dict[str, str] = field(default_factory=dict)
    displayName: str = None
    internalName: str = None
    id: str = ""
    projectId: str = ""
    tenant: str = ""
    isCustom: bool = False
    metadataClassificationInternalName: str = ""

    def to_dict(self):
        """
        Converts the AttributeLink instance to a dictionary.

        Returns:
            dict: A dictionary representation of the AttributeLink instance.
        """
        return asdict(self)

    def __post_init__(self):
        """
        Post-initialization processing to set the internal name if it is not provided.
        """
        if self.internalName is None:
            self.internalName = get_internal_name(self.displayName)