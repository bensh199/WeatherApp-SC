def Weatherapp_running = false

pipeline {
    agent any

    stages {
        stage('build') {
            steps {
                dir('./Python-Project') {
                    sh "docker build -t bensh99/weatherapp:V1.$BUILD_NUMBER ."
                }
            }
        }

        stage('test') {
            steps {
                dir('./Python-Project') {
                    script {
                        sh "docker run --rm --name weatherapp -p 8000:8000 -d bensh99/weatherapp:V1.$BUILD_NUMBER"
                        Weatherapp_running = true
                    }
                }
                dir('./Python-Project') {
                    sh 'python3 test.py'
                    sh "docker kill weatherapp"
                }
            }
        }

        stage('publish') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'DockerHubCredentials', passwordVariable: 'HUB_PASSWORD', usernameVariable: 'HUB_USERNAME')]) {
                    script {
                        sh "docker login -u $HUB_USERNAME -p $HUB_PASSWORD"
                        sh "docker push bensh99/weatherapp:V1.$BUILD_NUMBER"
                    }
                }
            }
        }

        stage('Update Helm chart') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'GitHubCredentials', passwordVariable: 'GitHub_Token', usernameVariable: 'GitHub_User')]) {
                    script{
                        dir('/home/jenkins/workspace'){

                            sh "git clone https://$GitHub_Token@github.com/bensh199/WeatherApp-Helm.git"
                            dir('/home/jenkins/workspace/WeatherApp-Helm'){
                                sh 'chmod +x ./version.sh'
                                sh "./version.sh V1.$BUILD_NUMBER"

                                sh 'git add .'
                                sh 'git config --global user.email benshahar99@gmail.com'
                                sh 'git config --global user.name Ben'
                                sh 'git commit -m "JenkinsAction: Update Docker image tag"'
                                sh 'git push'
                            }
                            sh "rm -rf ./WeatherApp-Helm/"
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout'
            cleanWs()
        }
    }
}