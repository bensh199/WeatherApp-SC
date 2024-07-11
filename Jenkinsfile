pipeline {
    agent any

    // environment {
    //     SONAR_SCANNER = tool 'SonarScanner'
    //     SNYK = tool name: 'Snyk@Latest'
    // }

    stages {

        stage("create file") {
            steps {
                sh"echo hello > test1.txt"
                sh"echo hello > test2.txt"
                sh"mv test.txt /tmp/test.txt"
                sh"mv test2.txt /tmp/test2.txt"
            }
        }
        stage("upload 1") {
            slackUploadFile channel: 'jenkins-vulnerabilities-scans', filePath: "/tmp/test1.txt", initialComment:  "upload file1:"
            
        }
        stage("upload 2") {
            slackUploadFile channel: 'jenkins-vulnerabilities-scans', filePath: "/tmp/test2.txt", initialComment:  "upload file2:"
        }
    }
    post {
        always {
            // sh 'docker logout'
            // cleanWs(deleteDirs: true,
            //         disableDeferredWipeout: true)
            slackSend channel: 'jenkins-vulnerabilities-scans', color: "good", message: "test slack"
        }
    }
}