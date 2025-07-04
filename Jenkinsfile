
pipeline{
    agent any
    stages{
        stage{
            script{
                echo 'Cloning from github'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Nevin-A-S/MLOPS_Anime_Recommendation_System']])

            }
        }
    }
}