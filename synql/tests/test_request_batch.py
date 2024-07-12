# This may be helpful for testting out the batch processing functionality.
# Please set up the test data as needed, and feel free to reach out if you need any help: denver@semiotic.ai :)

# # system packages 
# import json 

# # external packages
# from openai import OpenAI
# from openai.types import FileContent, FileDeleted, FileObject

# # internal packages
# from synsql import SynSql
# from synsql import prepare_batch_request_file, upload_batch_request_file, create_batch_request

# class TestBatchProcessor:

#     def test_prepare_batch_request_file(self, syn: SynSql):
#         input_file_path = "tests/local_data/syn/test_generation_requests_pre_process.jsonl"
#         output_file_path = "tests/local_data/syn/test_generation_requests_post_process.jsonl"
#         prepare_batch_request_file(
#             input_file_path=input_file_path,
#             output_file_path=output_file_path
#         )

#     def test_upload_batch_request_file(self, open_ai_client: OpenAI):
#         upload_file_path = "tests/local_data/syn/test_generation_requests_post_process.jsonl"

#         upload = False
#         if upload:
#             file_id = upload_batch_request_file(
#                 client=open_ai_client,
#                 upload_file_path=upload_file_path
#             )
#             assert isinstance(file_id, str)
#         assert isinstance(open_ai_client, OpenAI)   

#     def test_get_file(self, open_ai_client: OpenAI):
#         test_file = "file-41PSv5SzkJG7PXMHCBLBDQTX"
#         file = open_ai_client.files.retrieve(test_file)
#         assert isinstance(file, FileObject)

#     def test_create_batch_request(self, open_ai_client: OpenAI):
#         upload_file_path = "tests/local_data/syn/test_generation_requests_post_process.jsonl"
#         save_path = "tests/local_data/syn/batch_request_meta_data.json"
        
#         run_create_batch_request = False
#         if run_create_batch_request:
#             batch_request = create_batch_request(
#                 client=open_ai_client,
#                 upload_file_path=upload_file_path,
#                 description="Test batch request",
#                 save_path=save_path
#             )