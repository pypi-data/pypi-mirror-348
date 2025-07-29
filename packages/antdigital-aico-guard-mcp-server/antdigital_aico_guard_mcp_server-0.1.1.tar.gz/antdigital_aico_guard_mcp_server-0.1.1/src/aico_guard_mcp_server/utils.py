
from antchain_sdk_aitechguard.client import Client as AITECHGUARDClient
from antchain_sdk_aitechguard import models as aitechguard_models
import uuid
import os
# pip install antchain_aitechguard

def create_client() -> AITECHGUARDClient:
    """
    使用AK&SK初始化账号Client
    @param access_key_id:
    @param access_key_secret:
    @return: Client
    @throws Exception
    """
    config = aitechguard_models.Config()


    config.access_key_id = os.getenv('ANT_DIGITAL_TECHNOLOGIES_ACCESS_KEY_ID')
    config.access_key_secret = os.getenv('ANT_DIGITAL_TECHNOLOGIES_ACCESS_KEY_SECRET')
    if not config.access_key_id or not config.access_key_secret:
        raise ValueError("Missing required ant credentials. Please set ANT_DIGITAL_TECHNOLOGIES_ACCESS_KEY_ID and ANT_DIGITAL_TECHNOLOGIES_ACCESS_KEY_SECRET environment variables.")
    config.endpoint = 'openapi.antchain.antgroup.com'
    return AITECHGUARDClient(config)


def ask_check(question: str):
    ask_request = aitechguard_models.CheckAicoguardrailsAskRequest()
    ask_request.request_id = uuid.uuid1()
    ask_request.session_id = uuid.uuid1()
    ask_request.app_code = 'MCP'
    ask_request.user_id = 'test'
    ask_request.scene_code = 'guardrails_risk_identification'
    # guardrails_risk_identification， guardrails_answer_only
    ask_request.question = question
    ask_request.question_format = 'PLAINTEXT'
    resp = create_client().check_aicoguardrails_ask(ask_request)
    return resp

