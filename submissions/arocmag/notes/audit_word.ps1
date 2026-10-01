$ErrorActionPreference = 'Stop'
$root = 'D:\kwaay-formal\submissions\arocmag'
$app = New-Object -ComObject kwps.Application
$app.Visible = $false
$app.DisplayAlerts = 0
try { $app.AutomationSecurity = 3 } catch {}
try {
  foreach ($item in @(@{Id='F01';Path='official\templates\投稿编辑模板-计算机应用研究.doc'}, @{Id='F05';Path='official\forms\题目及作者变更申请书-计算机应用研究.doc'}, @{Id='F04';Path='official\forms\著作权转让承诺书及保密审查证明-计算机应用研究.dotx'})) {
    $doc = $app.Documents.Open((Join-Path $root $item.Path), $false, $true)
    try {
      $doc.Content.Text | Set-Content -LiteralPath (Join-Path $root ('snapshots\'+$item.Id+'-word-text.txt')) -Encoding utf8
      $doc.ExportAsFixedFormat((Join-Path $root ('snapshots\'+$item.Id+'-render.pdf')),17)
      if ($item.Id -eq 'F01') { $doc.SaveAs2((Join-Path $root 'snapshots\F01-audit-copy.docx'),16) }
      Write-Output ($item.Id+' opened, extracted and rendered')
    } finally { $doc.Close(0) }
  }
} finally { $app.Quit() }
