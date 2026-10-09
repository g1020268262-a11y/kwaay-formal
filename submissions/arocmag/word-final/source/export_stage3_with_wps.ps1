param(
    [string]$RunName = 'stage3-render-final'
)

$ErrorActionPreference = 'Stop'

$wordRoot = Split-Path -Parent $PSScriptRoot
$docx = Join-Path $wordRoot 'K-Waay-AROCMAG-submission-stage3-polished.docx'
$qaDir = Join-Path $wordRoot (Join-Path 'qa' $RunName)
$pdf = Join-Path $qaDir 'K-Waay-AROCMAG-submission-stage3-polished-verified.pdf'
New-Item -ItemType Directory -Path $qaDir -Force | Out-Null

$app = New-Object -ComObject KWPS.Application
$app.Visible = $false
$app.DisplayAlerts = 0
$doc = $null
try {
    $doc = $app.Documents.Open($docx, $false, $true)
    $doc.Repaginate()
    if (Test-Path -LiteralPath $pdf) {
        Remove-Item -LiteralPath $pdf -Force
    }
    $doc.ExportAsFixedFormat($pdf, 17)
    [pscustomobject]@{
        Pages = $doc.ComputeStatistics(2)
        Words = $doc.ComputeStatistics(0)
        Paragraphs = $doc.Paragraphs.Count
        Tables = $doc.Tables.Count
        InlineShapes = $doc.InlineShapes.Count
        OMaths = $doc.OMaths.Count
        Sections = $doc.Sections.Count
        PDF = $pdf
    } | ConvertTo-Json -Depth 3
}
finally {
    if ($null -ne $doc) {
        $doc.Close($false)
    }
    $app.Quit()
    [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($app) | Out-Null
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
