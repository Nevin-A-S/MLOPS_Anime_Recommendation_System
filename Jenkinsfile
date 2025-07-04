pipeline{

    agent any
    
    enviornment{
        VENV_DIR = 'venv'
    }

    stages{
        stage('cloning from github'){
            steps{
                script{
                    echo 'Cloning from github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Nevin-A-S/MLOPS_Anime_Recommendation_System']])
                }
            }
        }
        stage('Creating a virtual env'){
            steps{
                script{
                    echo 'creating venv'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . /${VENV_DIR}/bin/activate
                    pip install -e .
                    pip install dvc
                    '''
                }
            }
        }

        stage('DVC PULL'){
            steps{
                withCredentials([file(credentialsId:'gcp-key',variable:'GOOGLE_APPLICATION_CREDENTIALS')])
                script{
                    echo 'dvc pull'
                    sh '''
                    . /${VENV_DIR}/bin/activate
                    dvc pull
                    '''
                }
            }
        }
    }
}