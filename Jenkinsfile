def Weatherapp_running = false

pipeline {
    agent any

    // environment {
    //     TARGET_HOST = '172.31.42.31'
    // }

    stages {
        stage('build') {
            steps {
                dir('./Python-Project') {
                    sh "docker build -t bensh99/weatherapp:$BUILD_NUMBER ."
                }
            }
        }

        stage('test') {
            steps {
                dir('./Python-Project') {
                    script {
                        sh "docker run --rm -p 8000:8000 -d bensh99/weatherapp:$BUILD_NUMBER"
                        Weatherapp_running = true
                    }
                }
                dir('./Python-Project') {
                    sh 'python3 test.py'
                    sh "docker kill bensh99/weatherapp:$BUILD_NUMBER"
                }
            }
        }

        stage('push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'DockerHubCredentials', passwordVariable: 'HUB_PASSWORD', usernameVariable: 'HUB_USERNAME')]) {
                    script {
                        sh "docker login -u $HUB_USERNAME -p $HUB_PASSWORD"
                        sh "docker push bensh99/weatherapp:$BUILD_NUMBER"
                        sh 'docker logout'
                    }
                }
            }
        }

        stage('Update Helm chart') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'GitHubCredentials', passwordVariable: 'GitHub_Token', usernameVariable: 'GitHub_User')]) {
                script{

                    sh "git clone https://$GitHub_Token@github.com/bensh199/WeatherApp-Helm.git"
                    sh 'chmod +x ./WeatherApp-Helm/version.sh'
                    sh "./WeatherApp-Helm/version.sh $BUILD_NUMBER"

                    sh 'git add .'
                    sh 'git commit -m "JenkinsAction: Update Docker image tag"'
                }
               }
            }
        }

        // post {
        //     always {
        //         script {
        //             if (Weatherapp_running == true) {
        //                 dir('./WeatherAppCompose') {
        //                     sh 'docker compose down'
        //                 }
        //             }
        //         }
        //     }
        //     success {
        //         slackSend(channel: '#bens-pipeline-notifications-success', color: 'good', message: "Build #${env.BUILD_NUMBER} successful!")
        //     }
        //     failure {
        //         slackSend(channel: '#bens-pipeline-notifications-failed', color: 'bad', message: "Build #${env.BUILD_NUMBER} failed successfully!")
        //     }
        // }
    }
}