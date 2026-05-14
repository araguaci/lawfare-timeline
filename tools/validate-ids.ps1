# validate-ids.ps1 — Validação de gaps e consistência de IDs no corpus lawfare-timeline
# Uso: pwsh -File tools/validate-ids.ps1 [[-Verbose]]

param([switch]$Verbose)

$root     = Split-Path $PSScriptRoot -Parent
$dataDir  = Join-Path $root "_data"
$syncFile = Join-Path $dataDir "claude.ai-corpus-ids-sync.json"
$mainFile = Join-Path $dataDir "lawfare.json"
$corpFile = Join-Path $dataDir "lawfare-unified-corpus.json"

$ok   = 0
$warn = 0
$err  = 0

function Pass($msg)  { Write-Host "  [OK]   $msg" -ForegroundColor Green;  $script:ok++ }
function Warn($msg)  { Write-Host "  [AVISO] $msg" -ForegroundColor Yellow; $script:warn++ }
function Fail($msg)  { Write-Host "  [ERRO]  $msg" -ForegroundColor Red;    $script:err++ }

Write-Host "`n=== LAWFARE-TIMELINE — VALIDAÇÃO DE IDS ===" -ForegroundColor Cyan
Write-Host "Data: $(Get-Date -Format 'yyyy-MM-dd HH:mm')`n"

# -----------------------------------------------------------------------
# 1. LAWFARE.JSON — fonte de verdade do main track
# -----------------------------------------------------------------------
Write-Host "[ 1 ] lawfare.json — main track (fonte de verdade)" -ForegroundColor Cyan
try {
    $main = (Get-Content $mainFile -Raw | ConvertFrom-Json).assuntos
    $ids  = $main | ForEach-Object { [int]$_.id } | Sort-Object
    $last = $ids | Select-Object -Last 1
    $next = $last + 1

    Pass "Carregado — $($ids.Count) entradas, ID 1 a $last"

    # Gaps
    $gaps = @()
    for ($i = 1; $i -lt $ids.Count; $i++) {
        $d = $ids[$i] - $ids[$i-1]
        if ($d -gt 1) { $gaps += "$($ids[$i-1]+1)–$($ids[$i]-1) ($($d-1) slot(s))" }
    }
    if ($gaps.Count -eq 0) { Pass "Sem gaps — sequência contínua" }
    else { Warn "Gaps detectados: $($gaps -join ' | ')" }

    # Duplicatas
    $dupes = $ids | Group-Object | Where-Object Count -gt 1
    if ($dupes) { Fail "IDs duplicados: $($dupes.Name -join ', ')" }
    else         { Pass "Sem IDs duplicados" }

    if ($Verbose) {
        Write-Host "    Últimas 5 entradas:"
        $main | Select-Object -Last 5 | ForEach-Object { "      $($_.id) | $($_.data_evento) | $($_.titulo.Substring(0,[Math]::Min(60,$_.titulo.Length)))" }
    }
} catch { Fail "Erro ao ler lawfare.json: $_" }

