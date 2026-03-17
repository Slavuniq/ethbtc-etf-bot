$b="C:\ai-tryon-bot"
function WS($t){Write-Host ">>> $t" -ForegroundColor Cyan}
function WO($t){Write-Host " OK $t" -ForegroundColor Green}
Clear-Host
Write-Host "==============================" -ForegroundColor Magenta
Write-Host "  AI Try-On Bot - Установка   " -ForegroundColor Magenta
Write-Host "==============================" -ForegroundColor Magenta
WS "Создаю папки..."
"persons","garments","results"|%{New-Item -ItemType Directory -Force -Path "$b\photos\$_"|Out-Null}
WO "Папки созданы: $b"
Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  Введите данные для настройки бота    " -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Токен получить: откройте @BotFather в Telegram, напишите /newbot" -ForegroundColor White
Write-Host ""
$token=""
while($token.Length -lt 30){$token=Read-Host "  Введите BOT_TOKEN";if($token.Length -lt 30){Write-Host "  Слишком короткий, попробуйте ещё раз" -ForegroundColor Red}}
Write-Host ""
Write-Host "  Ваш ID: напишите @userinfobot в Telegram" -ForegroundColor White
Write-Host ""
$aid=""
while($aid -notmatch "^\d+$"){$aid=Read-Host "  Введите ваш Telegram ID (только цифры)";if($aid -notmatch "^\d+$"){Write-Host "  Только цифры!" -ForegroundColor Red}}
"BOT_TOKEN=$token`r`nADMIN_IDS=$aid`r`nFREE_TRIES=999`r`nREFERRAL_BONUS=10"|Set-Content "$b\.env" -Encoding UTF8
WO ".env создан"
WS "Устанавливаю зависимости (1-3 минуты, ждите)..."
Set-Location $b
$py=$null
foreach($c in @("python","py","python3")){try{$v=&$c --version 2>&1;if($v -match "Python"){$py=$c;break}}catch{}}
if($null -eq $py){Write-Host "Python не найден!" -ForegroundColor Red;Read-Host "Нажмите Enter";exit 1}
&$py -m pip install --quiet --upgrade pip
&$py -m pip install --quiet -r requirements.txt
WO "Зависимости установлены!"
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ГОТОВО! Запускаю бота...             " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Откройте Telegram, найдите вашего бота и напишите /start" -ForegroundColor White
Write-Host "  Остановить бота: нажмите Ctrl+C" -ForegroundColor Gray
Write-Host ""
&$py bot.py
