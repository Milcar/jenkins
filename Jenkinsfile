pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -c "from pathlib import Path; import shutil; [shutil.rmtree(p) for p in ('reports/unittest', 'reports/behave') if Path(p).exists()]"
                            python3 -m pip install -r requirements.txt
                            python3 -c "from pathlib import Path; [Path(p).mkdir(parents=True, exist_ok=True) for p in ('reports/unittest', 'reports/behave')]"
                        '''
                    } else {
                        bat '''
                            py -3 -c "from pathlib import Path; import shutil; [shutil.rmtree(p) for p in ('reports/unittest', 'reports/behave') if Path(p).exists()]"
                            py -3 -m pip install -r requirements.txt
                            py -3 -c "from pathlib import Path; [Path(p).mkdir(parents=True, exist_ok=True) for p in ('reports/unittest', 'reports/behave')]"
                        '''
                    }
                }
            }
        }

        stage('Unit tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    script {
                        if (isUnix()) {
                            sh 'python3 -m xmlrunner discover -s tests -o reports/unittest'
                        } else {
                            bat 'py -3 -m xmlrunner discover -s tests -o reports/unittest'
                        }
                    }
                }
            }
        }

        stage('Acceptance tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    script {
                        if (isUnix()) {
                            sh 'python3 -m behave features --junit --junit-directory reports/behave'
                        } else {
                            bat 'py -3 -m behave features --junit --junit-directory reports/behave'
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/**/*.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}