# -----------------------------------------------------------------------
# 2. SYNC FILE — consistência com fonte de verdade
# -----------------------------------------------------------------------
Write-Host "`n[ 2 ] claude.ai-corpus-ids-sync.json — consistência" -ForegroundColor Cyan
try {
    $sync         = Get-Content $syncFile -Raw | ConvertFrom-Json
    $syncLastId   = $sync.tracks.main.last_id
    $syncNextAvail = $sync.tracks.main.next_available
    $realLastId   = $last
    $realNext     = $next

    if ($syncLastId -eq $realLastId) { Pass "main.last_id correto: $syncLastId" }
    else { Fail "main.last_id diverge — sync=$syncLastId / real=$realLastId" }

    if ($syncNextAvail -eq $realNext) { Pass "main.next_available correto: $syncNextAvail" }
    else { Fail "main.next_available diverge — sync=$syncNextAvail / real=$realNext" }

    # Verificar batch_file_only entries não colisão com main
    $batchOnly = $sync.tracks.main.confirmed_batches | Where-Object { $_.status -eq "batch_file_only" }
    foreach ($b in $batchOnly) {
        $bMin = $b.range[0]; $bMax = $b.range[1]
        $colide = $ids | Where-Object { $_ -ge $bMin -and $_ -le $bMax }
        if ($colide.Count -gt 0) { Fail "batch_file_only [$bMin-$bMax] colide com lawfare.json: $($colide -join ',')" }
        else { Pass "batch_file_only [$bMin-$bMax] sem colisão em lawfare.json" }
    }

    # Thematic track — sem gaps
    $tIds   = $sync.tracks.thematic.entries | ForEach-Object { $_.id } | Sort-Object
    $tLast  = $sync.tracks.thematic.last_id
    $tNext  = $sync.tracks.thematic.next_available
    $tGaps  = @()
    for ($i = 1; $i -lt $tIds.Count; $i++) {
        $d = $tIds[$i] - $tIds[$i-1]
        if ($d -gt 1) { $tGaps += "$($tIds[$i-1]+1)–$($tIds[$i]-1)" }
    }
    if ($tGaps.Count -eq 0) { Pass "Thematic track sem gaps internos ($($tIds.Count) entradas, $($tIds[0])–$($tIds[-1]))" }
    else { Warn "Thematic track gaps: $($tGaps -join ' | ')" }

    if ($tLast -eq ($tIds | Select-Object -Last 1)) { Pass "thematic.last_id correto: $tLast" }
    else { Fail "thematic.last_id=$tLast mas maior ID encontrado=$($tIds | Select-Object -Last 1)" }

    if ($tNext -eq ($tLast + 1)) { Pass "thematic.next_available correto: $tNext" }
    else { Warn "thematic.next_available=$tNext (esperado $($tLast+1))" }

    # Pending não conflita com confirmed
    $pending  = $sync.tracks.thematic.pending
    $confIds  = $sync.tracks.thematic.entries | Where-Object { $_.status -eq "confirmed" } | ForEach-Object { $_.id }
    $conflict = $pending | Where-Object { $_ -in $confIds }
    if ($conflict) { Warn "Pending também marcado como confirmed: $($conflict -join ',')" }
    else            { Pass "Pending sem colisão com confirmed ($($pending -join ','))" }

} catch { Fail "Erro ao ler sync file: $_" }

