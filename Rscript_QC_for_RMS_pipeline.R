# install.packages("openxlsx")
library(openxlsx)
# install.packages("PRROC")
library("PRROC")
############################### Variables ############################### 
args = commandArgs(trailingOnly=TRUE)
group <- as.character(args[1])
# group <- "test_new" # testing on computer
path_to_anno <- as.character(args[2])
# path_to_anno <- "/Users/lzg240/Documents/Bioinformatics/PROJECT-rRNA-RMS/scripts/helpfiles" # testing on computer
dirpath <- as.character(args[3])   # path to RMS_comb.txt.xlsx file # plots will be saved here
# dirpath <- "/Users/lzg240/Desktop/pipe_test" # testing on computer
load(file.path(path_to_anno,"RMS.anno.rRNA.Rdata"))
possites.col <- "True.2Ome.109" # chose column defining true Nm sites # could also be f.ex "True.2Ome.111

fnames <- file.path(dirpath,paste(group,"RMS_comb.txt.xlsx",sep = "_"))
datatab <- read.xlsx(fnames, startRow = 2,skipEmptyRows = T,cols = c(1:23))
colnames(datatab) <- gsub("Std.dev.","Sdev",colnames(datatab))
colnames(datatab) <- gsub("Nucl","Nucleotide",colnames(datatab))
colnames(datatab) <- gsub("RNA","Subunit",colnames(datatab))
datatab$pos <- paste(datatab$Subunit,datatab$Position,sep = "_") #this is the new ref pos
rownames(datatab) <-  datatab$pos #good idead also to make this the rownames
tabname <- paste("RMS","data",group,sep = ".")
assign(tabname, datatab)

filenam <- file.path(dirpath,paste(tabname,"Rdata",sep = ".")) # output in /home/disat/data/RMS/ : need to move to correct folder later
save(list=ls(pattern = "RMS.data"),file=filenam)
#### ROC ####
su <- as.character(c("5.8S","18S","28S"))
methpct.comb <- subset(datatab,(datatab$Subunit==su[1]|datatab$Subunit==su[2]|datatab$Subunit==su[3]),"Av.Meth%")
annotab <- subset(RMS.anno,RMS.anno$Subunit==su[1]|RMS.anno$Subunit==su[2]|RMS.anno$Subunit==su[3])

err <- sum(ifelse(annotab$pos==methpct.comb$pos,0,1))
errmessage <- ifelse(err==0,"R session finished sucessfully","Fatal error in table dimensions when producing ROC curve")
if(err==0){
tit <- group
## pdf
mypath= file.path(dirpath,paste("ROC",group,"pdf",sep = "."))
pdf(file=mypath,paper="special",pointsize=12,width=6,height=6 ,bg="white")

for(i in 1:length(methpct.comb[1,])){
  i <- 1
  t<-methpct.comb[annotab[,possites.col]==T,i]
  f<-methpct.comb[annotab[,possites.col]==F,i]
  roc<-roc.curve(scores.class0 = t, scores.class1 = f, curve=T)
  # pr<-pr.curve(scores.class0 = t, scores.class1 = f, curve=T)
  plot(roc)
  # plot(pr)  
  legend("center",legend = tit[i],bty = "n")
}
dev.off()
}
if(err!=0){print(paste("R session:",date(),".........",errmessage))}

#####################################
x.range <- c(-0.1,1.1)
colnames(datatab) <- gsub("Av.Meth%","Av.methpct",colnames(datatab)) #we dont want to grep Av.Meth% only the single ones
methtab <- datatab[datatab$Subunit==su[1]|datatab$Subunit==su[2]|datatab$Subunit==su[3],grep("Meth%",colnames(datatab))]
##############
mypath= file.path(dirpath,paste("QC.density",group,"pdf",sep = "."))
pdf(file=mypath,paper="special",pointsize=12,width=7,height=6 ,bg="white")
par(mar=c(3,3,5,9)) #c(bottom, left, top, right)

n.col <- length(colnames(methtab))
col.select <- 1:n.col
for(k in 1:((n.col/3))){
  select <- col.select[1:3]
  col.select <- col.select[4:length(col.select)]
  dtab <- methtab[,select]
  list.dtab <- list(dtab[annotab[,possites.col]==F&annotab$True.PU.put==F,],
                    dtab[annotab[,possites.col]==F,],
                    dtab[annotab[,possites.col]==T,],
                    dtab[annotab$True.PU.put==T,])
  head(list.dtab[[4]])
  leg <- c("2'O-me & pU neg sites", "2'O-me neg sites","2'Ome pos sites","pU pos sites")
  colvec <- c("gray80","gray60","red","cyan")
  ltypch <- c(1,2,3)
  ltyvec <- c(rep(ltypch,length(colnames(dtab))))
  tit <- paste("Meth% density in", group)
  
  # calculate the max/min scores to set the plot window accordingly
  max.y <- c()
  min.y <- c()
  max.x <- c()
  min.x <- c()
  i <- 1
  j <- 1

    (as.numeric(as.data.frame(list.dtab[[i]])[,j]))

  for(i in 1:length(list.dtab)){for(j in 1:3){
  max.y <- append(max.y,max(density(as.data.frame(list.dtab[[i]])[,j])$y))
  min.y <- append(min.y,min(density(as.data.frame(list.dtab[[i]])[,j])$y))
  max.x <- append(max.x,max(density(as.data.frame(list.dtab[[i]])[,j])$x))
  min.x <- append(min.x,min(density(as.data.frame(list.dtab[[i]])[,j])$x))
  }}
  ymax <- max(max.y)
  #or chose this as max as a standard for all exp..?
  # ymax <- 16 
  # plot densities
  plot(density(as.data.frame(list.dtab[[1]])[,1]),ylim=c(0,ymax),xlim=x.range,col=colvec[1], lwd=2,main = tit, cex.main=1,xpd=T,lty=ltyvec[1])#ylim=c(0,max(my))
  for(j in 1:3){
    for(i in 1:length(list.dtab)){lines(density(as.data.frame(list.dtab[[i]])[,j]),col=colvec[i],lty=ltyvec[j],lwd=2,xpd=F)} #,lty=ltyvec[i]
    legend("topright", inset=c(-0.35,0),legend =leg,col=colvec ,bty = "n",cex = 0.7,lwd=2,xpd = T)
    legend("topright", inset=c(-0.19,0.2),legend =c("library1","library2","library3"),lty = ltypch ,bty = "n",cex = 0.7,lwd=2,xpd = T)
  }}
dev.off()


print(paste("R session:",date(),"......... Rdata tab saved in location:"))
