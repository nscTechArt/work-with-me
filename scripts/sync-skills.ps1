<#
.SYNOPSIS
Syncs installable skills from this repository to local Windows agent configurations.

.DESCRIPTION
Scans top-level skills/<name>/SKILL.md directories under this repository and:
1. Creates or updates per-skill NTFS directory junctions in each junction target directory (default: ~/.agents/skills,
   which ~/.claude/skills shares via junction), removing only stale or broken junctions pointing into this repository
   while leaving unrelated third-party skills and directories untouched.
2. Ensures Antigravity's ~/.gemini/config/skills.json registers this repository's skills/ directory directly (Antigravity
   skips NTFS junctions inside ~/.gemini/config/skills, so it reads the real repo folder via skills.json).
#>
[CmdletBinding()]
param(
    [string[]]$Targets = @(
        (Join-Path $env:USERPROFILE '.agents\skills')
    ),
    [string]$AntigravitySkillsJson = (Join-Path $env:USERPROFILE '.gemini\config\skills.json'),
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-NormalizedPath {
    param([Parameter(Mandatory)][string]$Path)
    $cleaned = $Path -replace '^\\\\\?\\', ''
    return [System.IO.Path]::GetFullPath($cleaned).TrimEnd('\')
}

function Get-ReparseTarget {
    param([Parameter(Mandatory)][System.IO.FileSystemInfo]$Item)
    if (-not ($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
        return $null
    }
    $raw = if ($Item.Target -is [System.Array]) { $Item.Target[0] } else { [string]$Item.Target }
    if ([string]::IsNullOrWhiteSpace($raw)) {
        return $null
    }
    try {
        return Get-NormalizedPath -Path $raw
    } catch {
        return ($raw -replace '^\\\\\?\\', '').TrimEnd('\')
    }
}

function Remove-DirectorySafely {
    param([Parameter(Mandatory)][System.IO.FileSystemInfo]$Item)
    # Never run Remove-Item -Recurse on a junction or symlink, as Windows PowerShell 5.1 can follow it into the target.
    if ($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
        [System.IO.Directory]::Delete($Item.FullName)
    } else {
        Remove-Item -LiteralPath $Item.FullName -Recurse -Force
    }
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$skillsRoot = Get-NormalizedPath -Path (Join-Path $repoRoot 'skills')
if (-not (Test-Path -LiteralPath $skillsRoot -PathType Container)) {
    throw "Skills root not found: $skillsRoot"
}

$repoSkills = [ordered]@{}
$skillDirs = Get-ChildItem -LiteralPath $skillsRoot -Directory | Sort-Object Name
foreach ($dir in $skillDirs) {
    if (-not (Test-Path -LiteralPath (Join-Path $dir.FullName 'SKILL.md') -PathType Leaf)) {
        continue
    }
    $repoSkills[$dir.Name] = Get-NormalizedPath -Path $dir.FullName
}

if ($repoSkills.Count -eq 0) {
    throw "No skills found under $skillsRoot"
}

$skillsRootPrefix = "$skillsRoot\"
$prefix = if ($DryRun) { '[DryRun] ' } else { '' }

foreach ($rawTarget in $Targets) {
    $targetRoot = Get-NormalizedPath -Path $rawTarget
    $created = New-Object System.Collections.Generic.List[string]
    $updated = New-Object System.Collections.Generic.List[string]
    $removed = New-Object System.Collections.Generic.List[string]
    $unchanged = 0

    if (-not (Test-Path -LiteralPath $targetRoot)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
        }
    }

    foreach ($skillName in $repoSkills.Keys) {
        $srcPath = $repoSkills[$skillName]
        $dstPath = Join-Path $targetRoot $skillName
        $existing = Get-Item -LiteralPath $dstPath -Force -ErrorAction SilentlyContinue

        if ($null -eq $existing) {
            $created.Add($skillName)
            if (-not $DryRun) {
                New-Item -ItemType Junction -Path $dstPath -Target $srcPath | Out-Null
            }
            continue
        }

        $existingTarget = Get-ReparseTarget -Item $existing
        if ($null -ne $existingTarget -and $existingTarget -ieq $srcPath) {
            $unchanged++
            continue
        }

        $updated.Add($skillName)
        if (-not $DryRun) {
            Remove-DirectorySafely -Item $existing
            New-Item -ItemType Junction -Path $dstPath -Target $srcPath | Out-Null
        }
    }

    if (Test-Path -LiteralPath $targetRoot) {
        $entries = Get-ChildItem -LiteralPath $targetRoot -Directory -Force -ErrorAction SilentlyContinue
        foreach ($entry in $entries) {
            if ($repoSkills.Contains($entry.Name)) {
                continue
            }

            $entryTarget = Get-ReparseTarget -Item $entry
            $pointsIntoRepo = ($null -ne $entryTarget) -and $entryTarget.StartsWith($skillsRootPrefix, [System.StringComparison]::OrdinalIgnoreCase)

            if ($pointsIntoRepo) {
                $removed.Add($entry.Name)
                if (-not $DryRun) {
                    Remove-DirectorySafely -Item $entry
                }
            }
        }
    }

    Write-Output "${prefix}Target: $targetRoot"
    if ($created.Count -gt 0) { Write-Output "  Created ($($created.Count)): $($created -join ', ')" }
    if ($updated.Count -gt 0) { Write-Output "  Updated ($($updated.Count)): $($updated -join ', ')" }
    if ($removed.Count -gt 0) { Write-Output "  Removed ($($removed.Count)): $($removed -join ', ')" }
    Write-Output "  Unchanged: $unchanged"
}

if (-not [string]::IsNullOrWhiteSpace($AntigravitySkillsJson)) {
    $agyJsonPath = Get-NormalizedPath -Path $AntigravitySkillsJson
    $skillsRootPosix = $skillsRoot -replace '\\', '/'
    $config = $null
    if (Test-Path -LiteralPath $agyJsonPath -PathType Leaf) {
        $rawJson = Get-Content -LiteralPath $agyJsonPath -Raw
        if (-not [string]::IsNullOrWhiteSpace($rawJson)) {
            $config = $rawJson | ConvertFrom-Json
        }
    }

    $entries = New-Object System.Collections.Generic.List[object]
    $alreadyRegistered = $false
    if ($null -ne $config -and $config.PSObject.Properties['entries'] -and $null -ne $config.entries) {
        foreach ($entry in $config.entries) {
            $entries.Add($entry)
            if ($entry.PSObject.Properties['path'] -and -not [string]::IsNullOrWhiteSpace([string]$entry.path)) {
                try {
                    if ((Get-NormalizedPath -Path ([string]$entry.path)) -ieq $skillsRoot) {
                        $alreadyRegistered = $true
                    }
                } catch {
                    # Ignore non-filesystem or relative paths owned by other entries.
                }
            }
        }
    }

    if ($alreadyRegistered) {
        Write-Output "${prefix}Antigravity config: $agyJsonPath (unchanged)"
    } else {
        $entries.Add([pscustomobject]@{ path = $skillsRootPosix })
        if ($null -eq $config) {
            $config = [pscustomobject]@{ entries = @($entries) }
        } elseif ($config.PSObject.Properties['entries']) {
            $config.entries = @($entries)
        } else {
            $config | Add-Member -NotePropertyName 'entries' -NotePropertyValue @($entries)
        }

        if (-not $DryRun) {
            $parentDir = Split-Path -Parent $agyJsonPath
            if (-not (Test-Path -LiteralPath $parentDir)) {
                New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
            }
            $jsonOut = $config | ConvertTo-Json -Depth 10
            [System.IO.File]::WriteAllText($agyJsonPath, "$jsonOut`n", [System.Text.UTF8Encoding]::new($false))
        }
        Write-Output "${prefix}Antigravity config: $agyJsonPath (registered $skillsRootPosix)"
    }
}