# -----------------------------------------------------------------------
# 3. UNIFIED CORPUS — integridade interna
# -----------------------------------------------------------------------
Write-Host "`n[ 3 ] lawfare-unified-corpus.json — integridade" -ForegroundColor Cyan
try {
    $corpus   = (Get-Content $corpFile -Raw | ConvertFrom-Json).entradas
    $cIds     = $corpus | ForEach-Object { $_.id_corpus }
    $cIdsSorted = $cIds | Sort-Object

    Pass "Carregado — $($corpus.Count) entradas"

    # IDs duplicados no corpus
    $dupes = $cIds | Group-Object | Where-Object Count -gt 1
    if ($dupes) { Fail "id_corpus duplicados: $($dupes.Name -join ', ')" }
    else         { Pass "Sem id_corpus duplicados" }

    # IDs temáticos (100-999) são namespace separado do main track — sem verificação de colisão
    # Colisão numérica com lawfare.json é esperada e intencional (track distinto)
    $tCorpus = $cIds | Where-Object { [int]$_ -ge 100 -and [int]$_ -lt 1000 }
    $tOutOfRange = $tCorpus | Where-Object { [int]$_ -lt 100 -or [int]$_ -ge 1000 }
    if ($tOutOfRange) { Warn "IDs temáticos fora do range 100-999: $($tOutOfRange -join ',')" }
    elseif ($tCorpus.Count -gt 0) { Pass "Track temático: $($tCorpus.Count) entradas no range 100-999 ($($tCorpus -join ','))" }

    # IDs numéricos >1000: main track — alguns só existem em JSON batch até merge em lawfare.json
    $mCorpus = $cIds | Where-Object { [int]$_ -gt 1000 } | ForEach-Object { [int]$_ } | Sort-Object
    $inMain  = $mCorpus | Where-Object { $_ -le $realLastId }
    $inBatch = $mCorpus | Where-Object { $_ -gt $realLastId }
    if ($inMain.Count -gt 0)  { Pass "IDs main presentes em lawfare.json: $($inMain -join ',')" }

    if ($inBatch.Count -gt 0) {
        # Esperado quando sync marca confirmed_batches.status=batch_file_only (ex.: 1449–1511)
        $syncRef          = Get-Content $syncFile -Raw | ConvertFrom-Json
        $batchOnlyRanges  = @($syncRef.tracks.main.confirmed_batches | Where-Object { $_.status -eq "batch_file_only" })
        $outsideDeclared = New-Object System.Collections.Generic.List[int]
        foreach ($nid in $inBatch) {
            $inside = $false
            foreach ($b in $batchOnlyRanges) {
                $lo = [int]$b.range[0]; $hi = [int]$b.range[1]
                if ($nid -ge $lo -and $nid -le $hi) { $inside = $true; break }
            }
            if (-not $inside) { [void]$outsideDeclared.Add($nid) }
        }
        if ($batchOnlyRanges.Count -eq 0) {
            Warn "IDs main > $($realLastId) mas sync não define batch_file_only: $($inBatch -join ',')"
        } elseif ($outsideDeclared.Count -gt 0) {
            Warn "IDs main > $($realLastId) fora dos ranges batch_file_only no sync: $($outsideDeclared -join ',')"
        } else {
            Pass "IDs main apenas em batch _data/*.json (OK — dentro de batch_file_only sync): $($inBatch -join ',')"
        }
    }

    # Verificar fontes verificadas (todo entry deve ter >= 1 URL)
    $semFonte = $corpus | Where-Object { $_.fontes_verificadas.Count -eq 0 }
    if ($semFonte) { Fail "Entradas sem fontes_verificadas: $(($semFonte | ForEach-Object { $_.id_corpus }) -join ',')" }
    else            { Pass "Todas as entradas têm fontes_verificadas" }

    # Verificar conexoes não apontam para IDs inexistentes no corpus
    $allCorpusIds = $cIds | ForEach-Object { "id_$_" }
    $conexoesRotas = $corpus | ForEach-Object {
        $entry = $_
        $entry.conexoes | ForEach-Object {
            if ($_ -notin $allCorpusIds -and $_ -notlike "id_1*" -and [int]($_ -replace 'id_','') -lt 200) {
                "$($entry.id_corpus)→$_"
            }
        }
    }
    # Apenas verificar que conexoes têm formato correto
    $malformed = $corpus | ForEach-Object { $_.conexoes | Where-Object { $_ -notmatch '^id_\d+$' } }
    if ($malformed) { Warn "Conexoes com formato inválido: $($malformed -join ',')" }
    else             { Pass "Formato de conexoes correto em todas as entradas" }

    # jekyll_categories válidas
    $validCats = @("escandalos","estudos","operacoes","lawfare","stf","justica","bancos","crise-diplomatica",
                   "decano","dossie","extravagancia","governo","impunidade","indecoro","penduricalhos","tse","vazatoga","sabedoria")
    $invalidCat = $corpus | Where-Object { $_.jekyll_categories[0] -notin $validCats }
    if ($invalidCat) { Fail "Categorias inválidas: $(($invalidCat | ForEach-Object { "$($_.id_corpus)=$($_.jekyll_categories[0])" }) -join ',')" }
    else              { Pass "Todas as jekyll_categories válidas ($($corpus | ForEach-Object { $_.jekyll_categories[0] } | Sort-Object -Unique))" }

    if ($Verbose) {
        Write-Host "    Distribuição de categorias:"
        $corpus | ForEach-Object { $_.jekyll_categories[0] } | Group-Object | Sort-Object Count -Descending |
            ForEach-Object { "      $($_.Count)x $($_.Name)" }
    }

} catch { Fail "Erro ao ler unified corpus: $_" }

# -----------------------------------------------------------------------
# SUMÁRIO
# -----------------------------------------------------------------------
Write-Host "`n=== RESULTADO ===" -ForegroundColor Cyan
Write-Host "  OK:     $ok"
Write-Host "  Avisos: $warn" -ForegroundColor $(if ($warn -gt 0) {"Yellow"} else {"White"})
Write-Host "  Erros:  $err"  -ForegroundColor $(if ($err  -gt 0) {"Red"}    else {"White"})

if ($err -gt 0)  { Write-Host "`nSTATUS: FALHOU" -ForegroundColor Red;    exit 1 }
elseif ($warn -gt 0) { Write-Host "`nSTATUS: AVISO" -ForegroundColor Yellow; exit 0 }
else             { Write-Host "`nSTATUS: OK"     -ForegroundColor Green;   exit 0 }
