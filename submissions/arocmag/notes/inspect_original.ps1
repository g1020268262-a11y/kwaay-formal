$ErrorActionPreference='Stop'
$root='D:\kwaay-formal\submissions\arocmag'
$app=New-Object -ComObject kwps.Application
$app.Visible=$false
$app.DisplayAlerts=0
try { $app.AutomationSecurity=3 } catch {}
try {
 $doc=$app.Documents.Open((Join-Path $root 'official\templates\投稿编辑模板-计算机应用研究.doc'),$false,$true)
 try {
  $info=[ordered]@{Application=$app.Name;Version=$app.Version;ReadOnly=$doc.ReadOnly;Pages=$doc.ComputeStatistics(2);Paragraphs=$doc.Paragraphs.Count;Sections=@();Styles=@();InlineShapes=@();Shapes=$doc.Shapes.Count;Fields=$doc.Fields.Count;Bookmarks=$doc.Bookmarks.Count;Comments=$doc.Comments.Count;Revisions=$doc.Revisions.Count;Footnotes=$doc.Footnotes.Count;Endnotes=$doc.Endnotes.Count;Stories=@()}
  foreach($s in $doc.Sections) { $ps=$s.PageSetup; $info.Sections+=@{Index=$s.Index;Start=$ps.SectionStart;Width=$ps.PageWidth;Height=$ps.PageHeight;Top=$ps.TopMargin;Bottom=$ps.BottomMargin;Left=$ps.LeftMargin;Right=$ps.RightMargin;Header=$ps.HeaderDistance;Footer=$ps.FooterDistance;Columns=$ps.TextColumns.Count;ColumnSpacing=$ps.TextColumns.Spacing;DifferentFirstPage=$ps.DifferentFirstPageHeaderFooter} }
  foreach($s in $doc.Styles) { if($s.NameLocal.StartsWith('@')) { $info.Styles+=@{Name=$s.NameLocal;Font=$s.Font.Name;FarEast=$s.Font.NameFarEast;Ascii=$s.Font.NameAscii;Size=$s.Font.Size;Bold=$s.Font.Bold;Italic=$s.Font.Italic;Alignment=$s.ParagraphFormat.Alignment;LineSpacing=$s.ParagraphFormat.LineSpacing;LineSpacingRule=$s.ParagraphFormat.LineSpacingRule;SpaceBefore=$s.ParagraphFormat.SpaceBefore;SpaceAfter=$s.ParagraphFormat.SpaceAfter;FirstLineIndent=$s.ParagraphFormat.FirstLineIndent;LeftIndent=$s.ParagraphFormat.LeftIndent;RightIndent=$s.ParagraphFormat.RightIndent} } }
  foreach($s in $doc.InlineShapes) { $prog=''; try{$prog=$s.OLEFormat.ProgID}catch{}; $info.InlineShapes+=@{Type=$s.Type;ProgID=$prog;Width=$s.Width;Height=$s.Height} }
  foreach($s in $doc.StoryRanges) { $details=@(); foreach($field in $s.Fields) {$details+=@{Type=$field.Type;Code=$field.Code.Text;Result=$field.Result.Text}}; $info.Stories+=@{Type=$s.StoryType;Text=$s.Text;Fields=$s.Fields.Count;FieldDetails=$details;Shapes=$s.ShapeRange.Count} }
  $info | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $root 'snapshots\F01-original-com-audit.json') -Encoding utf8
  Write-Output ('Original audited: '+$info.Pages+' pages; '+$info.Styles.Count+' custom styles; '+$info.InlineShapes.Count+' inline objects')
 } finally {$doc.Close(0)}
} finally {$app.Quit()}
