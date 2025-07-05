pipeline{

    agent any
    
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'eastern-period-463504-e2'
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
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
                    echo 'Making a virtual environment...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install  dvc
                    '''
                }
            }
        }

        stage('DVC Pull'){
            steps{
                withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
                    script{
                        echo 'DVC Pul....'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }

        stage('Build and Push Image to GCR'){
            steps{
                withCredentials([
                    file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' ),
                    string(credentialsId: 'comet-ml', variable: 'COMET_ML_KEY')
                ]){
                    script{
                        echo 'Build and Push Image to GCR'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}

                        echo -n "${COMET_ML_KEY}" > .comet_secret

                        DOCKER_BUILDKIT=1 docker build \
                            --secret id=comet_ml_key,src=.comet_secret \
                            --build-arg GCP_PROJECT=${GCP_PROJECT} \
                            -t gcr.io/${GCP_PROJECT}/anime-recommendation-project:latest .

                        rm .comet_secret

                        gcloud auth configure-docker --quiet

                        docker push gcr.io/${GCP_PROJECT}/anime-recommendation-project:latest
                        '''
                    }
                }
            }
        }

        stage('Deploying to Kubernetes'){
            steps{
                withCredentials([
                    file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' ),
                    string(credentialsId: 'comet-ml', variable: 'COMET_ML_KEY')
                ]){
                    script{
                        echo 'Deploying to Kubernetes'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials anime-cluster --region us-central1
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }

    }
}