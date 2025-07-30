import os
import sys
import boto3
import time
import uuid
import datetime
import traceback
import requests
from pushover import Client

DYNAMODB_METHODS = [
    'get_item', 'put_item', 'update_item', 'delete_item',
    'batch_get_item', 'batch_write_item',
    'query', 'scan'
]

class LambdaMonitor:

    def __init__(self, context, suffix=None):
        sys.stdout.write(f"initialising LambdaMonitor\n")
        sys.stdout.flush()

        self.start_time = time.time()

        self.dbd = boto3.client('dynamodb')
        self.function_name = context.function_name

        if suffix is not None:
            self.function_name = f"{self.function_name}_{suffix}"

        self.state = self.get_state()
        self.pushover = pushover = Client(os.environ['LAMBDA_TRACING_PUSHOVER_USER'], api_token=os.environ['LAMBDA_TRACING_PUSHOVER_APP'])

        self.initialise_metrics()

        self.track_calls = False


    def initialise_metrics(self):
        self.calls = {
        }

        for method in DYNAMODB_METHODS:
            self.calls[method] = 0

        self.metrics = {
            'read': 0,
            'write': 0,
            'delete': 0
        }


    def collect_metrics(self):
        if self.track_calls is False:
            self.patch_boto()
            self.track_calls = True


    def log_method_call(self, method_name):
        if method_name not in self.calls:
            self.calls[method_name] = 0

        self.calls[method_name] += 1


    def log_read(self, count):
        self.metrics['read'] += count


    def log_write(self, count):
        self.metrics['write'] += count


    def log_delete(self, count):
        self.metrics['delete'] += count


    def patch_boto(self):
        original_client = boto3.client
        lm = self

        def patch_method(client, method_name):
            original = getattr(client, method_name)

            def wrapper(*args, **kwargs):
                lm.log_method_call(method_name)
                resp = original(*args, **kwargs)

                if 'Item' in resp:
                    lm.log_read(1)
                elif 'Items' in resp:
                    lm.log_read(len(resp['Items']))

                if method_name in ['put_item', 'update_item']:
                    lm.log_write(1)
                elif method_name == 'delete_item':
                    lm.log_delete(1)
                elif method_name == 'batch_write_item':
                    for key in kwargs['RequestItems']:
                        lm.log_write(len(kwargs['RequestItems'][key]))

                return resp

            setattr(client, method_name, wrapper)

        def patched_client(service_name, *args, **kwargs):
            client = original_client(service_name, *args, **kwargs)
            if service_name == 'dynamodb':
                for method in DYNAMODB_METHODS:
                    if hasattr(client, method):
                        patch_method(client, method)
            return client

        boto3.client = patched_client


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
        timestamp = int(time.time())
        runtime = time.time() - self.start_time

        if 'success' in self.state and self.state['success']['BOOL'] == False:
            self.pushover.send_message('resolved', title=self.function_name)

        self.state['success'] = {'BOOL': True}
        self.state['last_success'] = {'N': str(timestamp)}

        self.dbd.put_item(
            TableName="lambda_state",
            Item=self.state
        )

        if self.track_calls:
            self.send_metrics(True, timestamp, runtime)


    def send_metrics(self, success, timestamp, runtime):
        sys.stdout.write(f"emitting metrics:\n")
        sys.stdout.write(f"success: {int(success)}\n")
        sys.stdout.write(f"runtime: {runtime:.2f} seconds\n")

        for method, count in self.calls.items():
            sys.stdout.write(f"{method}: {count}\n")

        for metric, count in self.metrics.items():
            sys.stdout.write(f"{metric}: {count}\n")

        sys.stdout.flush()

        resp = requests.post(
            os.environ['LAMBDA_TRACING_METRICS_ENDPOINT'],
            json={
                'success': success,
                'key': self.function_name,
                'timestamp': timestamp,
                'runtime': runtime,
                'calls': self.calls,
                'metrics': self.metrics
            },
            headers={
                'Content-Type': 'application/json'
            },
            timeout=5,
            auth=(os.environ['LAMBDA_TRACING_METRICS_USERNAME'], os.environ['LAMBDA_TRACING_METRICS_PASSWORD'])
        )


    def failure(self):
        timestamp = int(time.time())
        runtime = time.time() - self.start_time

        if self.track_calls:
            self.send_metrics(False, timestamp, runtime)

        if 'success' not in self.state or self.state['success']['BOOL'] == True:
            exception = traceback.format_exc()

            content = f"Function: {self.function_name}\n"
            content += f"Runtime: {runtime:.2f} seconds\n"
            content += f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            content += traceback.format_exc()

            self.dbd.put_item(
                TableName="lambda_tracing",
                Item={
                    'key': {'S': self.state['key']['S']},
                    'timestamp': {'N': str(timestamp)},
                    'exception': {'S': content}
                }
            )

            exception_endpoint = os.environ['LAMBDA_TRACING_EXCEPTION_ENDPOINT']

            url = f"{exception_endpoint}?key={self.function_name}&timestamp={int(time.time())}"

            exception = traceback.format_exception_only(*sys.exc_info()[:2])[-1].strip()

            self.pushover.send_message(exception, title=self.function_name, url=url)

            self.state['success'] = {'BOOL': False}

            resp = self.dbd.put_item(
                TableName="lambda_state",
                Item=self.state
            )
