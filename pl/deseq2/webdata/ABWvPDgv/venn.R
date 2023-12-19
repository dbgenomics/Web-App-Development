library (VennDiagram)
jpeg (filename="/home/act/software/nickbild/webdata/venn_general/webdata/ABWvPDgv/venn/venn.jpg", width=2400, height=2400, res=300)
draw.triple.venn(area1 = 3116, area2 = 6155, area3 = 5865, n12 = 1538, n23 = 2497, n13 = 1490, n123 = 714, category=c('C long description', 'A long description', 'B long description'), fill=c('light blue', 'pink', 'skyblue') )
dev.off()
svg (filename="/home/act/software/nickbild/webdata/venn_general/webdata/ABWvPDgv/venn/venn.svg")
draw.triple.venn(area1 = 3116, area2 = 6155, area3 = 5865, n12 = 1538, n23 = 2497, n13 = 1490, n123 = 714, category=c('C long description', 'A long description', 'B long description'), fill=c('light blue', 'pink', 'skyblue') )
dev.off()

