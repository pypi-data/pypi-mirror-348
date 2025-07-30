import os
import sys
import boto3
import time
import uuid
import datetime
import traceback
from pushover import Client

class LambdaMonitor:

    def __init__(self, context, suffix=None):
        self.start = time.time()

        self.s3 = boto3.client('s3')
        self.function_name = context.function_name

        if suffix is not None:
            self.function_name = f"{self.function_name}_{suffix}"

        #self.state = self.get_state()
        self.pushover = pushover = Client(os.environ['LAMBDA_TRACING_PUSHOVER_USER'], api_token=os.environ['LAMBDA_TRACING_PUSHOVER_APP'])


    def get_state(self):
        resp = self.dbd.get_item(
            TableName="lambda_state",
            Key={'key': {'S': self.function_name}}
        )

        if 'Item' in resp:
            return resp['Item']

        return {
            'key': {'S': self.function_name}
        }


    def success(self):
        return

        runtime = time.time() - self.start

        if 'success' in self.state and self.state['success']['BOOL'] == False:
            self.pushover.send_message('resolved', title=self.function_name)

        self.state['success'] = {'BOOL': True}
        self.state['last_success'] = {'N': str(int(time.time()))}

        self.dbd.put_item(
            TableName="lambda_state",
            Item=self.state
        )


    def failure(self):
        runtime = time.time() - self.start

        content = f"Function: {self.function_name}\n"
        content += f"Runtime: {runtime:.2f} seconds\n"
        content += f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        content += traceback.format_exc()

        obj_name = f"{self.function_name}/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

        self.s3.put_object(Bucket='mw-stacktraces', Key=obj_name, Body=content)

        exception = traceback.format_exception_only(*sys.exc_info()[:2])[-1].strip()

        url = self.s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'mw-stacktraces', 'Key': obj_name},
            ExpiresIn=86400
        )

        self.pushover.send_message(exception, title=self.function_name, url=url)
