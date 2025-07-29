# -*- coding =utf-8 -*-
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class HTTPStatus(Enum):
    """HTTP status codes and reason phrases
    Status codes from the following RFCs are all observed =
        * RFC 7231 = Hypertext Transfer Protocol (HTTP/1.1), obsoletes 2616
        * RFC 6585 = Additional HTTP Status Codes
        * RFC 3229 = Delta encoding in HTTP
        * RFC 4918 = HTTP Extensions for WebDAV, obsoletes 2518
        * RFC 5842 = Binding Extensions to WebDAV
        * RFC 7238 = Permanent Redirect
        * RFC 2295 = Transparent Content Negotiation in HTTP
        * RFC 2774 = An HTTP Extension Framework
    """
    def __new__(cls, value, phrase, description=''):
        obj = object.__new__(cls)
        obj._value_ = obj
        obj.code = value
        obj.phrase = phrase
        obj.description = description
        return obj

    @property
    def value(self):
        return self.code

    # informational
    SUCCESS = (0, 'success', 'Success')

    ### 通用 40xxxxx ###

    # 400001 请求路径错误
    REQUEST_PATH_ERR = (400001, '请求路径错误', '请求路径错误')


    # 400002 请求方法错误
    REQUEST_METHOD_ERR = (400002, "请求方法错误", "请求方法错误，请使用 POST 请求")
    REQUEST_METHOD_GET_ERR = (400002, "请求方法错误", "请求方法错误，请使用 GET 请求")


    # 400003 请求体内容为空
    BODY_EMPTY_ERR = (400003, "请求体内容为空", "请求体请求数据为空，没有包含内容")


    # 400004 请求体内容为空
    BODY_JSON_ERR = (400004, "请求体非 json 格式", "请求体内容需要符合 json 要求")


    # 400005 请求体类型错误
    BODY_TYPE_ERR = (400005, "请求体类型错误", "请求体需为字典，不能为其他类型")


    # 400006 必传的参数未传
    MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Action、ImageData）未传")
    TEXT_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Action、TextData）未传")
    AUDIO_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Action、AudioData）未传")
    VIDEO_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Action、VideoData）未传")
    IMAGE_AB_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Action、ImageDataA、ImageDataB）未传")
    INPUTS_OR_URLS_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（inputs 或 input_urls）未传") # 内容审核
    IMAGE_DATA_OR_IMAGE_URL_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（ImageData 或 ImageURL）未传") # 内容审核
    AUDIO_DATA_OR_AUDIO_URL_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（AudioData 或 AudioURL）未传") # 录音文件识别
    TEXT_DATA_OR_TEXT_URL_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（TextData 或 TextURL）未传") 
    VIDEO_DATA_OR_VIDEO_URL_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（VideoData 或 VideoURL）未传") 
    IMAGE_DATA_AB_OR_IMAGE_URL_AB_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（ImageDataA、ImageDataB 或 ImageURLA、ImageURLB）未传") # 人脸比对
    WEBSOCKET_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Action、Signal）未传") # 实时语音识别
    DATA_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（data）未传")
    SMALL_DATA_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（data）未传")
    IMAGE_CONTENT_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（imageContent）未传")
    IMG1BASE64_OR_IMG2BASE64_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（img1Base64 或 img2Base64）未传")
    
    ACTION_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Action）未传")
    IMAGE_DATA_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（ImageData）未传")
    IMAGE_DATA_AB_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（ImageDataA、ImageDataB）未传")
    IMAGE_URL_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（ImageURL）未传")
    IMAGE_URL_AB_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（ImageURLA、ImageURLB）未传")
    TEXT_R_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Text）未传")
    TEXT_DATA_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（TextData）未传")
    TEXT_URL_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（TextURL）未传")
    AUDIO_DATA_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（AudioData）未传")
    AUDIO_URL_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（AudioURL）未传")
    VIDEO_DATA_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（VideoData）未传")
    VIDEO_URL_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（VideoURL）未传") 
    INPUT_URLS_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（input_urls）未传")
    APPKEY_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（AppKey）未传")
    TOKEN_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Token）未传")
    VERSION_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Version）未传")
    DEVICE_ID_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（DeviceID）未传") # 设备ID
    STREAM_URL_OR_CALLBACK_URL_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（StreamURL 或 CallbackURL）未传")  # 流语音识别：流请求
    
    MAKEUP_TYPE_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（MakeupType）未传") # 人脸美妆
    SUBTASK_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（SubTask）未传") # 内容审核
    SUBEVENT_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（SubEvent）未传") # 内容审核
    TASKID_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（TaskId）未传") # 内容审核
    SIGNAL_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Signal）未传") # 实时语音识别
    ROI_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Roi）未传") # 电子围栏
    
    DBNAME_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（DbName）未传") # 数据库
    ENTITY_ID_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（EntityId）未传") # 数据库
    LABELS_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Labels）未传") # 数据库
    OFFSET_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Offset）未传") # 数据库
    EXTRA_DATA_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（ExtraData）未传") # 数据库
    LIMIT_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Limit）未传") # 数据库
    FACE_ID_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（FaceId）未传") # 数据库
    
    INSTRUCTION_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Instruction）未传") # 大模型
    INSTRUCTIONS_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Instructions）未传") # 大模型
    INPUT_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Input）未传") # 大模型
    INPUTS_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Inputs）未传") # 大模型
    MESSAGE_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Message）未传") # 大模型
    MESSAGES_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Messages）未传") # 大模型
    PROMPT_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Prompt）未传") # 大模型
    USER_NAME_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（UserName）未传") # 大模型
    DB_NAME_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（DbName）未传") # 大模型
    FILE_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（File）未传") # 大模型
    FILE_NAME_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（FileName）未传") # 大模型
    FILE_ID_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（FileID）未传") # 大模型
    QA_ID_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（QAID）未传") # 大模型
    QA_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（QA）未传") # 大模型
    QUERY_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Query）未传") # 大模型
    L0_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（L0）未传") # 大模型
    L1_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（L1）未传") # 大模型
    L2_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（L2）未传") # 大模型
    INTENT_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Intent）未传") # 大模型
    EMBEDDING_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Embedding）未传") # 大模型
    DOMAIN_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Domain）未传")  # 大模型
    WRONG_WORD_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（WrongWord）未传") # 纠错黑词

    SOURCES_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（sources）未传") # 建木
    CAMERA_ID_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（camera_id）未传")
    ALGORITHM_MUST_EMPTY_ERR = (400006, "必传的参数未传", "必须的参数（algorithm）未传")
    ALGORITHM_ID_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（algorithm.id）未传")
    CONFIDENCE_MUST_EMPTY_ERR = (400006, "必传的参数未传", "必须的参数（confidence）未传")
    TASK_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（task）未传")

    ScoreThresh_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（ScoreThresh）未传") # 图片帧算法加跟踪
    WarnInterval_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（WarnInterval）未传") 
    IsCollectData_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（IsCollectData）未传")
    CollectThresh_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（CollectThresh）未传")
    Frequency_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Frequency）未传")
    IsLargeModel_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（IsLargeModel）未传")
    SizeThresh_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（SizeThresh）未传")
    AnalysisArea_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（AnalysisArea）未传")
    ShieldedArea_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（ShieldedArea）未传")
    AreaSensitivity_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（AreaSensitivity）未传")
    Duration_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Duration）未传")
    ProportionSensitivity_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（ProportionSensitivity）未传")
    CAMID_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（CamID）未传")

    CALLBACK_URL_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（CallbackUrl）未传")
    AONEID_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（AoneId）未传")
    ROOMID_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（RoomId）未传")
    ISOVER_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（IsOver）未传")

    DETECT_LABELS_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（detect_labels）未传")
    TASK_LISTS_MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Task_Lists）未传")
    

    # 400007 传递非法参数
    ILLEGAL_PRAM_ERR = (400007, "传递非法参数", "请求体字典内有除（Action、ImageData）外的参数")


    # 400008 请求体的字段类型错误
    PRAM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Action、ImageData 字段应该是 string 类型")
    SCREENDETECTINTERVAL_PRAM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ScreenDetectInterval 字段应该是 int 类型")
    IMAGE_AB_PRAM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Action、ImageDataA、ImageDataB 字段应该是 string 类型")
    TEXT_PRAM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Action、TextData 字段应该是 string 类型")
    TEXT_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Text 字段应该是 string 类型")
    AUDIO_PRAM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Action、AudioData 字段应该是 string 类型")
    VIDEO_PRAM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Action、VideoData 字段应该是 string 类型")
    WEBSOCKET_PRAM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Action、Signal 字段应该是 string 类型")
    DEVICE_ID_PRAM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "DeviceID 字段应该是 string 类型") # 设备ID
    STREAM_URL_OR_CALLBACK_URL_PRAM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "StreamURL 和 CallbackURL 字段应该是 string 类型")   # 流语音识别：流请求
    DATA_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "data 字段应该是 string 类型")
    DATA_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "data 字段应该是 list 类型")
    SMALL_DATA_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "data 字段应该是 list 类型")
    IMAGE_CONTENT_STR_TYPE_ERR = (400008, "请求体的参数字段类型错误", "imageContent 字段应该是 string 类型")
    IMG1BASE64_OR_IMG2BASE64_STR_TYPE_ERR = (400008, "请求体的参数字段类型错误", "img1Base64、img2Base64 字段应该是 string 类型")
    
    IMAGE_DATA_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ImageData 字段应该是 string 类型")
    IMAGE_DATA_AB_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ImageDataA、ImageDataB 字段应该是 string 类型")
    IMAGE_DATA_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ImageData 字段应该是 list 类型")
    IMAGE_DATA_LIST_ITEM_STR_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ImageData 字段 list 的成员是 str 类型")
    IMAGE_URL_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ImageURL 字段应该是 string 类型")
    IMAGE_URL_AB_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ImageURLA、ImageURLB 字段应该是 string 类型")
    IMAGE_URL_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ImageURL 字段应该是 list 类型")
    TEXT_DATA_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "TextData 字段应该是 string 类型")
    TEXT_DATA_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "TextData 字段应该是 list 类型")
    TEXT_URL_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "TextURL 字段应该是 string 类型")
    TEXT_URL_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "TextURL 字段应该是 list 类型")
    AUDIO_DATA_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "AudioData 字段应该是 string 类型")
    AUDIO_DATA_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "AudioData 字段应该是 list 类型")
    AUDIO_URL_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "AudioURL 字段应该是 string 类型")
    AUDIO_URL_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "AudioURL 字段应该是 list 类型")
    VIDEO_DATA_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "VideoData 字段应该是 string 类型")
    VIDEO_DATA_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "VideoData 字段应该是 list 类型")
    VIDEO_URL_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "VideoURL 字段应该是 string 类型")
    VIDEO_URL_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "VideoURL 字段应该是 list 类型")
    INPUT_URLS_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "input_url 字段应该是 string 类型")
    INPUT_URLS_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "input_urls 字段应该是 list 类型")
    
    INSTRUCTION_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Instruction 字段应该是 string 类型") # 大模型 string
    INSTRUCTIONS_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Instructions 字段应该是 string 类型")
    INPUT_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Input 字段应该是 string 类型")
    INPUTS_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Inputs 字段应该是 string 类型")
    MESSAGE_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Message 字段应该是 string 类型")
    MESSAGE_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Message 字段应该是 list 类型") # list
    MESSAGES_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Messages 字段应该是 string 类型")
    MESSAGES_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Messages 字段应该是 list 类型") # list
    PROMPT_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Prompt 字段应该是 string 类型")
    USER_NAME_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "UserName 字段应该是 string 类型")
    USER_NAME_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "UserName 字段应该是 list 类型") # list
    DB_NAME_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "DbName 字段应该是 string 类型")
    DB_NAME_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "DbName 字段应该是 list 类型") # list
    FILE_NAME_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "FileName 字段应该是 string 类型")
    FILE_ID_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "FileID 字段应该是 string 类型")
    FILE_ID_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "FileID 字段应该是 int 类型") # int
    FILE_ID_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "FileID 字段应该是 list 类型") # list
    QA_ID_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "QAID 字段应该是 string 类型")
    QA_ID_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "QAID 字段应该是 int 类型") # int
    QA_ID_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "QAID 字段应该是 list 类型") # list
    QA_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "QA 字段应该是 string 类型")
    QA_DICT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "QA 字段应该是 dict 类型") # dict
    QA_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "QA 字段应该是 list 类型") # list
    QUERY_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Query 字段应该是 string 类型")
    L0_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "L0 字段应该是 string 类型")
    L1_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "L1 字段应该是 string 类型")
    L2_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "L2 字段应该是 string 类型")
    INTENT_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Intent 字段应该是 string 类型")
    EMBEDDING_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Embedding 字段应该是 string 类型")
    DOMAIN_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Domain 字段应该是 string 类型")  # 大模型

    CORRECT_WORD_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "CorrectWord 字段应该是 string 类型") # 纠错黑词
    WRONG_WORD_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "WrongWord 字段应该是 string 类型")
    EXCEPTION_WORD_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ExceptionWord 字段应该是 string 类型")
    
    TEMPERATURE_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Temperature 字段应该是 float 类型") # 大模型 float
    TOPP_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "TopP 字段应该是 float 类型")
    REPETITION_PENALTY_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "RepetitionPenalty 字段应该是 float 类型")
    TOPK_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "TopK 字段应该是 int 类型") # 大模型 int
    BEAMS_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Beams 字段应该是 int 类型")
    MAX_TOKENS_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "MaxTokens 字段应该是 int 类型")
    DO_SAMPLE_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "DoSample 字段应该是 bool 类型") # 大模型 bool
    
    VOICE_TYPE_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "VoiceType 字段应该是 int 类型")  # 语音合成
    PITCH_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Pitch 字段应该是 int 类型")  # 语音合成
    SPEED_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Speed 字段应该是 int 类型")  # 语音合成
    VOLUME_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Volume 字段应该是 int 类型")  # 语音合成
    SMOKE_LEVEL_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Level 字段应该是 int 类型")  # 吸烟检测
    MAKEUP_TYPE_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "MakeupType 字段应该是 int 类型")  # 人脸美妆
    MAX_FACE_NUM_TYPE_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "MaxFaceNum 字段应该是 int 类型")  # 人脸检测
    MIN_FACE_SIZE_TYPE_ERR = (400008, "请求体的参数字段类型错误", "MinFaceSize 字段应该是 int 类型")  # 人脸检测
    FREQUENCY_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Frequency 字段应该是 int 类型")  # 视频内容审核
    OFFSET_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Offset 字段应该是 int 类型") # 数据库
    LIMIT_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Limit 字段应该是 int 类型") # 数据库
    ROI_ITEM_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Roi 字段中的两点坐标应该是 int 类型")  # 电子围栏
    
    PITCH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Pitch 字段应该是 float 类型")  # 语音合成
    SPEED_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Speed 字段应该是 float 类型")  # 语音合成
    VOLUME_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Volume 字段应该是 float 类型")  # 语音合成
    SCORE_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ScoreThresh 字段应该是 float 类型")  # 通用分数阈值
    PERSON_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "PersonThresh 字段应该是 float 类型")  # 行人检测
    FACE_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "FaceThresh 字段应该是 float 类型")  # 人脸检测
    FIRE_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "FireThresh 字段应该是 float 类型")  # 烟雾明火检测
    SMOKE_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "SmokeThresh 字段应该是 float 类型")  # 烟雾明火检测
    CAR_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "CarThresh 字段应该是 float 类型")  # 车辆检测
    VEHICLE_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "VehicleThresh 字段应该是 float 类型")  # 车辆检测
    HELMET_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "HelmetThresh 字段应该是 float 类型")  # 安全帽检测
    SUIT_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "SuitThresh 字段应该是 float 类型")  # 防护服检测
    EBIKE_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "EbikeThresh 字段应该是 float 类型")  # 电动车检测
    AREA_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "AreaThresh 字段应该是 float 类型")  # 遮挡检测
    HAND_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "HandThresh 字段应该是 float 类型")  # 手势关键点检测
    STRENGTH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Strength 字段应该是 float 类型")  # 人脸美妆
    MASK_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "MaskThresh 字段应该是 float 类型")  # 口罩检测
    MOUSE_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "MouseThresh 字段应该是 float 类型")  # 老鼠检测
    HAT_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "HatThresh 字段应该是 float 类型")  # 厨师帽检测
    CLOTH_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ClothThresh 字段应该是 float 类型")  # 厨师服检测
    PORN_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "PornThresh 字段应该是 float 类型")  # 内容审核色情
    TERROR_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "TerrorThresh 字段应该是 float 类型")  # 内容审核暴恐
    POLITIC_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "PoliticThresh 字段应该是 float 类型")  # 内容审核政治
    PUBLIC_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "PublicThresh 字段应该是 float 类型")  # 内容审核公众人物
    OCR_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "OCRThresh 字段应该是 float 类型")  # 内容审核OCR
    FALLDOWN_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "FalldownThresh 字段应该是 float 类型")  # 跌倒检测  
    BLOCK_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "BlockThresh 字段应该是 float 类型")  # 内容审核
    REVIEW_THRESH_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ReviewThresh 字段应该是 float 类型")  # 内容审核

    OCR_CAR_NEED_CAR_BOX_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedCarBox 字段应该是 bool 类型")  # 车牌识别
    OCR_CAR_NEED_CAR_ORIEN_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedCarOrien 字段应该是 bool 类型")  # 车牌识别
    OCR_CAR_NEED_PLATE_LANDMARK_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedPlateLandmark 字段应该是 bool 类型")  # 车牌识别
    OCR_CAR_NEED_CAR_TYPE_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedCarType 字段应该是 bool 类型")  # 车辆属性
    OCR_CAR_NEED_CAR_COLOR_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedCarColor 字段应该是 bool 类型")  # 车辆属性
    OCR_CAR_NEED_CAR_BRAND_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedCarBrand 字段应该是 bool 类型")  # 车辆属性
    DETECT_FACE_NEED_FACE_FEATURE_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedFaceFeature 字段应该是 bool 类型")  # 人脸检测
    DETECT_FACE_NEED_FACE_QUALITY_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedFaceQuality 字段应该是 bool 类型")  # 人脸检测
    DETECT_FACE_NEED_FACE_ANGLE_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedFaceAngle 字段应该是 bool 类型")  # 人脸检测
    FACE_COMPARE_DIRECT_COMPARE_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "DirectCompare 字段应该是 bool 类型")  # 人脸比对
    DOUBLELICENSE_OCR_NEED_BACK_PAGE_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedBackPage 字段应该是 bool 类型")  # 驾驶证行驶证
    IS_MONOLINGUAL_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "IsMonolingual 字段应该是 bool 类型")  # 语种分类
    DETECT_PERSON_NEED_BODY_FEATURE_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedBodyFeature 字段应该是 bool 类型")  # 行人检测
    ASR_NEED_PUNCTUATION_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "NeedPunctuation 字段应该是 bool 类型")  # 语音识别
    IS_SPLIT_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "IsSplit 字段应该是 bool 类型")  # 测试 语音识别 是否切割
    SEGMENT_MODEL_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "SegmentModel 字段应该是 bool 类型")  # 测试 语音识别 分割模型
    IS_STRUCT_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "IsStruct 字段应该是 bool 类型")  # 报关单识别 是否结构化
    CONVERT_NUMBER_BOOL_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ConvertNumber 字段应该是 bool 类型")  # 语音识别 逆文本功能
    
    ACTION_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Action 字段应该是 string 类型")
    APPKEY_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "AppKey 字段应该是 string 类型")
    TOKEN_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Token 字段应该是 string 类型")
    VERSION_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Version 字段应该是 string 类型")
    TASKID_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "TaskId 字段应该是 string 类型")  # 内容审核
    
    TIME_STAMP_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "TimeStamp 字段应该是 int 类型") 
    START_TIME_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "StartTime 字段应该是 int 类型") 
    END_TIME_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "EndTime 字段应该是 int 类型") 
    TIME_STAMP_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "TimeStamp 字段应该是 float 类型") 
    START_TIME_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "StartTime 字段应该是 float 类型") 
    END_TIME_FLOAT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "EndTime 字段应该是 float 类型") 
    TIME_STAMP_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "TimeStamp 字段应该是 string 类型") 
    START_TIME_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "StartTime 字段应该是 string 类型") 
    END_TIME_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "EndTime 字段应该是 string 类型") 
    
    SIGNAL_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Signal 字段应该是 string 类型") # 实时语音识别
    LANGUAGE_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Language 字段应该是 string 类型")  # 语音识别
    DBNAME_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "DbName 字段应该是 string 类型") # 数据库
    ENTITY_ID_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "EntityId 字段应该是 string 类型") # 数据库
    LABELS_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Labels 字段应该是 string 类型") # 数据库
    EXTRA_DATA_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ExtraData 字段应该是 string 类型") # 数据库
    FACE_ID_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "FaceId 字段应该是 string 类型") # 数据库
    FACE_ID_INT_TYPE_ERR = (400008, "请求体的参数字段类型错误", "FaceId 字段应该是 int 类型") # 数据库

    INPUTS_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "inputs 字段应该是 list 类型") # 内容审核
    IMG_CENSOR_SUBTASK_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "SubTask 字段应该是 list 类型")  # 内容审核
    SUBEVENT_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "SubEvent 字段应该是 list 类型")  # 内容审核
    ROI_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Roi 字段应该是 list 类型")  # 电子围栏

    SOURCES_TYPE_ERR = (400008, "请求体的参数字段类型错误", "sources 字段应该是 list 类型") # 建木
    CAMERA_ID_TYPE_ERR = (400008, "请求体的参数字段类型错误", "camera_id 字段应该是 string 类型")
    ALGORITHM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "algorithm 字段应该是 dict 类型")
    ALGORITHM_ID_TYPE_ERR = (400008, "请求体的参数字段类型错误", "algorithm.id 字段应该是 string 类型")
    CONFIDENCE_TYPE_ERR = (400008, "请求体的参数字段类型错误", "confidence 字段应该是 float 类型")
    TASK_TYPE_ERR = (400008, "请求体的参数字段类型错误", "task 字段应该是 dict 类型")

    ScoreThresh_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ScoreThresh 字段应该是 dict 类型") # 图片帧加跟踪去重
    WarnInterval_TYPE_ERR = (400008, "请求体的参数字段类型错误", "WarnInterval 字段应该是 int 类型")
    IsCollectData_TYPE_ERR = (400008, "请求体的参数字段类型错误", "IsCollectData 字段应该是 int 类型")
    CollectThresh_TYPE_ERR = (400008, "请求体的参数字段类型错误", "CollectThresh 字段应该是 float 类型")
    Frequency_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Frequency 字段应该是 float 类型")
    IsLargeModel_TYPE_ERR = (400008, "请求体的参数字段类型错误", "IsLargeModel 字段应该是 int 类型")
    SizeThresh_TYPE_ERR = (400008, "请求体的参数字段类型错误", "SizeThresh 字段应该是 dict 类型")
    AnalysisArea_TYPE_ERR = (400008, "请求体的参数字段类型错误", "AnalysisArea 字段应该是 list 类型")
    ShieldedArea_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ShieldedArea 字段应该是 list 类型")
    AreaSensitivity_TYPE_ERR = (400008, "请求体的参数字段类型错误", "AreaSensitivity 字段应该是 int 类型")
    Duration_TYPE_ERR = (400008, "请求体的参数字段类型错误", "Duration 字段应该是 int 类型")
    ProportionSensitivity_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ProportionSensitivity 字段应该是 int 类型")
    CAMID_TYPE_ERR = (400008, "请求体的参数字段类型错误", "CamID 字段应该是 string 类型")
    ScoreThreshLM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ScoreThreshLM 字段应该是 dict 类型")
    IouThreshLM_TYPE_ERR = (400008, "请求体的参数字段类型错误", "IouThreshLM 字段应该是 float 类型")

    CALLBACK_URL_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "CallbackUrl 字段应该是 string 类型")
    AONEID_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "AoneId 字段应该是 string 类型")
    ROOMID_STRING_TYPE_ERR = (400008, "请求体的参数字段类型错误", "RoomId 字段应该是 string 类型")
    ISOVER_BOOL_TYPE_ER = (400008, "请求体的参数字段类型错误", "IsOver 字段应该是 bool 类型")

    DETECT_LABELS_LIST_TYPE_ERR =  (400008, "请求体的参数字段类型错误", "detect_labels 字段应该是 list 类型")
    TASK_LISTS_TYPE_ERR =  (400008, "请求体的参数字段类型错误", "Task_List 字段应该是 list 类型")
    SCORE_THRESH_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "ScoreThresh 字段应该是 list 类型")  # 通用分数阈值
    IOU_THRESH_LIST_TYPE_ERR = (400008, "请求体的参数字段类型错误", "IouThresh 字段应该是 list 类型")  # 通用分数阈值


    # 400009 请求体的参数字段值为空
    IMAGE_DATA_AND_ACTION_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Action、ImageData 字段值为空字符")
    IMAGE_DATA_EMPTY_ERR = (400009, "请求体的参数字段值为空", "ImageData 字段值为空字符")
    IMAGE_DATA_LIST_EMPTY_ERR = (400009, "请求体的参数字段值为空", "ImageData 列表为空")
    IMAGE_AB_DATA_EMPTY_ERR = (400009, "请求体的参数字段值为空", "ImageDataA、ImageDataB 字段值为空字符")
    TEXT_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Text 字段值为空字符")
    TEXT_DATA_EMPTY_ERR = (400009, "请求体的参数字段值为空", "TextData 字段值为空字符")
    AUDIO_DATA_EMPTY_ERR = (400009, "请求体的参数字段值为空", "AudioData 字段值为空字符")
    VIDEO_DATA_EMPTY_ERR = (400009, "请求体的参数字段值为空", "VideoData 字段值为空字符")
    IMAGE_URL_EMPTY_ERR = (400009, "请求体的参数字段值为空", "ImageURL 字段值为空字符")
    IMAGE_URL_AB_EMPTY_ERR = (400009, "请求体的参数字段值为空", "ImageURLA、ImageURLB 字段值为空字符")
    TEXT_URL_EMPTY_ERR = (400009, "请求体的参数字段值为空", "TextURL 字段值为空字符")
    AUDIO_URL_EMPTY_ERR = (400009, "请求体的参数字段值为空", "AudioURL 字段值为空字符")
    VIDEO_URL_EMPTY_ERR = (400009, "请求体的参数字段值为空", "VideoURL 字段值为空字符")
    DATA_EMPTY_ERR = (400009, "请求体的参数字段值为空", "data 字段值为空")
    SMALL_DATA_LIST_EMPTY_ERR = (400009, "请求体的参数字段值为空", "data 列表为空")
    IMAGE_CONTENT_EMPTY_ERR = (400009, "请求体的参数字段值为空", "imageContent 字段值为空字符")
    IMG1BASE64_OR_IMG2BASE64_EMPTY_ERR = (400009, "请求体的参数字段值为空", "img1Base64 或 img2Base64 字段值为空字符")
    
    IMAGE_URL_LIST_EMPTY_ERR = (400009, "请求体的参数字段值为空", "ImageURL 列表为空")
    TEXT_URL_LIST_EMPTY_ERR = (400009, "请求体的参数字段值为空", "TextURL 列表为空")
    AUDIO_URL_LIST_EMPTY_ERR = (400009, "请求体的参数字段值为空", "AudioURL 列表为空")
    VIDEO_URL_LIST_EMPTY_ERR = (400009, "请求体的参数字段值为空", "VideoURL 列表为空")
    INPUTS_LIST_EMPTY_ERR = (400009, "请求体的参数字段值为空", "inputs 列表为空")
    INPUT_URLS_EMPTY_ERR = (400009, "请求体的参数字段值为空", "input_urls 列表为空")
    
    ACTION_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Action 字段值为空字符")
    APPKEY_EMPTY_ERR = (400009, "请求体的参数字段值为空", "AppKey 字段值为空字符")
    TOKEN_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Token 字段值为空字符")
    VERSION_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Version 字段值为空字符")
    TASKID_EMPTY_ERR = (400009, "请求体的参数字段值为空", "TaskId 字段值为空字符") # 内容审核
    WEBSOCKET_DATA_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Signal 字段值为空字符") # 实时语音识别 
    DBNAME_EMPTY_ERR = (400009, "请求体的参数字段值为空", "DbName 字段值为空字符") # 数据库
    ENTITY_ID_EMPTY_ERR = (400009, "请求体的参数字段值为空", "EntityId 字段值为空字符") # 数据库
    LABELS_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Labels 字段值为空字符") # 数据库
    EXTRA_DATA_EMPTY_ERR = (400009, "请求体的参数字段值为空", "ExtraData 字段值为空字符") # 数据库
    FACE_ID_EMPTY_ERR = (400009, "请求体的参数字段值为空", "FaceId 字段值为空字符") # 数据库
    DEVICE_ID_EMPTY_ERR = (400009, "请求体的参数字段值为空", "DeviceID 字段值为空字符") # 设备ID
    STREAM_URL_OR_CALLBACK_URL_EMPTY_ERR = (400009, "请求体的参数字段值为空", "StreamURL 和 CallbackURL 字段为空字符")   # 流语音识别：流请求
    
    INSTRUCTION_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Instruction 字段值为空字符") # 大模型
    INSTRUCTIONS_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Instructions 字段值为空字符") 
    INPUT_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Input 字段值为空字符") 
    INPUTS_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Inputs 字段值为空字符") 
    MESSAGE_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Message 字段值为空字符") 
    MESSAGES_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Messages 字段值为空字符") 
    MESSAGE_LIST_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Message 列表为空")  # list
    MESSAGES_LIST_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Messages 列表为空")  # list
    PROMPT_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Prompt 字段值为空字符") 
    USER_NAME_EMPTY_ERR = (400009, "请求体的参数字段值为空", "UserName 字段值为空字符") 
    DB_NAME_EMPTY_ERR = (400009, "请求体的参数字段值为空", "DbName 字段值为空字符") 
    FILE_EMPTY_ERR = (400009, "请求体的参数字段值为空", "File 字段内容为空") 
    FILE_NAME_EMPTY_ERR = (400009, "请求体的参数字段值为空", "FileName 字段内容为空") 
    FILE_ID_EMPTY_ERR = (400009, "请求体的参数字段值为空", "FileID 字段内容为空") 
    QA_ID_EMPTY_ERR = (400009, "请求体的参数字段值为空", "QAID 字段内容为空") 
    QA_EMPTY_ERR = (400009, "请求体的参数字段值为空", "QA 字段内容为空") 
    QUERY_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Query 字段内容为空") 
    L0_EMPTY_ERR = (400009, "请求体的参数字段值为空", "L0 字段内容为空") 
    L1_EMPTY_ERR = (400009, "请求体的参数字段值为空", "L1 字段内容为空") 
    L2_EMPTY_ERR = (400009, "请求体的参数字段值为空", "L2 字段内容为空") 
    INTENT_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Intent 字段内容为空") 
    EMBEDDING_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Embedding 字段内容为空") 
    DOMAIN_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Domain 字段为空字符")
    WRONG_WORD_EMPTY_ERR = (400009, "请求体的参数字段值为空", "WrongWord 字段值为空") # 纠错黑词
    
    IMG_CENSOR_SUBTASK_EMPTY_ERR = (400009, "请求体的参数字段值为空", "SubTask 列表为空") # 内容审核
    SUBEVENT_EMPTY_ERR = (400009, "请求体的参数字段值为空", "SubEvent 列表为空") # 内容审核
    ROI_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Roi 列表为空") # 电子围栏

    SOURCES_EMPTY_ERR = (400009, "请求体的参数字段值为空", "sources 字段值为空") # 建木
    CAMERA_ID_EMPTY_ERR = (400009, "请求体的参数字段值为空", "camera_id 字段值为空")
    ALGORITHM_ID_EMPTY_ERR = (400009, "请求体的参数字段值为空", "algorithm.id 字段值为空")
    
    ScoreThresh_EMPTY_ERR = (400009, "请求体的参数字段值为空", "ScoreThresh 字段值为空") # 图片帧加跟踪
    SizeThresh_EMPTY_ERR = (400009, "请求体的参数字段值为空", "SizeThresh 字段值为空")
    AnalysisArea_EMPTY_ERR = (400009, "请求体的参数字段值为空", "AnalysisArea 字段值为空")
    CAMID_EMPTY_ERR = (400009, "请求体的参数字段值为空", "CamID 字段值为空字符")

    CALLBACK_URL_EMPTY_ERR = (400009, "请求体的参数字段值为空", "CallbackUrl 字段值为空")
    AONEID_EMPTY_ERR = (400009, "请求体的参数字段值为空", "AoneId 字段值为空")
    ROOMID_EMPTY_ERR = (400009, "请求体的参数字段值为空", "RoomId 字段值为空")

    DETECT_LABELS_EMPTY_ERR = (400009, "请求体的参数字段值为空", "detect_labels 字段值为空")
    TASK_LISTS_EMPTY_ERR = (400009, "请求体的参数字段值为空", "Task_Lists 字段值为空")
    IOU_THRESH_EMPTY_ERR = (400009, "请求体的参数字段值为空", "IouThresh 字段值为空")

    # 400010 请求体的参数字段值设置错误
    ACTION_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Action 值设置错误")  # ACTION
    IMAGE_DATA_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "ImageData 字段不符合规范，请参考接口文档说明")
    TEXT_DATA_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "TextData 字段不符合规范，请参考接口文档说明")
    AUDIO_DATA_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "AudioData 字段不符合规范，请参考接口文档说明")
    VIDEO_DATA_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "VideoData 字段不符合规范，请参考接口文档说明")
    IMAGE_URL_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "ImageURL 字段不符合规范，请参考接口文档说明")
    TEXT_URL_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "TextURL 字段不符合规范，请参考接口文档说明")
    AUDIO_URL_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "AudioURL 字段不符合规范，请参考接口文档说明")
    VIDEO_URL_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "VideoURL 字段不符合规范，请参考接口文档说明")
    INPUT_URLS_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "input_urls 字段不符合规范，请参考接口文档说明")
    INPUTS_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "inputs 字段不符合规范，请参考接口文档说明")
    
    APPKEY_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "AppKey 字段不符合规范，请参考接口文档说明")
    TOKEN_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Token 字段不符合规范，请参考接口文档说明")
    VERSION_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Version 字段不符合规范，请参考接口文档说明")
    SIGNAL_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Signal 字段不符合规范，请参考接口文档说明")
    DEVICE_ID_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "DeviceID 字段不符合规范，请参考接口文档说明") # 设备ID
    
    MESSAGES_ITEM_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Messages 字段不符合规范，请参考接口文档说明") # 大模型
    ROLE_USER_ASSISTANT_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "输入中的 role 字段只能为 user 或 assistant") # 大模型
    TEMPERATURE_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Temperature 字段不符合规范，请参考接口文档说明") 
    TOPP_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "TopP 字段不符合规范，请参考接口文档说明") 
    TOPK_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "TopK 字段不符合规范，请参考接口文档说明") 
    BEAMS_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Beams 字段不符合规范，请参考接口文档说明") 
    REPETITION_PENALTY_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "RepetitionPenalty 字段不符合规范，请参考接口文档说明") 
    MAX_TOKENS_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "MaxTokens 字段不符合规范，请参考接口文档说明") 
    DOMAIN_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Domain 字段不符合规范，请参考接口文档说明")
    QA_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "QA 字段不符合规范，请参考接口文档说明")
    
    VOICE_TYPE_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "VoiceType 字段不符合规范，请参考接口文档说明")  # 语音合成
    PITCH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Pitch 字段不符合规范，请参考接口文档说明")  # 语音合成
    SPEED_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Speed 字段不符合规范，请参考接口文档说明")  # 语音合成
    VOLUME_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Volume 字段不符合规范，请参考接口文档说明")  # 语音合成
    STRENGTH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Strength 字段不符合规范，请参考接口文档说明")  # 人脸美妆
    SMOKE_LEVEL_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Level 字段不符合规范，请参考接口文档说明")  # 吸烟检测
    IMG_CENSOR_SUBTASK_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "SubTask 字段不符合规范，请参考接口文档说明")  # 内容审核
    SUBEVENT_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "SubEvent 字段不符合规范，请参考接口文档说明")  # 视频内容审核
    FREQUENCY_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Frequency 字段不符合规范，请参考接口文档说明")  # 视频内容审核
    LANGUAGE_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Language 字段不符合规范，请参考接口文档说明")  # 语音识别
    IS_MONOLINGUAL_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "IsMonolingual 字段不符合规范，请参考接口文档说明")  # 语种分类
    MAX_FACE_NUM_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "MaxFaceNum 字段不符合规范，请参考接口文档说明")  # 人脸检测
    MIN_FACE_SIZE_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "MinFaceSize 字段不符合规范，请参考接口文档说明")  # 人脸检测
    ROI_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Roi 字段不符合规范，请参考接口文档说明")  # 电子围栏

    SCORE_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "ScoreThresh 字段不符合规范，请参考接口文档说明")  # 通用分数阈值
    PERSON_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "PersonThresh 字段不符合规范，请参考接口文档说明")  # 行人检测
    FACE_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "FaceThresh 字段不符合规范，请参考接口文档说明")  # 人脸检测
    FIRE_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "FireThresh 字段不符合规范，请参考接口文档说明")  # 烟雾明火检测
    SMOKE_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "SmokeThresh 字段不符合规范，请参考接口文档说明")  # 烟雾明火检测
    CAR_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "CarThresh 字段不符合规范，请参考接口文档说明")  # 车辆检测
    VEHICLE_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "VehicleThresh 字段不符合规范，请参考接口文档说明")  # 车辆检测
    HELMET_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "HelmetThresh 字段不符合规范，请参考接口文档说明")  # 安全帽检测
    SUIT_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "SuitThresh 字段不符合规范，请参考接口文档说明")  # 防护服检测
    EBIKE_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "EbikeThresh 字段不符合规范，请参考接口文档说明")  # 电动车检测
    AREA_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "AreaThresh 字段不符合规范，请参考接口文档说明")  # 遮挡检测
    HAND_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "HandThresh 字段不符合规范，请参考接口文档说明")  # 手势关键点检测
    MAKEUP_TYPE_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "MakeupType 字段不符合规范，请参考接口文档说明")  # 人脸美妆
    MASK_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "MaskThresh 字段不符合规范，请参考接口文档说明")  # 口罩检测
    MOUSE_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "MouseThresh 字段不符合规范，请参考接口文档说明")  # 老鼠检测
    HAT_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "HatThresh 字段不符合规范，请参考接口文档说明")  # 厨师帽检测
    CLOTH_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "ClothThresh 字段不符合规范，请参考接口文档说明")  # 厨师服检测
    PORN_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "PornThresh 字段不符合规范，请参考接口文档说明")  # 内容审核色情
    TERROR_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "TerrorThresh 字段不符合规范，请参考接口文档说明")  # 内容审核暴恐
    POLITIC_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "PoliticThresh 字段不符合规范，请参考接口文档说明")  # 内容审核政治
    PUBLIC_THRESH_VALUE_ERR = (400010, "请求体的参数字段类型错误", "PublicThresh 字段不符合规范，请参考接口文档说明")  # 内容审核公众人物
    OCR_THRESH_VALUE_ERR = (400010, "请求体的参数字段类型错误", "OCRThresh 字段不符合规范，请参考接口文档说明")  # 内容审核OCR
    FALLDOWN_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "FalldownThresh 字段不符合规范，请参考接口文档说明")  # 跌倒检测     
    BLOCK_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "BlockThresh 字段不符合规范，请参考接口文档说明") # 内容审核
    REVIEW_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "ReviewThresh 字段不符合规范，请参考接口文档说明")  # 内容审核

    DBNAME_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "DbName 字段不符合规范，请参考接口文档说明") # 数据库
    ENTITY_ID_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "EntityId 字段不符合规范，请参考接口文档说明") # 数据库
    LABELS_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Labels 字段不符合规范，请参考接口文档说明") # 数据库
    OFFSET_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Offset 字段不符合规范，请参考接口文档说明") # 数据库
    EXTRA_DATA_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "ExtraData 字段不符合规范，请参考接口文档说明") # 数据库
    LIMIT_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Limit 字段不符合规范，请参考接口文档说明") # 数据库
    FACE_ID_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "FaceId 字段不符合规范，请参考接口文档说明") # 数据库

    CONFIDENCE_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "confidence 字段不符合规范，请参考接口文档说明") # 建木

    ScoreThresh_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "ScoreThresh 字段不符合规范，请参考接口文档说明") # 图片帧加跟踪
    WarnInterval_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "WarnInterval 字段不符合规范，请参考接口文档说明")
    IsCollectData_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "IsCollectData 字段不符合规范，请参考接口文档说明")
    CollectThresh_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "CollectThresh 字段不符合规范，请参考接口文档说明")
    Frequency_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Frequency 字段不符合规范，请参考接口文档说明")
    IsLargeModel_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "IsLargeModel 字段不符合规范，请参考接口文档说明")
    SizeThresh_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "SizeThresh 字段不符合规范，请参考接口文档说明")
    AnalysisArea_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "AnalysisArea 字段不符合规范，请参考接口文档说明")
    ShieldedArea_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "ShieldedArea 字段不符合规范，请参考接口文档说明")
    AreaSensitivity_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "AreaSensitivity 字段不符合规范，请参考接口文档说明")
    Duration_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Duration 字段不符合规范，请参考接口文档说明")
    ProportionSensitivity_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "ProportionSensitivity 字段不符合规范，请参考接口文档说明")
    ScoreThreshLM_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "ScoreThreshLM 字段不符合规范，请参考接口文档说明")
    IouThreshLM_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "IouThreshLM 字段不符合规范，请参考接口文档说明")
    ACTION_new_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Action 字段不符合规范，请参考接口文档说明")

    DETECT_LABELS_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "detect_labels 字段不符合规范，请参考接口文档说明")
    TASK_LISTS_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "Task_Lists 字段不符合规范，请参考接口文档说明")
    IOU_THRESH_VALUE_ERR = (400010, "请求体的参数字段值设置错误", "IouThresh 字段不符合规范，请参考接口文档说明")

    # 400011 base64 数据处理异常
    IMAGE_DATA_BASE64_ERR = (400011, "base64 数据处理异常", "ImageData 字段的 base64 字符串转换字节码异常")
    IMAGE_AB_DATA_BASE64_ERR = (400011, "base64 数据处理异常", "ImageDataA 或 ImageDataB 字段的 base64 字符串转换字节码异常")
    TEXT_DATA_BASE64_ERR = (400011, "base64 数据处理异常", "TextData 字段的 base64 字符串转换字节码异常")
    AUDIO_DATA_BASE64_ERR = (400011, "base64 数据处理异常", "AudioData 字段的 base64 字符串转换字节码异常")
    VIDEO_DATA_BASE64_ERR = (400011, "base64 数据处理异常", "VideoData 字段的 base64 字符串转换字节码异常")
    INPUTS_BASE64_ERR = (400011, "base64 数据处理异常", "inputs 字段的 base64 字符串转换字节码异常")
    SMALL_DATA_BASE64_ERR = (400011, "base64 数据处理异常", "data 字段的 base64 字符串转换字节码异常")
    IMAGE_CONTENT_BASE64_ERR = (400011, "base64 数据处理异常", "imageContent 字段的 base64 字符串转换字节码异常")
    IMG1BASE64_OR_IMG2BASE64_BASE64_ERR = (400011, "base64 数据处理异常", "img1Base64 或 img2Base64 字段的 base64 字符串转换字节码异常")
    
    # 400012 文件格式不合法
    IMAGE_TYPE_ERR = (400012, "文件格式不合法", "仅支持 jpeg/png/jpg/bmp 格式")
    IMAGE_TYPE_WEBP_ERR = (400012, "文件格式不合法", "仅支持 jpeg/png/jpg/bmp/webp 格式")
    IMAGE_TYPE_GIF_ERR = (400012, "文件格式不合法", "仅支持 jpeg/png/jpg/bmp/gif 格式")
    IMAGE_TYPE_TIFF_ERR = (400012, "文件格式不合法", "仅支持 jpeg/png/jpg/bmp/tiff 格式")
    IMAGE_TYPE_WEBP_GIF_TIFF_ERR = (400012, "文件格式不合法", "仅支持 jpeg/png/jpg/bmp/webp/tiff/gif 格式")
    IMAGE_TYPE_DOC_ERR = (400012, "文件格式不合法", "支持的图片格式请参考接口文档说明")

    AUDIO_TYPE_ERR = (400012, "文件格式不合法", "仅支持 pcm/wav 格式")
    AUDIO_TYPE_FLAC_ERR = (400012, "文件格式不合法", "仅支持 pcm/wav/flac 格式")
    AUDIO_TYPE_FLAC_MP3_ERR = (400012, "文件格式不合法", "仅支持 pcm/wav/flac/mp3 格式")
    AUDIO_TYPE_DOC_ERR = (400012, "文件格式不合法", "支持的音频格式请参考接口文档说明")

    VIDEO_TYPE_ERR = (400012, "文件格式不合法", "仅支持 mp4 格式")
    VIDEO_TYPE_DOC_ERR = (400012, "文件格式不合法", "支持的视频格式请参考接口文档说明")

    FILE_TYPE_DOC_ERR = (400012, "文件格式不合法", "支持的文件格式请参考接口文档说明")


    # 400013 文件大小不符合要求
    IMAGE_SIZE_ERR = (400013, "文件大小不符合要求", "该文件大小不符合要求，图片要求小于 7M")
    IMAGE_SIZE_DOC_ERR = (400013, "文件大小不符合要求", "该文件大小不符合要求，请参考接口文档说明")
    IMAGE_2_SIZE_ERR = (400013, "文件大小不符合要求", "该文件大小不符合要求，图片要求小于 2M")
    IMAGE1_2_SIZE_ERR = (400013, "文件大小不符合要求", "该文件大小不符合要求，图片一要求小于 2M")
    IMAGE2_2_SIZE_ERR = (400013, "文件大小不符合要求", "该文件大小不符合要求，图片二要求小于 2M")
    IMAGE_10_SIZE_ERR = (400013, "文件大小不符合要求", "该文件大小不符合要求，图片要求小于 10M")
    
    TEXT_SIZE_ERR = (400013, "文件大小不符合要求", "该文件大小不符合要求，文本要求小于 7M")
    TEXT_SIZE_DOC_ERR = (400013, "文件大小不符合要求", "该文件大小不符合要求，请参考接口文档说明")

    AUDIO_SIZE_ERR = (400013, "文件大小不符合要求", "该文件大小不符合要求，音频要求小于 7M")
    AUDIO_SIZE_DOC_ERR = (400013, "文件大小不符合要求", "该文件大小不符合要求，请参考接口文档说明")
    
    VIDEO_SIZE_ERR = (400013, "文件大小不符合要求", "该文件大小不符合要求，视频要求小于 7M")
    VIDEO_SIZE_DOC_ERR = (400013, "文件大小不符合要求", "该视频大小不符合要求，请参考接口文档说明")


    # 4000014 请求时间范围不合法
    TIME_RANGE_ERR = (400014, "请求时间范围不合法", "请求时间范围不合法")
    TIME_RANGE_START_AND_END_ERR = (400014, "请求时间范围不合法", "请求时间范围不合法，StartTime 应该小于 EndTime")


    # 4000015 文件下载错误
    IMAGE_URL_DOWNLOAD_ERR = (400015, "文件下载错误", "无法解析图片链接，下载失败")
    IMAGE_URL_A_DOWNLOAD_ERR = (400015, "文件下载错误", "无法解析 ImageURLA 图片链接，下载失败")
    IMAGE_URL_B_DOWNLOAD_ERR = (400015, "文件下载错误", "无法解析 ImageURLB 图片链接，下载失败")
    TEXT_URL_DOWNLOAD_ERR = (400015, "文件下载错误", "无法解析文本链接，下载失败")
    AUDIO_URL_DOWNLOAD_ERR = (400015, "文件下载错误", "无法解析音频链接，下载失败")
    VIDEO_URL_DOWNLOAD_ERR = (400015, "文件下载错误", "无法解析视频链接，下载失败")
    FILE_URLS_DOWNLOAD_ERR = (400015, "文件下载错误", "无法解析文件链接，下载失败")


    # 4000016 必传的参数重复
    INPUTS_AND_URLS_DUPLI_PRAM_ERR = (400016, "必传的参数重复", "必须的参数（inputs 或 input_urls）只能二选一")
    IMAGE_DATA_AND_IMAGE_URL_DUPLI_PRAM_ERR = (400016, "必传的参数重复", "必须的参数（ImageData 或 ImageURL）只能二选一")
    IMAGE_DATA_AB_AND_IMAGE_URL_AB_DUPLI_PRAM_ERR = (400016, "必传的参数重复", "必须的参数（ImageDataA、ImageDataB 或 ImageURLA、ImageURLB）只能二选一")
    TEXT_DATA_AND_TEXT_URL_DUPLI_PRAM_ERR = (400016, "必传的参数重复", "必须的参数（TextData 或 TextURL）只能二选一")
    AUDIO_DATA_AND_AUDIO_URL_DUPLI_PRAM_ERR = (400016, "必传的参数重复", "必须的参数（AudioData 或 AudioURL）只能二选一")
    VIDEO_DATA_AND_VIDEO_URL_DUPLI_PRAM_ERR = (400016, "必传的参数重复", "必须的参数（VideoData 或 VideoURL）只能二选一")


    # 4000017 时间戳格式不对
    TIME_STAMP_FORMAT_ERR = (400017, "时间戳格式不对", "TimeStamp 应该是 10 位时间戳格式，单位为秒")
    START_TIME_FORMAT_ERR = (400017, "时间戳格式不对", "StartTime 应该是 10 位时间戳格式，单位为秒")
    END_TIME_FORMAT_ERR = (400017, "时间戳格式不对", "EndTime 应该是 10 位时间戳格式，单位为秒") 

    TIME_STAMP_FORMAT_MS_ERR = (400017, "时间戳格式不对", "TimeStamp 应该是 13 位时间戳格式，单位为毫秒")
    START_TIME_FORMAT_MS_ERR = (400017, "时间戳格式不对", "StartTime 应该是 13 位时间戳格式，单位为毫秒") 
    END_TIME_FORMAT_MS_ERR = (400017, "时间戳格式不对", "EndTime 应该是 13 位时间戳格式，单位为毫秒") 


    # 4000018 超过个数限制
    OVER_LIMIT_5_ERR = (400018, "超过个数限制", "超过个数限制，最多传 5 张图片")
    
    IMAGE_DATA_OVER_LIMIT_8_ERR = (400018, "超过个数限制", "ImageData 超过个数限制，最多传 8 张图片")
    IMAGE_DATA_OVER_LIMIT_16_ERR = (400018, "超过个数限制", "ImageData 超过个数限制，最多传 16 张图片")
    IMAGE_DATA_OVER_LIMIT_DOC_ERR = (400018, "超过个数限制", "ImageData 超过个数限制，请参考接口文档说明")
    IMAGE_URL_OVER_LIMIT_8_ERR = (400018, "超过个数限制", "ImageURL 超过个数限制，最多传 8 张图片")
    IMAGE_URL_OVER_LIMIT_16_ERR = (400018, "超过个数限制", "ImageURL 超过个数限制，最多传 16 张图片")
    IMAGE_URL_OVER_LIMIT_DOC_ERR = (400018, "超过个数限制", "ImageURL 超过个数限制，请参考接口文档说明")
 
    SMALL_DATA_OVER_LIMIT_50_ERR = (400018, "超过个数限制", "data 超过个数限制，最多传 50 张图片")
 
    TEXT_DATA_OVER_LIMIT_DOC_ERR = (400018, "超过个数限制", "TextData 超过个数限制，请参考接口文档说明")
    TEXT_URL_OVER_LIMIT_DOC_ERR = (400018, "超过个数限制", "TextURL 超过个数限制，请参考接口文档说明")

    AUDIO_DATA_OVER_LIMIT_DOC_ERR = (400018, "超过个数限制", "AudioData 超过个数限制，请参考接口文档说明")
    AUDIO_URL_OVER_LIMIT_DOC_ERR = (400018, "超过个数限制", "AudioURL 超过个数限制，请参考接口文档说明")

    VIDEO_DATA_OVER_LIMIT_DOC_ERR = (400018, "超过个数限制", "VideoData 超过个数限制，请参考接口文档说明")
    VIDEO_URL_OVER_LIMIT_DOC_ERR = (400018, "超过个数限制", "VideoURL 超过个数限制，请参考接口文档说明")

    
    # 400019 请求体的参数字段长度错误
    ROI_LENGTH_ERR = (400019, "请求体的参数字段长度错误", "Roi 字段长度必须大于 3 或者小于 10") # 电子围栏
    
    # 400020 上传文件失败
    UPLOAD_ERR = (400020, "上传文件失败", "上传文件失败") 
    UPLOAD_FILE_NAME_ERR = (400020, "上传文件失败", "获取文件名失败") 
    UPLOAD_FILE_CONTENT_ERR = (400020, "上传文件失败", "获取文件内容失败") 
    UPLOAD_GBK_ERR = (400020, "上传文件失败", "gbk 转换 utf8 格式失败") 
    UPLOAD_LOAD_ERR = (400020, "上传文件失败", "文件上传解析失败") 
    UPLOAD_PATH_ERR = (400020, "上传文件失败", "上传文件路径不存在") 
    
    # 400021 URL 出错
    URL_CONNECT_ERR = (400021, "URL 出错", "URL 访问出错，请检查 URL 或网络状态") # URL 通用错误
    STREAM_TIMEOUT_ERR = (400021, "URL 出错", "流访问超时，请检查网络状态")  # 流语音识别：流请求
    STREAM_ADDRESS_ERR = (400021, "URL 出错", "流访问出错，请检查流地址")  # 流语音识别：流请求
    
    ### 图片 41xxxxx ###

    # 410001 图片解码错误
    IMAGE_DECODE_ERR = (410001, "图片解码错误", "字节码解码为图片错误")
    IMAGE1_DECODE_ERR = (410001, "图片一解码错误", "字节码解码为图片错误")
    IMAGE2_DECODE_ERR = (410001, "图片二解码错误", "字节码解码为图片错误")

    # 410002 图片尺寸不符合要求
    IMAGE_SHAPE_ERR = (410002, "图片尺寸不符合要求", "分辨率长宽尺寸应不高于 5000 不低于 32")
    IMAGE_SHAPE_6000_ERR = (410002, "图片尺寸不符合要求", "分辨率长宽尺寸应不高于 6000 不低于 32")
    IMAGE_SHAPE_DOC_ERR = (410002, "图片尺寸不符合要求", "图片尺寸不符合要求，请参考接口文档说明")



    ### 文本 42xxxxx ###

    # 420001 文本长度超过限制
    TEXT_TOO_LONG_ERR = (420001, "文本长度超过限制", "文本输入过长，请参考接口文档说明")

    # 420002 文本长度低于阈值
    TEXT_TOO_SHORT_ERR = (420002, "文本长度低于阈值", "文本输入过短，请参考接口文档说明")

    # 420003 中文占比过低
    TEXT_CHINESE_TOO_LOW_ERR = (
        420003, "中文占比过低", "文本中的中文（仅包含汉字，不包含任何数字、符号）占比不低于 50%")

    # 420004 文本不是 UTF8 格式
    TEXT_NOT_UTF8_ERR = (420004, "文本不是 UTF8 格式", "文本不是 UTF8 格式")

    # 420005 文本含有非法字符
    TEXT_ILLEGAL_ERR = (420005, "文本含有非法字符", "文本含有非法字符")
    
    # 420006 文本操作失败
    WRONG_WORD_EXISTS = (420006, "文本上传失败", "错误词已存在")
    EXCEPTION_WORD_NOT_EXIST = (420006, "文本上传失败", "例外语境必须包含至少一个错误词")
    WRONG_WORD_NOT_EXIST = (420006, "文本修改失败", "错误词不存在")

    ### 音频 43xxxxx

    # 430001 音频解码错误
    AUDIO_DECODE_ERR = (430001, "音频解码错误", "字节码解码为音频解错误")


    # 430002 音频采样率不符合要求
    AUDIO_SAMPLE_RATE_ERR = (430002, "音频采样率不符合要求", "音频采样率应该为 16k")
    AUDIO_SAMPLE_RATE_DOC_ERR = (430002, "音频采样率不符合要求", "音频采样率不符合要求，请参考接口文档说明")


    # 430003 音频采样精度不符合要求
    AUDIO_SAMPLE_ACCURACY_ERR = (430003, "音频采样精度不符合要求", "音频采样精度应该为 16bit")
    AUDIO_SAMPLE_ACCURACY_DOC_ERR = (430003, "音频采样精度不符合要求", "音频采样精度不符合要求，请参考接口文档说明")


    # 430004 音频声道数不符合要求
    AUDIO_CHANNEL_ERR = (430004, "音频声道数不符合要求", "音频应该为单声道")
    AUDIO_CHANNEL_DOC_ERR = (430004, "音频声道数不符合要求", "音频声道数不符合要求，请参考接口文档说明")


    # 430005 音频长度不符合要求
    AUDIO_LENGTH_60s_ERR = (430005, "音频长度不符合要求", "音频长度过长，音频应该限制在 60s 内")
    AUDIO_LENGTH_120s_ERR = (430005, "音频长度不符合要求", "音频长度过长，音频应该限制在 120s 内")
    AUDIO_LENGTH_ERR = (430005, "音频长度不符合要求", "音频长度过长，请参考接口文档说明")

    ### 视频 44xxxxx

    # 440001 视频解码错误
    VIDEO_DECODE_ERR = (440001, "视频解码错误", "字节码解码为视频解错误")

    # 440002 视频长度不符合要求
    VIDEO_LENGTH_ERR = (440002, "视频长度不符合要求", "视频长度过长，请参考接口文档说明")
    VIDEO_LENGTH_TOO_SHORT_ERR = (440002, "视频长度不符合要求", "视频长度过短，请参考接口文档说明")

    # 440003 视频尺寸不符合要求
    VIDEO_SHAPE_ERR = (440003, "视频尺寸不符合要求", "分辨率长宽尺寸应不高于 5000 不低于 32")
    VIDEO_SHAPE_DOC_ERR = (440003, "视频尺寸不符合要求", "视频尺寸不符合要求，请参考接口文档说明")
    
    ### 数据库 45xxxxx ###

    # 450001 数据库操作失败
    DB_OPERATE_ERR = (450001, "数据库操作失败", "数据库操作失败")
    DB_OPERATE_CONNECT_ERR = (450001, "数据库操作失败", "数据库连接失败，请重试")
    DB_OPERATE_MILVUS_CONNECT_ERR = (450001, "数据库操作失败", "向量数据库连接失败，请重试")

    DB_OVER_DB_MAX_COUNT_ERR = (450001, "数据库操作失败", "达到数据库最大限制")
    DB_CREATE_FACE_DB_ERR = (450001, "数据库操作失败", "创建人脸数据库失败")
    DB_CREATE_FACE_MILVUS_ERR = (450001, "数据库操作失败", "创建人脸向量库失败")
    DB_DROP_FACE_DB_ERR = (450001, "数据库操作失败", "删除人脸数据库失败")
    DB_DROP_FACE_MILVUS_ERR = (450001, "数据库操作失败", "删除人脸向量库失败")
    DB_QUERY_FACE_DB_ERR = (450001, "数据库操作失败", "查询人脸数据库失败")
    DB_QUERY_FACE_MILVUS_ERR = (450001, "数据库操作失败", "查询人脸向量库失败")
    
    DB_CREATE_QA_DB_ERR = (450001, "数据库操作失败", "创建QA数据库失败")
    DB_CREATE_QA_MILVUS_ERR = (450001, "数据库操作失败", "创建QA向量库失败")
    DB_DROP_QA_DB_ERR = (450001, "数据库操作失败", "删除QA数据库失败")
    DB_DROP_QA_MILVUS_ERR = (450001, "数据库操作失败", "删除QA向量库失败")
    
    DB_CREATE_KNOWLEDGE_DB_ERR = (450001, "数据库操作失败", "创建知识库失败")
    DB_CREATE_KNOWLEDGE_MILVUS_ERR = (450001, "数据库操作失败", "创建知识向量库失败")
    DB_DROP_KNOWLEDGE_DB_ERR = (450001, "数据库操作失败", "删除知识库失败")
    DB_DROP_KNOWLEDGE_MILVUS_ERR = (450001, "数据库操作失败", "删除知识库失败")
    
    DB_CREATE_PERSON_ENTITY_ERR = (450001, "数据库操作失败", "添加人员实体失败")
    DB_DELETE_PERSON_ENTITY_ERR = (450001, "数据库操作失败", "删除人员实体失败")
    DB_UPDATE_PERSON_ENTITY_ERR = (450001, "数据库操作失败", "更新人员实体失败")
    DB_QUERY_PERSON_ENTITY_ERR = (450001, "数据库操作失败", "查询人员实体失败")
    
    DB_CREATE_FILE_ERR = (450001, "数据库操作失败", "添加文档失败")
    DB_DELETE_FILE_ERR = (450001, "数据库操作失败", "删除文档失败")
    DB_UPDATE_FILE_ERR = (450001, "数据库操作失败", "更新文档失败")

    DB_ADD_FACE_ERR = (450001, "数据库操作失败", "添加人脸失败")
    DB_DELETE_FACE_ERR = (450001, "数据库操作失败", "删除人脸失败")
    DB_UPDATE_FACE_ERR = (450001, "数据库操作失败", "更新人脸失败")
    DB_QUERY_FACE_ERR = (450001, "数据库操作失败", "查询人脸失败")
    DB_SEARCH_FACE_ERR = (450001, "数据库操作失败", "搜索人脸失败")
    
    DB_ADD_QA_ERR = (450001, "数据库操作失败", "添加QA对失败")
    DB_DELETE_QA_ERR = (450001, "数据库操作失败", "删除QA对失败")
    DB_UPDATE_QA_ERR = (450001, "数据库操作失败", "更新QA对失败")
    DB_QUERY_QA_ERR = (450001, "数据库操作失败", "查询QA对失败")
    DB_SEARCH_QA_ERR = (450001, "数据库操作失败", "搜索QA对失败")
    
    DB_QUERY_KNOWLEDGE_ERR = (450001, "数据库操作失败", "查询知识库内容失败")
    DB_SEARCH_KNOWLEDGE_ERR = (450001, "数据库操作失败", "搜索知识库内容失败")


    # 450002 请求的数据库不存在
    DB_NOT_EXIST_ERR = (450002, "请求的数据库不存在", "请求的数据库不存在")
    DB_NOT_EXIST_APPKEY_ERR = (450002, "请求的数据库不存在", "该 AppKey 未注册，请求的数据库不存在")

    DB_NOT_EXIST_NOT_DELETE_ERR = (450002, "请求的数据库不存在", "请求的数据库不存在，无法删除")
    DB_NOT_EXIST_NOT_CREATE_ENTITY_ERR = (450002, "请求的数据库不存在", "请求的数据库不存在，无法创建实体")
    DB_NOT_EXIST_NOT_DELETE_ENTITY_ERR = (450002, "请求的数据库不存在", "请求的数据库不存在，无法删除实体")
    DB_NOT_EXIST_NOT_UPDATE_ENTITY_ERR = (450002, "请求的数据库不存在", "请求的数据库不存在，无法更新实体")
    DB_NOT_EXIST_NOT_QUERY_ENTITY_ERR = (450002, "请求的数据库不存在", "请求的数据库不存在，无法查询实体")

    DB_NOT_EXIST_USERNAME_DBNAME_ERR = (450002, "请求的知识库不存在", "UserName 或 DbName 错误，或知识库不存在")
    
    # 450003 请求的数据库已存在
    DB_EXIST_ERR = (450003, "请求的数据库已存在", "请求的数据库已存在")
    DB_EXIST_NOT_CREATE_ERR = (450003, "请求的数据库已存在", "请求的数据库已存在，无法创建")


    # 450004 请求的数据库实体不存在
    DB_NOT_ENTITY_EXIST_ERR = (450004, "请求的数据库实体不存在", "请求的数据库实体不存在")
    DB_NOT_ENTITY_EXIST_PERSON_ERR = (450004, "请求的数据库实体不存在", "请求的人员实体库不存在")
    DB_NOT_ENTITY_EXIST_PERSON_NOT_ADD_FACE_ERR = (450004, "请求的数据库实体不存在", "请求的人员实体库不存在，无法添加人脸")
    DB_NOT_ENTITY_EXIST_PERSON_NOT_DELETE_FACE_ERR = (450004, "请求的数据库实体不存在", "请求的人员实体库不存在，无法删除人脸")
    DB_NOT_ENTITY_EXIST_PERSON_NOT_UPDATE_FACE_ERR = (450004, "请求的数据库实体不存在", "请求的人员实体库不存在，无法更新人脸")
    DB_NOT_ENTITY_EXIST_PERSON_NOT_QUERY_FACE_ERR = (450004, "请求的数据库实体不存在", "请求的人员实体库不存在，无法查询人脸")
    DB_NOT_ENTITY_EXIST_PERSON_NOT_SEARCH_FACE_ERR = (450004, "请求的数据库实体不存在", "请求的人员实体库不存在，无法搜索人脸")


    # 450005 请求的数据库实体已存在
    DB_ENTITY_EXIST_ERR = (450005, "请求的数据库实体已存在", "请求的数据库实体已存在")
    DB_ENTITY_EXIST_PERSON_ERR = (450005, "请求的数据库实体已存在", "请求的人员实体库已存在")
    DB_ENTITY_EXIST_PERSON_NOT_ADD_FACE_ERR = (450005, "请求的数据库实体已存在", "请求的人员实体库已存在，无法添加人脸")


    # server 服务 5xxxxxx
    SERVER_ERR = (500001, "服务接口异常，请联系管理员", "需要联系管理员处理")
    SERVER_DB_ERR = (500002, "数据库接口异常，请联系管理员", "需要联系管理员处理")
    SERVER_INFER_ERR = (500003, "模型推理错误，请联系管理员", "需要联系管理员处理")
    
    SERVER_DEPENDENT_ERR = (500004, "依赖服务异常，请联系管理员", "依赖服务异常，请联系管理员")
    SERVER_DEPENDENT_EMBED_ERR = (500004, "依赖服务异常，请联系管理员", "Embedding 组件异常，请联系管理员")
    SERVER_DEPENDENT_RANK_ERR = (500004, "依赖服务异常，请联系管理员", "Ranking 组件异常，请联系管理员")
    SERVER_DEPENDENT_DMX_ERR = (500004, "依赖服务异常，请联系管理员", "大模型组件异常，请联系管理员")
    SERVER_DEPENDENT_PARSE_ERR = (500004, "依赖服务异常，请联系管理员", "文本解析组件异常，请联系管理员")
    SERVER_DEPENDENT_CHUNK_ERR = (500004, "依赖服务异常，请联系管理员", "文本切分组件异常，请联系管理员")
    SERVER_DEPENDENT_SEARCH_ERR = (500004, "依赖服务异常，请联系管理员", "搜索组件异常，请联系管理员")

    SERVER_LICENSE_EXPIRE_ERR = (500005, "授权过期，请联系管理员", "授权过期，请联系管理员")

    ### 业务字段 6xxxxx

    ### 人体相关业务字段 600xxx ###

    # 600001 人体特征提取错误
    BODY_FEATURE_ERR = (600001, "人体特征提取错误", "人体特征提取错误")
    BODY_FEATURE_NUM_ONE_ERR = (601001, "人体特征提取错误", "人体数量大于 1")
    BODY_FEATURE_NUM_DOC_ERR = (601001, "人体特征提取错误", "人体数量错误，请参考接口文档说明")

    # 600002 未检测到人体
    BODY_NO_DETECT_ERR = (600002, "未检测到人体", "未检测到人体")


    ### 人脸相关业务字段 601xxx ###

    # 601001 人脸特征提取错误
    FACE_FEATURE_ERR = (601001, "人脸特征提取错误", "人脸特征提取错误")
    FACE_FEATURE_NUM_ONE_ERR = (601001, "人脸特征提取错误", "人脸数量大于 1")
    FACE_FEATURE_NUM_DOC_ERR = (601001, "人脸特征提取错误", "人脸数量错误，请参考接口文档说明")
    FACE1_NO_DETECT_ERR = (601002, "图片一未检测到人脸", "上传图片一中不包含人脸")
    FACE2_NO_DETECT_ERR = (601002, "图片二未检测到人脸", "上传图片二中不包含人脸")
    
    # 601002 未检测到人脸
    FACE_NO_DETECT_ERR = (601002, "未检测到人脸", "未检测到人脸")
    # 601002 人脸不存在
    NOT_FACE_ID = (601002, "此人脸不存在", "此人脸不存在")

    # 601003 未检测到人脸
    FACE_QUALITY_ERR = (601003, "输入图片质量不符合要求", "输入图片质量不符合要求")
    
    ### Roi 相关业务字段 602xxx ###
    
    # 602001 Roi 不符合规范
    ROI_POLYGON = (602001, "Roi 不符合规范", "Roi 不符合规范，应该为凸多边形")
    
    # 联网相关业务 7xxxxx
    WEB_API_ERROR = (700001, "联网搜索服务异常", "需要联系管理员处理")
    WEB_INVALID_ACCOUNT_ERROR = (700002, "联网搜索账号不存在，请检查账号", "联网搜索账号不存在，请检查账号")
    WEB_ACCOUNT_STATS_ERROR = (700003, "联网搜索账号状态异常", "联网搜索账号状态异常")
    WEB_ARREARS_ERROR = (700004, "联网搜索账号欠费，请充值", "联网搜索账号欠费，请充值")
    WEB_RATE_LIMIT_ERROR = (700005, "联网搜索服务限流，请重试", "联网搜索服务限流，请重试")