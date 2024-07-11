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
                sh"mv test1.txt /tmp/test.txt"
                sh"mv test2.txt /tmp/test2.txt"
            }
        }
        stage("upload 1") {
            steps {
                slackUploadFile channel: 'jenkins-vulnerabilities-scans', filePath: "/tmp/test1.txt", initialComment:  "upload file1:"
            }
        }
        stage("upload 2") {
            steps {
                slackUploadFile channel: 'jenkins-vulnerabilities-scans', filePath: "/tmp/test2.txt", initialComment:  "upload file2:"
            }
        }
    }
    post {
        always {
            // sh 'docker logout'
            // cleanWs(deleteDirs: true,
            //         disableDeferredWipeout: true)
            slackSend channel: 'jenkins-vulnerabilities-scans', color: "good", message: "test slack, result: https://ci.build.novisign.com/job/Trivy_test/$BUILD_NUMBER/execution/node/$EXECUTOR_NUMBER/ws/trivy_results/" 
        }
    }
}