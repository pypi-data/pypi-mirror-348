**Readme**

DataRefiner Client Library is a Python API toolkit designed to seamlessly connect your Python code with the DataRefiner platform, enabling convenient access and interaction.

**Website**: [https://datarefiner.com](https://datarefiner.com)

### What functions this library support? ###

* Login using API key
* Upload dataset to the platform
* Configure project settings before training
* Start training (you can track rendering progress)
* Embed TDA map from DataRefiner right in your Jupyter Notebook for analysis
* Export result data from the TDA: cluster labels for source data, parameter scores for segmentation, list of the most importan features for all clusters, download TDA coordinates 
* Perform Supervised labelling (predict cluster labels and groups from trained toplogical project)

### Usage example: 
###

```
import pandas as pd

from datarefiner_client import DataRefinerClient
from datarefiner_client.services.project_settings import ProjectSettingsFactory, ProjectType
from datarefiner_client.exceptions import DatarefinerExploreDownloadsError

from dataclasses import asdict
from pprint import pprint as pp

API_TOKEN = "<api_token>" # get API token from your user profile page
API_BASE_URL = "https://app.datarefiner.com"

# Login using API key
datarefiner_api = DataRefinerClient(
    token=API_TOKEN,
    base_url=API_BASE_URL,
)
datarefiner_api.me()

# Loading new data from CSV file
df = pd.read_csv("./data.csv")

# Upload dataset to the platform
upload, project_settings = datarefiner_api.upload(df=df, title="Data", load_filedetails=True)

# Check the project settings generated automatically
pp(asdict(project_settings))

# Change the field mapping settings: overlay/learn/disabled.
project_settings.fields_config['1'].config = "overlay"
project_settings.fields_config['2'].config = "learn"
project_settings.fields_config['3'].config = "disabled"

# You can change the rest of the project settings, here some examples:
project_settings.json_params.allow_noise_points = False
project_settings.json_params.beta = [45, 100, 200]
project_settings.json_params.clusterisation_type = 'kMeans'
project_settings.json_params.metric = ['euclidean', 'cosine']

# Perform rendering of the project
project_settings.name = "Create test project from API client"
project = datarefiner_api.create_project(project_settings=project_settings)

# Embed TDA map right in your Jupyter notebook
datarefiner_api.explore(project_id=project.id)

# Get assigned clusters for your source data
cluster_labels_df = datarefiner_api.get_cluster_labels(project_id=project.id)

# Get user-defined labels for your source data (and catch the excpection if there are no groups defined for the project)
try:
    group_labels_df = datarefiner_api.get_group_labels(project_id=project.id)
    print(group_labels_df.groupby('GroupID').count())
except DatarefinerExploreDownloadsError as e: 
    print(e)

# Get top parameters impacting the segmentation
parameter_scores_df = datarefiner_api.get_parameter_scores_for_segmentation(project_id=project.id)

# Get he list of the most important features for all clusters in one request
most_important_features_df = datarefiner_api.get_most_important_features_for_all_clusters(project_id=project.id)

# Get 2D and 3D TDA coordinates for your source data points (can be used in downstream tasks) 
tda_coordinates_df = datarefiner_api.get_tda_coordinates(project_id=project.id)

# Performig prediction for new data (we use the same data as for training, but in reality you'll use new data in the same format)
clusters_df, groups_df = datarefiner_api.supervised_labeling(project_id=project.id, df=df)
```

### Visual Anomaly detection features, supported by this library: ###
###
* Upload new images from the local drive and get anomaly and detection results as JSON structures
###

```python
# Get details about your anomaly detection project
anomaly_project_id = '37379063-3980-44bd-891b-99d4062171fa'
anomaly_project = client.get_anomaly_project(anomaly_project_id=anomaly_project_id)

# Load images from the local drive
local_path: str = "./img_folder"
dataset: ImagesDataset = ImagesDataset.from_dir(local_path)

# Perform anomaly and detection steps for uploaded images
anomaly_projects_detection_prediction = client.anomaly_projects_detection_predict(anomaly_project_id=anomaly_project_id, 
                                                                                  dataset=dataset)
```

The anoresult JSON structure is following:
###

```

AnomalyProjectsDetectionPrediction
	id: 1fb75580-d712-4d32-8e1f-e2728681a1e2
	selected: False
	filename: 001.png
	url: /static/renders/37379063-3980-44bd-891b-99d4062171fa/969482a7-9394-4176-8186-baff5aa75848/001.png
	anomaly_score: 0.0269941
	created: 2024-09-17 12:55:19
	annotations:
		AnomalyProjectUploadImageAnnotation(annotate_type=<AnomalyProjectSupervisedImageAnnotateType.MODEL: 
            'model'>,  annotate=[{'type': 'scratch', 'conf': 0.897187, 'coords': [[335.3411560058594, 93.66542053222656], [357.1182556152344, 113.873779296875]]}, 
                                 {'type': 'scratch', 'conf': 0.897114, 'coords': [[91.52696228027344, 47.56052017211914], [109.08097839355469, 65.63035583496094]]}, 
                                 {'type': 'scratch', 'conf': 0.855264, 'coords': [[140.56350708007812, 361.5419921875], [156.49615478515625, 377.48468017578125]]}]),
```

