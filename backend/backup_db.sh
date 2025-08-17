#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Create filename with current date and time
BACKUP_FILE="${DB_NAME}_backup_$(date +%Y%m%d_%H%M%S).sql"
ARCHIVE_FILE="${DB_NAME}_backup_$(date +%Y%m%d_%H%M%S).tar.gz"

# Create database backup
echo "Creating backup of database ${DB_NAME}..."
PGPASSWORD=${DB_PASSWORD} docker compose exec -T postgres pg_dump -U ${DB_USER} -d ${DB_NAME} > ${BACKUP_FILE}

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "Backup created successfully: ${BACKUP_FILE}"
    
    # Create archive
    echo "Creating archive..."
    tar -czf ${ARCHIVE_FILE} ${BACKUP_FILE}
    
    # Check if archive creation was successful
    if [ $? -eq 0 ]; then
        echo "Archive created successfully: ${ARCHIVE_FILE}"
        
        # Remove original SQL file
        rm ${BACKUP_FILE}
        echo "Original SQL file removed."
    else
        echo "Error creating archive."
    fi
else
    echo "Error creating database backup."
fi
