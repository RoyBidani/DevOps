## Clear Stage

To achieve the goal of deleting any unused Docker images and containers on the Jenkins agent (slave) and deleting the 'new-container' along with any irrelevant images on the EC2 instance, you can modify the 'clear' stage as follows:

```groovy
stage('Clear') {
    steps {
        echo 'Clearing resources...'
        script {
            // Clean up on Jenkins agent (slave)
            sh "docker system prune -a --force"
            
            // SSH into the EC2 instance and clear resources
            sshagent(['deployment instance']) {
                // Stop and remove the running container (if exists)
                sh "ssh -o StrictHostKeyChecking=no ec2-user@172.31.44.243 'docker stop new-container || true'"
                sh "ssh -o StrictHostKeyChecking=no ec2-user@172.31.44.243 'docker rm -f new-container || true'"

                // Remove any dangling (unused) images and prune all unused volumes
                sh "ssh -o StrictHostKeyChecking=no ec2-user@172.31.44.243 'docker image prune -a --force'"
                sh "ssh -o StrictHostKeyChecking=no ec2-user@172.31.44.243 'docker volume prune --force'"
            }
        }
    }
}

