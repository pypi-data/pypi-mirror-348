# -*- coding =utf-8 -*-
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class HTTPStatusElectronFence(Enum):
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

    def __new__(cls, value, phrase, description=""):
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
    SUCCESS = (0, "success", "Success")

    BODY_JSON_ERR = (4004, "请求体格式错误，json内容不能为空", "请求的body不是字典类型")
    MUST_PRAM_ERR = (4005, "请求参数中缺少关键字，仅支持image和area", "请求body中的参数名错误")
    IMAGE_ONLY_LIST_ERR = (4006, "请求参数类型错误，image仅支持list", "参数image的格式需要为list")
    LIST_NOT_EMPTY_ERR = (4007, "请求参数内容错误，list不能为空或大于32", "参数image的list内容为空长度超限")
    IMGAE_DECODE_ERR = (4009, "请求参数内容错误，图像解析失败", "图像解析不成功")
    AREA_ONLY_STRING_ERR = (4011, "请求参数类型错误，area仅支持string", "传递的area值需要为string")
    AREA_NOT_MATCH_ERR = (4012, "请求参数内容错误，area字符串不符合要求", "设置电子围栏区域'x1,y1,x2,y2,x3,y3,x4,y4'，数据类型为字符串，坐标点数量大于2小于10, 逆时针或顺时针排序")
    AREA_OUT_RANGE_ERR = (4013, "请求参数错误，area范围超出图像区域", "参数area范围超过图像区域，或不支持的图片格式")
    SERVER_ERR = (5000, "服务错误", "未被识别的异常错误")
    INFER_ERR = (5001, "推理服务异常，请联系管理员", "推理过程中服务处理失败")
    DATABASE_ERR = (5002, "数据库服务异常，请联系管理员", "数据库处理错误")
