#!groovy
def PROJECT_NAME = "VLOG-API"
def SLACK_CHANNEL = '#niels-test'
def PLAYBOOK = 'deploy-vlog.yml'
def PLAYBOOK_INVENTORY = 'acceptance'
def PLAYBOOK_BRANCH = 'feature/deploy-vlog'
def SLACK_MESSAGE = [
    "title_link": BUILD_URL,
    "fields": [
        ["title": "Project","value": PROJECT_NAME],
        ["title":"Branch", "value": BRANCH_NAME, "short":true],
        ["title":"Build number", "value": BUILD_NUMBER, "short":true]
    ]
]



pipeline {
    agent any

    environment {
        VERSION = env.BRANCH_NAME.replace('/', '-').toLowerCase().replace(
            'master', 'latest'
        )
        SHORT_UUID = sh( script: "uuidgen | cut -d '-' -f1", returnStdout: true).trim()
        COMPOSE_PROJECT_NAME = "${PROJECT_NAME}-${env.SHORT_UUID}"
    }

    stages {
        stage('Test') {
            steps {
                sh 'make build/test'
                sh 'make test'
            }
        }

        stage('Build, push and deploy') {
            when { 
                anyOf {
                    branch 'master'
                    buildingTag()
                }
            }
            environment {
                TNO_CI_KEY = credentials('TNO_CI_KEY')
            }
            stages {
                stage('Build') {
                    steps {
                        sh 'make build'
                    }
                }

                stage('Push') {
                    steps {
                        retry(3) {
                            sh 'make push'
                        }
                    }
                }

                stage('Deploy to acceptance') {
                    when { tag pattern: "[\\d+\\.]+-RC.*", comparator: "REGEXP"}
                    steps {
                        sh 'echo Deploy acceptance'
                        build job: 'Subtask_Openstack_Playbook', parameters: [
                            string(name: 'PLAYBOOK', value: PLAYBOOK),
                            string(name: 'INVENTORY', value: PLAYBOOK_INVENTORY),
                            string(name: 'BRANCH', value: PLAYBOOK_BRANCH),
                            string(
                                name: 'PLAYBOOKPARAMS', 
                                value: "-e deployversion=${VERSION}"
                            )
                        ], wait: true
                    }
                }

                stage('Deploy to production') {
                    when { tag pattern: "[\\d+\\.]+-RC.*", comparator: "REGEXP"}
                    steps {
                        sh 'echo Deploy prod'
                    }
                }
            }
        }

    }
    post {
        always {
            sh 'make clean'
        }
        success {
            slackSend(channel: SLACK_CHANNEL, attachments: [SLACK_MESSAGE << 
                [
                    "color": "#36a64f",
                    "title": "Build succeeded :rocket:",
                ]
            ])
        }
        failure {
            slackSend(channel: SLACK_CHANNEL, attachments: [SLACK_MESSAGE << 
                [
                    "color": "#D53030",
                    "title": "Build failed :fire:",
                ]
            ])
        }
    }
}

