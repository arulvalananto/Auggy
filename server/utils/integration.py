from models.common import Classification
from models.paddyfield import AddLog
from utils.chains import Chain
from utils.enums import Apps


class Integration:
    @staticmethod
    def process(question: str, classification: Classification) -> str:
        app_name = classification["app_name"].lower().replace(" ", "")

        template = None
        if app_name == Apps.PADDY_FIELD.value:
            template = AddLog
        else:
            template = None

        if template is None:
            return "We are sorry, but we do not have the capability to process this request."
        else:
            payload_chain = Chain.payload_formatter(template=template)
            payload = payload_chain.invoke({"question": question})

            return {"payload": payload}
