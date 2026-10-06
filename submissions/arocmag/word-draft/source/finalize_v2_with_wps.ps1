$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)))
$draftRoot = Join-Path $root 'submissions\arocmag\word-draft'
$docx = Join-Path $draftRoot 'manuscript\kwaay-arocmag-draft-v2.docx'
$pdf = Join-Path $draftRoot 'manuscript\kwaay-arocmag-review-v2.pdf'

$app = New-Object -ComObject KWPS.Application
$app.Visible = $false
$app.DisplayAlerts = 0
$doc = $null
try {
    $doc = $app.Documents.Open($docx, $false, $false)
    $doc.Repaginate()
    $doc.Save()
    if (Test-Path -LiteralPath $pdf) {
        Remove-Item -LiteralPath $pdf -Force
    }
    $doc.ExportAsFixedFormat($pdf, 17)
    [pscustomobject]@{
        Pages = $doc.ComputeStatistics(2)
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
