# -*- coding =utf-8 -*-
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class HTTPStatusDigitalLife(Enum):
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

    # 0 请求成功
    SUCCESS = (0, '请求成功', '')

    # 1001 参数错误
    PARAM_FORMAT_ERR = (1001, '参数错误', '')

    # 必传的参数未传
    sourceId_MUST_PRAM_ERR = (1001, '必须的参数 sourceId 未传', '')
    source_MUST_PRAM_ERR = (1001, '必须的参数 source 未传', '')
    requestId_MUST_PRAM_ERR = (1001, '必须的参数 requestId 未传', '')

    # 请求体的字段类型错误
    sourceId_STRING_TYPE_ERR = (1001, 'sourceId 参数应该是 string 类型', '')
    sourceType_INT_TYPE_ERR = (1001, 'sourceType 参数应该是 int 类型', '')
    source_STRING_TYPE_ERR = (1001, 'source 参数应该是 string 类型', '')
    monitorArea_ARRAY_TYPE_ERR = (1001, 'monitorArea 参数应该是 array 类型', '')
    isTagPic_INT_TYPE_ERR = (1001, 'isTagPic 参数应该是 int 类型', '')
    requestId_STRING_TYPE_ERR = (1001, 'requestId 参数应该是 string 类型', '')

    # 请求体的参数字段值为空
    sourceId_EMPTY_ERR = (1001, 'sourceId 参数不能为空', '')
    source_EMPTY_ERR = (1001, 'source 参数不能为空', '')
    monitorArea_EMPTY_ERR = (1001, 'monitorArea 参数不能为空', '')
    requestId_EMPTY_ERR = (1001, 'requestId 参数不能为空', '')

    # 请求体的参数字段值设置错误
    sourceType_VALUE_ERR = (1001, 'sourceType 参数值不符合规范', '')
    isTagPic_VALUE_ERR = (1001, 'isTagPic 参数值不符合规范', '')

    # 1002 请求异常
    REQUEST_ERR = (1002, "请求异常", "")
    REQUEST_PATH_ERR = (1002, '请求路径错误', '')
    REQUEST_METHOD_ERR = (1002, '请求方法错误', '')
    REQUEST_METHOD_POST_ERR = (1002, '请求方法错误，请使用 POST 请求', '')
    REQUEST_METHOD_GET_ERR = (1002, '请求方法错误，请使用 GET 请求', '')
    BODY_EMPTY_ERR = (1002, '请求体内容为空', '')
    BODY_JSON_ERR = (1002, '请求体非 json 格式', '')
    BODY_TYPE_ERR = (1002, '请求体类型错误，请求体需为字典类型', '')

    # 1003 内部服务异常
    INTERNAL_SERVICE_ERR = (1003, "内部服务异常", "")
    SERVER_ERR = (1003, "服务接口异常，请联系管理员", "")
    
    # 1004 获取刷新地址异常
    REFRESH_SOURCE_URL_ERR = (1004, "获取刷新地址异常", "")

    # 1005 上传文件异常
    UPLOAD_FILE_ERR = (1005, "上传文件异常", "")

    # 1006 图像等资源异常
    SOURCE_ERR = (1006, "图像等资源异常", "")
    SOURCE_BASE64_ERR = (1006, "图片 base64 数据处理异常", "")
    
    SOURCE_IMAGE_TYPE_ERR = (1006, "图片格式不合法，仅支持 jpeg/png/jpg/bmp 格式", "")
    SOURCE_IMAGE_TYPE_DOC_ERR = (1006, "图片文件格式不合法，请参考接口文档", "")
    
    SOURCE_IMAGE_SIZE_ERR = (1006, "图片大小不符合要求，图片要求小于 7M", "")
    SOURCE_IMAGE_SIZE_DOC_ERR = (1006, "图片文件大小不符合要求，请参考接口文档", "")
    
    SOURCE_IMAGE_DECODE_ERR = (1006, "图片解码错误", "")
    
    SOURCE_IMAGE_SHAPE_ERR = (1006, "图片尺寸不符合要求，分辨率长宽尺寸应不高于 5000 不低于 32", "")
    SOURCE_IMAGE_SHAPE_DOC_ERR = (1006, "图片尺寸不符合要求，请参考接口文档", "")

    SOURCE_IMAGE_URL_ERR = (1006, "图片 URL 下载失败", "")

    # 1007 流文件不合法
    STREAM_ILLEGAL_ERR = (1007, "流文件不合法", "")

    # 1008 算法编码错误
    ALGORITHM_CODE_ERR = (1008, "算法编码错误", "")
