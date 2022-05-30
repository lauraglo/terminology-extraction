library(shiny)
library(dplyr)
library(tableHTML)
library(magrittr) # for the %<>% pipe
library(DT)
library(stringr)
library(tidyverse)

train <- read.delim("train.txt",header=FALSE, blank.lines.skip = FALSE,col.names = c('Word','BIO'))
train2<-train

#Cada caracter "nulo" ("") es el fin de un abstract -> introducimos un EOL
train2$Word <- replace(train$Word, train$Word  == "", "\n\n")

# Contar el Nº de abstracts 
nabs <- length(which(train2$Word == "\n\n")) + 1

# Etiquetar con el abstractID
l <- length(train2$Word)
vec <- 1:l
train2$AbstractID <- vec 

temp = 1
j = 1
for(i in train2$Word){
  train2[j, "AbstractID"] <- temp
  if(i=="\n\n"){
    temp = temp + 1
  }
  if(is.na(i)){
    break
  }
  j = j + 1
}


highlight <- '
                function getSelectionText() {
var text = "";
  if (window.getSelection) {
    text = window.getSelection().toString();
  } else if (document.selection) {
      text = document.selection.createRange().text;
  }
  return text;
}

document.onmouseup = document.onkeyup = document.onselectionchange = function() {
  var selection = getSelectionText();
  Shiny.onInputChange("mydata", selection);
};
'

coded_text <- character(0)

ui3 <- bootstrapPage(
  tags$script(highlight),
  fluidRow(
    column(8,
           tags$h1("Train file editor for terminology extraction"),
           tags$h3("Abstracts from the train file:"),
           #htmlOutput("table")
           DTOutput("table")
    ),
    column(3,
           tags$h2("File editor"),
           actionButton("code1", "Assign selected text as B-KEY and I-KEY"),
           verbatimTextOutput("selected_text"),
           verbatimTextOutput("key"),
           actionButton("download","Download train file")
    )
  )
)
train3 <- train2
p <- data.frame(AbstractID= ids, 
                Abstract = strsplit(do.call(paste, c(train3$Word, list(collapse=","))), "\n\n"), 
                Ntokens = 0, 
                NChanges = 2)

colnames(p) = c("ID","Abstract","NTokens","NChanges")

markkeys <- function(){
  cont=1
  for(i in train3$Word){
    if(train3$BIO[cont]=="B-KEY"){
      train3$Word[cont]<-paste0('<span style="background-color:yellow">',train3$Word[cont],'</span>')
    }
    if(train3$BIO[cont]=="I-KEY"){
      train3$Word[cont]<-paste0('<span style="background-color:#D6EEEE">',train3$Word[cont],'</span>')
    }
    cont = cont + 1
  }
  p <- data.frame(AbstractID= ids, 
                  Content = strsplit(do.call(paste, c(train3$Word, list(collapse=","))), "\n\n"), 
                  Ntokens =  str_count(p$Abstract, '\\s+')+1, 
                  NChanges = 2)
  colnames(p) = c("ID","Abstract","NºTokens","NºChanges")
  return(p)
}


p <- markkeys()

# REEMPLAZAR
# Buscar la key con esa palabra
train2$BIO[which(train2$Word == "Knowledge")]

server3 <- function(input, output) {
  
  #output$table <- renderUI({
    #HTML(p %>% 
      #tableHTML(escape=FALSE))
    #})
  
  output$table <- renderDataTable(p,selection = "single",rownames = FALSE,options = list(pageLength = 3), escape = FALSE)
  
  #observeEvent(input$code1, {
    #p <- markkeys()
  #})

  coded <- eventReactive(input$code1, {
    coded_text <<- c(coded_text, input$mydata)
    coded_text
  })
  
  output$selected_text <- renderPrint({
    coded()
  })
  
  keyed <- eventReactive(input$code1,{
    keyed_text <<- c(train3$BIO[which(train3$Word == input$mydata)])
    keyed_text
  })
  
  output$key <- renderPrint({
    keyed()
  })
  
}

shinyApp(ui = ui3, server = server3)
