# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import Optional

# [START documentai_train_processor_version]

from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID'
# processor_version_display_name = 'new-processor-version'
# train_data_uri = 'gs://bucket/directory/' # (Optional)
# test_data_uri = 'gs://bucket/directory/' # (Optional)


def train_processor_version_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version_display_name: str,
    train_data_uri: Optional[str] = None,
    test_data_uri: Optional[str] = None,
) -> None:
    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g. `projects/{project_id}/locations/{location}/processors/{processor_id}
    parent = client.processor_path(project_id, location, processor_id)

    processor_version = documentai.ProcessorVersion(
        display_name=processor_version_display_name
    )

    # If train/test data is not supplied, the default sets in the Cloud Console will be used
    input_data = documentai.TrainProcessorVersionRequest.InputData(
        training_documents=documentai.BatchDocumentsInputConfig(
            gcs_prefix=documentai.GcsPrefix(gcs_uri_prefix=train_data_uri)
        ),
        test_documents=documentai.BatchDocumentsInputConfig(
            gcs_prefix=documentai.GcsPrefix(gcs_uri_prefix=test_data_uri)
        ),
    )

    request = documentai.TrainProcessorVersionRequest(
        parent=parent, processor_version=processor_version, input_data=input_data
    )

    operation = client.train_processor_version(request=request)
    # Print operation details
    print(operation.operation.name)
    # Wait for operation to complete
    response = documentai.TrainProcessorVersionResponse(operation.result())

    metadata = documentai.TrainProcessorVersionMetadata(operation.metadata)

    print(f"New Processor Version:{response.processor_version}")
    print(f"Training Set Validation: {metadata.training_dataset_validation}")
    print(f"Test Set Validation: {metadata.test_dataset_validation}")


# [END documentai_train_processor_version]