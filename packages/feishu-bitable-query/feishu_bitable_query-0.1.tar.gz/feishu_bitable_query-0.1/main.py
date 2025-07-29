import json

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *


def t():
    return "test"

def get_record():
    # 创建client
    client = lark.Client.builder() \
        .app_id("YOUR_APP_ID") \
        .app_secret("YOUR_APP_SECRET") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: SearchAppTableRecordRequest = SearchAppTableRecordRequest.builder() \
        .page_size(20) \
        .request_body(SearchAppTableRecordRequestBody.builder()
            .view_id("vewqhz51lk")
            .field_names(["店铺", "ASIN"])
            .sort([Sort.builder()
                .field_name("多行文本")
                .desc(True)
                .build()
                ])
            .filter(FilterInfo.builder()
                .conjunction("and")
                .conditions([Condition.builder()
                    .field_name("职位")
                    .operator("is")
                    .value(["初级销售员"])
                    .build(),
                    Condition.builder()
                    .field_name("销售额")
                    .operator("isGreater")
                    .value(["10000.0"])
                    .build()
                    ])
                .build())
            .automatic_fields(False)
            .build()) \
        .build()

    # 发起请求
    response: SearchAppTableRecordResponse = client.bitable.v1.app_table_record.search(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_record.search failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    return lark.JSON.marshal(response.data, indent=4)
