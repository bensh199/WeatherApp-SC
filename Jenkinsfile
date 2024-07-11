pipeline {
    agent any

    // environment {
    //     SONAR_SCANNER = tool 'SonarScanner'
    //     SNYK = tool name: 'Snyk@Latest'
    // }

    stages {

        stage {
            steps {
                sh"echo hello"
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
}