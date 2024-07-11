pipeline {
    agent any

    // environment {
    //     SONAR_SCANNER = tool 'SonarScanner'
    //     SNYK = tool name: 'Snyk@Latest'
    // }

    stages {

        stage("create file") {
            steps {
                sh"echo hello > test.txt"
                sh"mv test.txt /tmp/test.txt"
            }
        }
        stage("upload file") {
            slackUploadFile channel: 'jenkins-vulnerabilities-scans', filePath: "/tmp/test.txt", initialComment:  "upload test:"
            slackUploadFile channel: 'jenkins-vulnerabilities-scans', filePath: "/tmp/test.txt"
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