[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$TargetRoot = (Join-Path ([Environment]::GetFolderPath('UserProfile')) '.agents\skills'),
    [ValidateSet('officecli', 'officecli-docx', 'officecli-thesis-gate')]
    [string[]]$Skill = @('officecli', 'officecli-docx', 'officecli-thesis-gate')
)

$ErrorActionPreference = 'Stop'
$skillNames = @($Skill | Select-Object -Unique)
if ($skillNames.Count -eq 0) {
    throw 'Select at least one skill.'
}
$sourceRoot = Join-Path $PSScriptRoot 'skills'
$resolvedTargetRoot = [IO.Path]::GetFullPath($TargetRoot)
$backupRoot = Join-Path (Split-Path -Parent $resolvedTargetRoot) 'skill-backups'
$backupRun = Join-Path $backupRoot ([DateTime]::Now.ToString('yyyyMMdd-HHmmss-fff') + '-' + [Guid]::NewGuid().ToString('N').Substring(0, 8))

# Validate every source before changing any installed skill.
foreach ($skillName in $skillNames) {
    $source = [IO.Path]::GetFullPath((Join-Path $sourceRoot $skillName))
    $target = [IO.Path]::GetFullPath((Join-Path $resolvedTargetRoot $skillName))
    if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md') -PathType Leaf)) {
        throw "Incomplete package: $skillName/SKILL.md is missing."
    }
    if ($target.Equals($source, [StringComparison]::OrdinalIgnoreCase) -or
        $target.StartsWith($source + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase) -or
        $source.StartsWith($target + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Source and installation paths must not overlap: $skillName"
    }
}
if ($skillNames -contains 'officecli-thesis-gate') {
    foreach ($scriptName in @('prepare_drawio_svg.py', 'style_drawio_svg.py')) {
        if (-not (Test-Path -LiteralPath (Join-Path $sourceRoot "officecli-thesis-gate\scripts\$scriptName") -PathType Leaf)) {
            throw "Incomplete package: $scriptName is missing."
        }
    }
}

foreach ($skillName in $skillNames) {
    $source = Join-Path $sourceRoot $skillName
    $target = [IO.Path]::GetFullPath((Join-Path $resolvedTargetRoot $skillName))
    # Check the absolute move target stays within the explicitly selected root.
    if (-not $target.StartsWith($resolvedTargetRoot.TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Installation target escapes TargetRoot: $target"
    }
    if (Test-Path -LiteralPath $target) {
        $existing = Get-Item -LiteralPath $target -Force
        if ($existing.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw "Existing skill is a symlink or junction. Install into a regular directory instead: $target"
        }
    }
    if ($PSCmdlet.ShouldProcess($target, 'Back up existing skill, then install package snapshot')) {
        New-Item -ItemType Directory -Path $resolvedTargetRoot -Force | Out-Null
        $backup = Join-Path $backupRun $skillName
        $hadExisting = Test-Path -LiteralPath $target
        if ($hadExisting) {
            New-Item -ItemType Directory -Path $backupRun -Force | Out-Null
            Move-Item -LiteralPath $target -Destination $backup
            Write-Output "Backup: $backup"
        }
        try {
            Copy-Item -LiteralPath $source -Destination $target -Recurse
        } catch {
            # Retain any partial copy for inspection; restore the previous skill.
            if (Test-Path -LiteralPath $target) {
                New-Item -ItemType Directory -Path $backupRun -Force | Out-Null
                Move-Item -LiteralPath $target -Destination (Join-Path $backupRun ($skillName + '-partial'))
            }
            if ($hadExisting) {
                Move-Item -LiteralPath $backup -Destination $target
            }
            throw
        }
        Write-Output "Installed: $target"
    }
}

if (-not $WhatIfPreference) {
    Write-Output 'Skills copied. Verify officecli --version on this computer separately.'
    Write-Output 'If the skills do not appear in Codex, restart Codex.'
}
