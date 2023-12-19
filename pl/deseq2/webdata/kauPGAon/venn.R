library (VennDiagram)
jpeg (filename="/home/act/software/nickbild/webdata/venn_general/webdata/kauPGAon/venn/venn.jpg", width=2400, height=2400, res=300)
draw.pairwise.venn(area1=3116, area2=6155, cross.area=1538, category=c('C long description', 'A long description'), fill=c('light blue', 'pink') )
dev.off()
svg (filename="/home/act/software/nickbild/webdata/venn_general/webdata/kauPGAon/venn/venn.svg")
draw.pairwise.venn(area1=3116, area2=6155, cross.area=1538, category=c('C long description', 'A long description'), fill=c('light blue', 'pink') )
dev.off()

