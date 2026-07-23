param([string]$Target="agents", [string]$Scope="global")
python -m companion_vault.cli skill-install --target $Target --scope $Scope
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
