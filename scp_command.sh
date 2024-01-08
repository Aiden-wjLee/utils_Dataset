FOLDER_NAME="nachi_grid_integrated_12_4"
REMOTE_USER="wonjong"
REMOTE_HOST="192.168.50.126"
REMOTE_PATH="/data/wonjong/23/Dataset/${FOLDER_NAME}/"

# SCP 명령어 실행
scp -r ./${FOLDER_NAME}/ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}