# Script PowerShell para iniciar os serviços
Write-Host "🚀 Iniciando serviços do protótipo..." -ForegroundColor Green

# Verificar se Docker está rodando
Write-Host "`n📦 Verificando Docker..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✅ Docker está rodando" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker não está rodando!" -ForegroundColor Red
    Write-Host "Por favor, inicie o Docker Desktop primeiro." -ForegroundColor Yellow
    exit 1
}

# Iniciar containers
Write-Host "`n🔧 Iniciando containers..." -ForegroundColor Yellow
docker-compose up -d

# Aguardar alguns segundos
Start-Sleep -Seconds 5

# Verificar status
Write-Host "`n📊 Status dos containers:" -ForegroundColor Yellow
docker-compose ps

# Verificar se frontend está acessível
Write-Host "`n🌐 Testando acesso ao frontend..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ Frontend está acessível em http://localhost:3000" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Frontend ainda não está respondendo. Aguarde alguns segundos..." -ForegroundColor Yellow
    Write-Host "Verifique os logs com: docker-compose logs -f frontend" -ForegroundColor Cyan
}

Write-Host "`n✨ Serviços iniciados!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan

