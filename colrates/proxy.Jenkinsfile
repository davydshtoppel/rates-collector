node('docker && python') {
    def proxy

    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
        dir('colrates') {
            sh 'pip install -r requirements.txt'
            sh 'python3 src/manage.py collectstatic --noinput'
            proxy = docker.build('davydstoppel/colrates-proxy', "-f proxy.Dockerfile .")
        }
    }

    stage('Run container') {
        def container = 'colrates-proxy'
        try {
            sh "docker stop $container"
        } catch (err) {
        }
        try {
            sh "docker rm $container"
        } catch (err) {
        }
        proxy.run("--name $container --network=depl1 -e RATES_HOST=${params.RATES_HOST} -e RATES_PORT=${params.RATES_PORT}")
    }

    stage('Push image') {
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            proxy.push('latest')
        }
    }
}