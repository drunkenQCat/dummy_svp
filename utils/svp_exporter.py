from models.svp import Svp, Time, RenderConfig
import json

svp = Svp(
    version=11,
    time=Time(),
    library=[],
    tracks=[],
    renderConfig=RenderConfig.from_filename("test"),
)
json.dumps(svp.model_dump(), ensure_ascii=True)
