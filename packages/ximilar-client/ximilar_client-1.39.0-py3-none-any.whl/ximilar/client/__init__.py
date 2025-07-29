from .client import RestClient
from .recognition import RecognitionClient
from .tagging import GenericTaggingClient, FashionTaggingClient, HomeDecorTaggingClient
from .colors import DominantColorProductClient, DominantColorGenericClient
from .detection import DetectionClient
from .search import (
    SimilarityPhotosClient,
    SimilarityProductsClient,
    SimilarityFashionClient,
    SimilarityCustomClient,
    ImageMatchingSearchClient,
    SimilarityColorsClient,
    SimilarityHomeDecorClient,
)
from .collectibles import CardGradingClient, CollectiblesRecognitionClient, CardConditionClient, CardCenteringClient
from .flows import FlowsClient
from .exceptions import XimilarClientException
from .removebg import RemoveBGClient
from .similarity import CustomSimilarityClient
from .upscaler import UpscaleClient
from .asyncr import AsyncRClient, AsynchronousRequest
from .ocr import OCRClient
from .description import ProductDescriptionClient
