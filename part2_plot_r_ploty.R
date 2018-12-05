# make plotly scatterplot
# register: https://plot.ly/r/
library(plotly)
library(stringr)

# set wd
setwd('/Users/kgedney/Documents/georgetown/anly503/project')

# load data
df <- read.csv('data/infra_and_fdi_share_gdp.csv')

# subset on 2016
df <- df[(df$date == 2016),]


# create palette
income_levels = c("High income", "Upper middle income", "Lower middle income", "Low income")
df$income_level <- factor(df$income_level, levels = income_levels)

pal <- c("#1f77b4", "#2ca02c", "#ff7f0e", "#d62728")
pal <- setNames(pal, income_levels)

# create a scatter plot
p <- plot_ly(x = df$infra, y = df$fdi,
             type  = 'scatter',
             mode  =  'markers',
             color  = as.factor(df$income_level), 
             colors = pal,
             text   = paste0("Country: ", df$country, 
                             '<br> FDI: ', round(df$fdi,0), '%',
                             '<br> Infra: ', round(df$infra,0), '%',
                             '<br> GDP:', round(df$gdp / 1e6, 1), "M"), 
             size  = df$gdp)  %>%
  
  layout(title = "GDP Contributions by Country <br> (2016)",
         xaxis = list(zeroline = FALSE, title='% of GDP from Infrastructure'),
         yaxis = list(zeroline = FALSE, title='% of GDP from FDI'))

p

library(htmlwidgets)
saveWidget(as_widget(p), file="infra_and_fdi.html")

