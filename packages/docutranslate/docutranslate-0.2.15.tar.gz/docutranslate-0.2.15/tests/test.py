from docutranslate import FileTranslater
import time
start=time.time()
translater=FileTranslater(
    base_url=r"https://open.bigmodel.cn/api/paas/v4/",
    key="969ba51b61914cc2b710d1393dca1a3c.hSuATex5IoNVZNGu",
    model_id="GLM-4-Flash",
    max_concurrent=30)

# translater=FileTranslater(
#     base_url=r"https://dashscope.aliyuncs.com/compatible-mode/v1",
#     key="sk-a3dd6bdedb5f446cbe678aedfab32038",
#     model_id="qwen-plus",
#     chunksize=2000,
# )

# translater=FileTranslater(
#     base_url=r"https://api.deepseek.com/v1",
#     key="sk-d809e448131d4fbc903a0ed476964294",
#     model_id="deepseek-chat",
#     chunksize=2000,
# )

# translater.translate_file("./files/test7.md",
#                           to_lang="中文",
#                           refine=True,
#                           formula=True,
#                           code=True,
#                           output_format="markdown")
#


translater.read_file("./files/test7.pdf",save=True,formula=True,code=True)


print(f"耗时:{time.time()-start}")