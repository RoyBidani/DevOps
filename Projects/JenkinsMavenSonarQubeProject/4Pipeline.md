import org.jfrog.hudson.pipeline.common.types.ArtifactoryServer

pipeline {
    agent any
    
    stages {
        stage('Fetch Code') {
            steps {
                // Clone the GitLab repository
                echo 'Fetching source code from GitLab...'
                git branch: 'feature-branch', credentialsId: 'Calculator', url: 'http://172.31.33.251/RoyBidani/calculator.git'
            }
        }
        stage('Build with Maven') {
            steps {
                // Build the Java application using Maven
                sh 'mvn clean package'
            }
        }
        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('calculator') {
                    sh 'mvn sonar:sonar'
                }
            }
        }
        stage("Quality gate") {
            steps {
                timeout(time: 1, unit: 'HOURS') { // Set a reasonable timeout duration
                waitForQualityGate abortPipeline: true
        }
    }
}
          stage('Publish to Artifactory') {
            steps {
                script {
                    def server = Artifactory.server 'Artifactory'
                    def uploadSpec = """{
                        "files": [
                            {
                                "pattern": "target/*.jar",
                                "target": "Calculator/"
                            }
                        ]
                    }"""
                    server.upload uploadSpec
                }
            }
        }
        stage("clean") {
            steps {
                deleteDir()
        }
    }
}
     post {
        success {
            // Send email notification for successful pipeline
            mail to: 'roybidani2@gmail.com',
                 subject: "Success pipeline - Build #${env.BUILD_NUMBER}",
                 body: "The pipeline was successful.\n\n" +
                       "Build Number: ${env.BUILD_NUMBER}\n" +
                       "Build URL: ${env.BUILD_URL}\n"
        }
        failure {
            // Send email notification for failed pipeline
            mail to: 'roybidani2@gmail.com',
                 subject: "Failed pipeline - Build #${env.BUILD_NUMBER}",
                 body: "The pipeline has failed.\n\n" +
                       "Build Number: ${env.BUILD_NUMBER}\n" +
                       "Build URL: ${env.BUILD_URL}\n"
        }
    }
  
}

