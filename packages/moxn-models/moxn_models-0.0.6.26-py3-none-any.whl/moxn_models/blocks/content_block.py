from pydantic import TypeAdapter

from moxn_models.blocks.image import ImageContentFromSourceModel
from moxn_models.blocks.document import PDFContentFromSourceModel
from moxn_models.blocks.signed import SignedURLContentModel
from moxn_models.blocks.variable import VariableContentModel
from moxn_models.blocks.text import TextContentModel

ContentBlockModel = (
    ImageContentFromSourceModel
    | PDFContentFromSourceModel
    | SignedURLContentModel
    | TextContentModel
    | VariableContentModel
)

ContentBlockAdapter: TypeAdapter[ContentBlockModel] = TypeAdapter(ContentBlockModel)
