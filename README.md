# NO4MRE

# Data preparation

locate our dataverse: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/EQ6UKN

download the processed_data and store it under the folder of simulation

## simulation

First pull our docker images: docker pull weihengz/dolfinx_mre:latest

On windows system:
$path = (Get-Location).Path
docker run -it -v "${path}:/workspace" -w /workspace weihengz/dolfinx_mre:latest



