import hashlib
import json

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *

def get_record(YOUR_APP_ID,YOUR_APP_SECRET,app_token,table_id,view_id,field_value):
    field_names=["md5"]
    # 创建client
    client = lark.Client.builder() \
        .app_id(YOUR_APP_ID) \
        .app_secret(YOUR_APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: SearchAppTableRecordRequest = SearchAppTableRecordRequest.builder().app_token(app_token).table_id(table_id) \
        .page_size(20) \
        .request_body(SearchAppTableRecordRequestBody.builder()
            .view_id(view_id)
            .field_names(field_names)
            .filter(FilterInfo.builder()
                .conjunction("and")
                .conditions([Condition.builder()
                    .field_name("md5")
                    .operator("is")
                    .value([field_value])
                    .build(),
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

def string_to_md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()


get_record("cli_a896910775a11013","oZvqNAt1AkvueG5szC69TBaJLx7iqDmg","W91Vbm68kaIdLxs8QpocTjjwn5b",
            "tbl4cxgCR9zKCBu1","vew3qfmhOE","1231231341241"
           )