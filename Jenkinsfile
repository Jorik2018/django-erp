pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        SERVICE_ID = 'django-erp'
        SERVICE_NAME = 'Django ERP'
        SERVICE_DESCRIPTION = 'Django ERP Application'

        DEPLOY_DIR = 'D:\\apps\\django-erp'

        PORT = '7784'
        BASE_PATH = '/django'
        DEFENDER_REDIS_URL = credentials('REDIS-DEVELOP')
        
    }

    stages {

        // ============================================================
        // 1. Verificar entorno
        // ============================================================

        stage('Check Environment') {
            steps {
                bat '''
                    SET PATH=%PYTHON_HOME%;%PYTHON_HOME%\\Scripts;%PATH%

                    echo ==========================================
                    echo PYTHON
                    echo ==========================================

                    "%PYTHON_HOME%\\python.exe" --version
                    "%PYTHON_HOME%\\python.exe" -m pip --version

                    echo ==========================================
                    echo GIT
                    echo ==========================================

                    git --version
                '''
            }
        }


        // ============================================================
        // 2. Detener servicio anterior
        // ============================================================

        stage('Stop Service') {
            steps {
                bat '''
                    echo ==========================================
                    echo Stopping Django ERP
                    echo ==========================================

                    "%PYTHON_HOME%\\python.exe" ^
                        "%SERVICE_MANAGER%" ^
                        stop ^
                        "%SERVICE_ID%"

                    exit /B 0
                '''
            }
        }


        // ============================================================
        // 3. Copiar aplicación
        // ============================================================

        stage('Deploy Files') {
            steps {
                powershell '''
                    $source = $env:WORKSPACE
                    $destination = $env:DEPLOY_DIR

                    if (-not (Test-Path $destination)) {
                        New-Item `
                            -ItemType Directory `
                            -Path $destination `
                            -Force | Out-Null
                    }

                    robocopy `
                        $source `
                        $destination `
                        /MIR `
                        /XD ".git" ".venv" "__pycache__" ".pytest_cache" "staticfiles" `
                        /XF ".env" "*.pyc"

                    $code = $LASTEXITCODE

                    # Robocopy 0-7 = OK
                    if ($code -gt 7) {
                        throw "Robocopy failed with exit code $code"
                    }

                    exit 0
                '''
            }
        }


        // ============================================================
        // 4. Crear virtualenv de producción
        // ============================================================

        stage('Prepare Python Environment') {
            steps {
                bat '''
                    echo ==========================================
                    echo Preparing Python virtual environment
                    echo ==========================================

                    if not exist "%DEPLOY_DIR%\\.venv" (
                        "%PYTHON_HOME%\\python.exe" ^
                            -m venv ^
                            "%DEPLOY_DIR%\\.venv"
                    )

                    "%DEPLOY_DIR%\\.venv\\Scripts\\python.exe" ^
                        -m pip install ^
                        --upgrade pip
                '''
            }
        }


        // ============================================================
        // 5. Instalar Poetry
        // ============================================================

        stage('Install Poetry') {
            steps {
                bat '''
                    "%DEPLOY_DIR%\\.venv\\Scripts\\python.exe" ^
                        -m pip install ^
                        poetry
                '''
            }
        }


        // ============================================================
        // 6. Instalar dependencias
        // ============================================================

        stage('Install Dependencies') {
            steps {
                bat '''
                    cd /D "%DEPLOY_DIR%"

                    SET POETRY_VIRTUALENVS_CREATE=false

                    "%DEPLOY_DIR%\\.venv\\Scripts\\poetry.exe" ^
                        install ^
                        --only main ^
                        --no-interaction ^
                        --no-ansi

                    if errorlevel 1 (
                        echo ERROR: Poetry install failed.
                        exit /B 1
                    )
                '''
            }
        }


        // ============================================================
        // 7. Verificar Django + Waitress
        // ============================================================

        stage('Verify Application') {
            steps {
                bat '''
                    cd /D "%DEPLOY_DIR%"

                    SET "BASE_PATH=%BASE_PATH%"

                    echo ==========================================
                    echo PYTHON
                    echo ==========================================

                    "%DEPLOY_DIR%\\.venv\\Scripts\\python.exe" --version

                    echo ==========================================
                    echo DJANGO
                    echo ==========================================

                    "%DEPLOY_DIR%\\.venv\\Scripts\\python.exe" ^
                        -m django ^
                        --version

                    echo ==========================================
                    echo DJANGO CHECK
                    echo ==========================================

                    "%DEPLOY_DIR%\\.venv\\Scripts\\python.exe" ^
                        manage.py ^
                        check

                    if errorlevel 1 (
                        echo ERROR: Django check failed.
                        exit /B 1
                    )

                    echo ==========================================
                    echo WAITRESS
                    echo ==========================================

                    "%DEPLOY_DIR%\\.venv\\Scripts\\waitress-serve.exe" ^
                        --help > nul

                    if errorlevel 1 (
                        echo ERROR: Waitress is not installed.
                        exit /B 1
                    )

                    echo Django ERP OK
                '''
            }
        }


        // ============================================================
        // 8. Migraciones
        // ============================================================

        stage('Run Migrations') {
            steps {
                bat '''
                    cd /D "%DEPLOY_DIR%"

                    SET "BASE_PATH=%BASE_PATH%"

                    echo ==========================================
                    echo Running Django migrations
                    echo ==========================================

                    "%DEPLOY_DIR%\\.venv\\Scripts\\python.exe" ^
                        manage.py ^
                        migrate ^
                        --noinput

                    if errorlevel 1 (
                        echo ERROR: Django migrations failed.
                        exit /B 1
                    )
                '''
            }
        }


        // ============================================================
        // 9. Collect Static
        // ============================================================

        stage('Collect Static') {
            steps {
                bat '''
                    cd /D "%DEPLOY_DIR%"

                    SET "BASE_PATH=%BASE_PATH%"

                    echo ==========================================
                    echo Collecting static files
                    echo ==========================================

                    "%DEPLOY_DIR%\\.venv\\Scripts\\python.exe" ^
                        manage.py ^
                        collectstatic ^
                        --noinput

                    if errorlevel 1 (
                        echo ERROR: collectstatic failed.
                        exit /B 1
                    )
                '''
            }
        }


stage('Configure Service') {
    steps {
        withCredentials([
            string(
                credentialsId: 'VAULT_TOKEN',
                variable: 'VAULT_TOKEN'
            ),
            string(
                credentialsId: 'REDIS-DEVELOP',
                variable: 'DEFENDER_REDIS_URL'
            )
        ]) {
            bat '''
                echo ==========================================
                echo Configuring Django ERP Windows service
                echo ==========================================

                "%PYTHON_HOME%\\python.exe" "%SERVICE_MANAGER%" install ^
                    "%SERVICE_ID%" ^
                    "%DEPLOY_DIR%" ^
                    --name "%SERVICE_NAME%" ^
                    --description "%SERVICE_DESCRIPTION%" ^
                    --type rust ^
                    --executable "%DEPLOY_DIR%\\.venv\\Scripts\\waitress-serve.exe" ^
                    --args "--listen=127.0.0.1:%PORT% config.wsgi:application" ^
                    --env "BASE_PATH=%BASE_PATH%" ^
                    --env "DEFENDER_REDIS_URL=%DEFENDER_REDIS_URL%" ^
                    --env "VAULT_ADDR=%VAULT_ADDR%" ^
                    --env "CSRF_TRUSTED_ORIGINS=%CSRF_TRUSTED_ORIGINS%" ^
                    --env "VAULT_TOKEN=%VAULT_TOKEN%"

                if errorlevel 1 (
                    echo ERROR: Service configuration failed
                    exit /B 1
                )
            '''
        }
    }
}


        // ============================================================
        // 11. Arrancar servicio
        // ============================================================

        stage('Start Service') {
            steps {
                bat '''
                    echo ==========================================
                    echo Starting Django ERP
                    echo ==========================================

                    "%PYTHON_HOME%\\python.exe" ^
                        "%SERVICE_MANAGER%" ^
                        start ^
                        "%SERVICE_ID%"

                    if errorlevel 1 (
                        echo ERROR: Could not start Django ERP.
                        exit /B 1
                    )
                '''
            }
        }


        // ============================================================
        // 12. Verificar servicio
        // ============================================================

        stage('Verify Service') {
            steps {
                bat '''
                    echo ==========================================
                    echo Checking Windows service
                    echo ==========================================

                    "%PYTHON_HOME%\\python.exe" ^
                        "%SERVICE_MANAGER%" ^
                        status ^
                        "%SERVICE_ID%"

                    if errorlevel 1 (
                        echo ERROR: Django ERP service is not running.
                        exit /B 1
                    )

                    echo ==========================================
                    echo Checking port %PORT%
                    echo ==========================================

                    netstat -ano | findstr ":%PORT%"

                    if errorlevel 1 (
                        echo ERROR: Django ERP is not listening on port %PORT%.
                        exit /B 1
                    )
                '''
            }
        }


        // ============================================================
        // 13. Health Check
        // ============================================================

        stage('Health Check') {
            steps {
                powershell '''
                    # IMPORTANTE:
                    # Este es el endpoint INTERNO de Django.
                    #
                    # Nginx:
                    #   /erp/... -> 127.0.0.1:7748/...
                    #
                    # Por eso NO usamos /erp aqui.

                    $url = "http://127.0.0.1:$env:PORT/auth/sign-in/"

                    $maxAttempts = 10

                    for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {

                        Write-Host "Health check $attempt/$maxAttempts"
                        Write-Host $url

                        try {

                            $response = Invoke-WebRequest `
                                -UseBasicParsing `
                                -Uri $url `
                                -TimeoutSec 5

                            if ($response.StatusCode -eq 200) {

                                Write-Host "Django ERP OK"

                                exit 0
                            }

                            Write-Host "HTTP status: $($response.StatusCode)"
                        }
                        catch {

                            Write-Host "Django ERP aun no disponible."
                            Write-Host $_.Exception.Message
                        }

                        Start-Sleep -Seconds 3
                    }

                    throw "Django ERP no respondio al health check."
                '''
            }
        }
    }


    post {
        success {
            echo '=========================================='
            echo 'Django ERP desplegado correctamente.'
            echo 'Puerto interno: 7748'
            echo 'Base path publico: /erp'
            echo 'Nginx debe publicar: https://DOMINIO/erp/'
            echo '=========================================='
        }

        failure {
            echo '=========================================='
            echo 'Fallo desplegando Django ERP.'
            echo '=========================================='
        }
    }
}