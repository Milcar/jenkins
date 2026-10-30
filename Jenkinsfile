pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\lumad\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
    }

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
                            "%PYTHON%" -c "from pathlib import Path; import shutil; [shutil.rmtree(p) for p in ('reports/unittest', 'reports/behave') if Path(p).exists()]"
                            "%PYTHON%" -m pip install -r requirements.txt
                            "%PYTHON%" -c "from pathlib import Path; [Path(p).mkdir(parents=True, exist_ok=True) for p in ('reports/unittest', 'reports/behave')]"
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
                            bat '"%PYTHON%" -m xmlrunner discover -s tests -o reports/unittest'
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
                            bat '"%PYTHON%" -m behave features --junit --junit-directory reports/behave'
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
