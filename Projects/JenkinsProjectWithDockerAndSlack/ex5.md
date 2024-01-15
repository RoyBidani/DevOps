1. add "deployment" stage that stops and remove the runing container, and pull from Dockerhub the latest image and build a new container with the image.

        stage('Deployment') {
            steps {
                echo 'Deploying the updated Docker container...'
                script {
                     // SSH into the EC2 instance and execute deployment commands
                    sshagent(['deployment instance']) {
                    
                        // delete the runing container
                        sh "ssh -o StrictHostKeyChecking=no ec2-user@172.31.44.243 'docker rm -f new-container'"

                        // Pull the updated image
                        sh "ssh -o StrictHostKeyChecking=no ec2-user@172.31.44.243 'docker pull roybidani/weather_app:app'"

                        // Run the new container
                        sh "ssh -o StrictHostKeyChecking=no ec2-user@172.31.44.243 'docker run -d -p 8000:8000 --name new-container roybidani/weather_app:app'"
                    }
                
                }
            }
        }
    
    
    
                        

