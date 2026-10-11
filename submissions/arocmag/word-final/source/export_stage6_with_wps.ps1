$ErrorActionPreference = 'Stop'
$wordRoot = Split-Path -Parent $PSScriptRoot
$docx = Join-Path $wordRoot 'K-Waay-AROCMAG-submission-stage6.docx'
$pdf = Join-Path $wordRoot 'K-Waay-AROCMAG-submission-stage6-preview.pdf'
$app = New-Object -ComObject KWPS.Application
$app.Visible = $false
$app.DisplayAlerts = 0
$doc = $null
try {
    $doc = $app.Documents.Open($docx, $false, $true)
    $doc.Repaginate()
    if (Test-Path -LiteralPath $pdf) { Remove-Item -LiteralPath $pdf -Force }
    $doc.ExportAsFixedFormat($pdf, 17)
    $result = [pscustomobject]@{
        Renderer = 'WPS Writer via KWPS.Application; not Microsoft Word'
        Version = $app.Version
        Pages = $doc.ComputeStatistics(2)
        Paragraphs = $doc.Paragraphs.Count
        Tables = $doc.Tables.Count
        InlineShapes = $doc.InlineShapes.Count
        OMaths = $doc.OMaths.Count
        Sections = $doc.Sections.Count
        PDF = $pdf
    } | ConvertTo-Json -Depth 3
    $result | Set-Content -LiteralPath (Join-Path $wordRoot 'qa/stage6/wps-export.json') -Encoding UTF8
    $result
}
finally {
    if ($null -ne $doc) { $doc.Close($false) }
    $app.Quit()
    [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($app) | Out-Null
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
