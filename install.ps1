param(
    [string]$Version = "",
    [string]$InstallDir = ""
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

if ([string]::IsNullOrWhiteSpace($Version)) {
    $Version = if ($env:PERSONADOCK_VERSION) { $env:PERSONADOCK_VERSION } else { "latest" }
}
if ([string]::IsNullOrWhiteSpace($InstallDir)) {
    $InstallDir = if ($env:PERSONADOCK_INSTALL_DIR) {
        $env:PERSONADOCK_INSTALL_DIR
    } else {
        Join-Path $env:LOCALAPPDATA "Programs\PersonaDock"
    }
}

$repository = "cuteyuchen/PersonaDock"
$asset = "personadock-windows-x86_64.zip"

if ($Version -eq "latest") {
    $baseUrl = "https://github.com/$repository/releases/latest/download"
} else {
    if (-not $Version.StartsWith("v")) {
        $Version = "v$Version"
    }
    $baseUrl = "https://github.com/$repository/releases/download/$Version"
}

if ($PSVersionTable.PSVersion.Major -lt 7) {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
}

$tempDir = Join-Path ([IO.Path]::GetTempPath()) ("personadock-" + [Guid]::NewGuid().ToString("N"))
$archivePath = Join-Path $tempDir $asset
$checksumsPath = Join-Path $tempDir "SHA256SUMS"

try {
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

    Write-Host "Downloading $asset..."
    Invoke-WebRequest -UseBasicParsing -Uri "$baseUrl/$asset" -OutFile $archivePath
    Invoke-WebRequest -UseBasicParsing -Uri "$baseUrl/SHA256SUMS" -OutFile $checksumsPath

    $checksumLine = Get-Content $checksumsPath | Where-Object {
        $_ -match "^[0-9a-fA-F]{64}\s+\*?$([Regex]::Escape($asset))$"
    } | Select-Object -First 1

    if (-not $checksumLine) {
        throw "SHA256SUMS does not contain $asset."
    }

    $expected = ($checksumLine -split "\s+")[0].ToLowerInvariant()
    $actual = (Get-FileHash -Algorithm SHA256 -Path $archivePath).Hash.ToLowerInvariant()
    if ($actual -ne $expected) {
        throw "Checksum verification failed for $asset."
    }

    $extractDir = Join-Path $tempDir "extracted"
    Expand-Archive -Path $archivePath -DestinationPath $extractDir -Force
    $sourceExe = Join-Path $extractDir "personadock.exe"
    if (-not (Test-Path $sourceExe -PathType Leaf)) {
        throw "The release archive does not contain personadock.exe."
    }

    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    $destinationExe = Join-Path $InstallDir "personadock.exe"
    Copy-Item -Path $sourceExe -Destination $destinationExe -Force

    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $pathEntries = @($userPath -split ";" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    if ($pathEntries -notcontains $InstallDir) {
        $newUserPath = (($pathEntries + $InstallDir) -join ";")
        [Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")
    }
    if (($env:Path -split ";") -notcontains $InstallDir) {
        $env:Path = "$InstallDir;$env:Path"
    }

    & $destinationExe --help | Out-Null
    Write-Host "PersonaDock installed to $destinationExe"
    Write-Host "Open a new terminal and run: personadock --help"
}
finally {
    if (Test-Path $tempDir) {
        Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
