#!/bin/bash

read -p "Enter the service name: " service_name
service_status=$(systemctl is-active "$service_name")

echo "Service status: $service_status"

echo "Menu:"
echo "1. Start the service"
echo "2. Stop the service"
echo "3. Leave it at the current state"

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        sudo systemctl start "$service_name"
        ;;
    2)
        sudo systemctl stop "$service_name"
        ;;
    3)
        echo "Leaving the service at the current state."
        ;;
    *)
        echo "Invalid choice."
        ;;
esac
