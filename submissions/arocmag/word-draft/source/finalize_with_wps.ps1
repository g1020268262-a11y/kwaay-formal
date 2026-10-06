$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)))
$draftRoot = Join-Path $root 'submissions\arocmag\word-draft'
$docx = Join-Path $draftRoot 'manuscript\kwaay-arocmag-draft.docx'
$pdf = Join-Path $draftRoot 'manuscript\kwaay-arocmag-review.pdf'
$fig1 = Join-Path $draftRoot 'figures\figure-1.emf'
$fig2 = Join-Path $draftRoot 'figures\figure-2.emf'

$app = New-Object -ComObject KWPS.Application
$app.Visible = $false
$app.DisplayAlerts = 0
$doc = $null
try {
    $doc = $app.Documents.Open($docx, $false, $false)
    $figures = @(
        @{ Marker = '[[FIGURE_1]]'; Path = $fig1; Width = 220.0 },
        @{ Marker = '[[FIGURE_2]]'; Path = $fig2; Width = 220.0 }
    )
    foreach ($figure in $figures) {
        $range = $doc.Content.Duplicate
        $found = $range.Find.Execute($figure.Marker)
        if ($found) {
            $range.Text = ''
            $shape = $doc.InlineShapes.AddPicture($figure.Path, $false, $true, $range)
            $shape.LockAspectRatio = -1
            $shape.Width = $figure.Width
        }
    }
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
