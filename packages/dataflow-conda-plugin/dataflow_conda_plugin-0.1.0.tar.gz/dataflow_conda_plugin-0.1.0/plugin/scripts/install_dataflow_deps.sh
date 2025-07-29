#!/bin/bash
set -e
conda_env_path=$1

py_version=$(${conda_env_path}/bin/python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
                      
${conda_env_path}/bin/pip install dash dash-renderer plotly flask flask-appbuilder typing jupyterhub oauthenticator jupyter-server-proxy jupyter streamlit ipython ipykernel ipython-sql jupysql psycopg2-binary dataflow-core dataflow-dbt    

# 3. Install Dataflow Airflow to a separate path in environment 
${conda_env_path}/bin/pip install \
    --force-reinstall --root-user-action ignore \
    --no-warn-conflicts dataflow-airflow==2.10.5 \
    --target ${conda_env_path}/bin/airflow-libraries/

files=(
    ${conda_env_path}/lib/python${py_version}/site-packages/dbt/config/profile.py 
    ${conda_env_path}/lib/python${py_version}/site-packages/dbt/task/debug.py
)
for file in ${files[@]}
do      
    awk '{gsub("from dbt.clients.yaml_helper import load_yaml_text", "from dbt.dataflow_config.secrets_manager import load_yaml_text"); print}' $file > temp 
    mv temp $file
done

echo "Environment Creation Successful"