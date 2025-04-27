#!/bin/bash
# Script to run the patient response model training and log all output to ml_pipeline.log

CMD="python manage.py shell -c 'from services.ai.training import train_patient_response_model; train_patient_response_model()'"
# echo "===== Run at $(date --iso-8601=seconds) =====" >> ml_pipeline.log
echo "===== Run at $(date "+%Y-%m-%dT%H:%M:%S") =====" >> ml_pipeline.log
echo "Command: $CMD" >> ml_pipeline.log
# Run the command, append stdout and stderr to the log
python manage.py shell -c "from services.ai.training import train_patient_response_model; train_patient_response_model()" >> ml_pipeline.log 2>&1
echo -e "\n" >> ml_pipeline.log
