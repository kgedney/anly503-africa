

# ref: https://rstudio.github.io/leaflet/choropleths.html

# libraries
library(leaflet)
library(maps)
library(mapdata)
library(maptools)
library(rgdal)
library(sp)
library(geojsonio)

# set wd
setwd('/Users/kgedney/Documents/georgetown/anly503/project/data')

# import state level results by candidate
df  <- read.csv('df_leaflet.csv', stringsAsFactors = FALSE)
df$COUNTRY <- df$country
df <- df[(df$date == 2016),]

# import US State map data (https://www.census.gov/geo/maps-data/data/cbf/cbf_state.html)
# import Africa map data 
africa.map <- readOGR(dsn='Africa_SHP', layer='Africa', stringsAsFactors = FALSE)

# drop non Sub Saharan Africa countries
africa.map <- africa.map[!africa.map$COUNTRY %in% c("Algeria", "Libya", "Egypt", "Morocco", 
                                                    "Tunisia", "Western Sahara", "Swaziland",
                                                    "Cape Verde", "Djibouti"),]

africa.map$COUNTRY[africa.map$COUNTRY == 'Gambia'] <- 'Gambia, The'
africa.map$COUNTRY[africa.map$COUNTRY == 'Democratic Republic of Congo'] <- 'Congo, Dem. Rep.'
africa.map$COUNTRY[africa.map$COUNTRY == 'Congo-Brazzaville'] <- "Congo, Rep."
africa.map$COUNTRY[africa.map$COUNTRY == 'Cote d`Ivoire'] <- "Cote d'Ivoire"

# check overlap
map_countries <- unique(africa.map$COUNTRY)
df_countries <- unique(df$country)
setdiff(map_countries, df_countries)

# merge the data
df_map <- merge(africa.map, df, by=c("COUNTRY"), duplicateGeoms = TRUE)

# merge with state center lat and long (taken from: https://www.kaggle.com/washimahmed/usa-latlong-for-state-abbreviations)
# centers <- read.csv('statelatlong.csv', stringsAsFactors = FALSE)
# centers$NAME <- centers$City
# electionmap  <- merge(electionmap, centers, by=c("NAME"))

# merge with centers of each country
library(rgeos)
library(rworldmap)

# get world map
wmap <- getMap(resolution="high")

# get centroids
centroids <- gCentroid(wmap, byid=TRUE)
centroids <- as.data.frame(centroids)
centroids$country <- rownames(centroids)

# rename for successful merge
centroids$country[centroids$country == 'Gambia'] <- 'Gambia, The'
centroids$country[centroids$country == 'Democratic Republic of Congo'] <- 'Congo, Dem. Rep.'
centroids$country[centroids$country == 'Republic of the Congo'] <- "Congo, Rep."
centroids$country[centroids$country == 'Ivory Coast'] <- "Cote d'Ivoire"

# filter on countries
centroids <- centroids[centroids$country %in% df_countries,]

# merge with df (now we have long=x, lat=y)
df_map <- merge(df_map, centroids, by=c("country"), duplicateGeoms = TRUE)


###### MAPPING #######
# set up colors for chloropleth
#quantile(df$birth_rate_per_1000)

pct.bins <-c(0, 5, 15, 30, 35, 40, 55, 100)
pct.pal  <- c("#2166AC","#4393C3", "#D1E5F0",
              "#F4A582", "#D6604D", "#B2182B")
pct.pal  <- colorBin(pct.pal, bins=pct.bins)

# format labels
labels <- sprintf("Country: %s <br/>Birth Rate: %s", 
                 df_map$country, round(df_map$birth_rate_per_1000, 0)) %>% lapply(htmltools::HTML)

text_for_markers <- paste0("<strong>Country: </strong>",
                            df_map$country,
                         "<br><strong>% Pop with Access to Electricty: </strong>",
                          round(df_map$electricity_access, 1))

# set up plot
a_map <- leaflet(data = df_map) %>%
  
  addTiles() %>%
  addPolygons(fillColor = ~pct.pal(df_map$birth_rate_per_1000), weight = 2, opacity = 1, color = "gray",
              dashArray = "3", fillOpacity = 0.95, 
              highlight = highlightOptions(weight = 5, color = "#666",dashArray = "",
                                           fillOpacity = 1.0, bringToFront = TRUE),
              label = labels,
              labelOptions = labelOptions(style = list("font-weight" = "normal", padding = "3px 8px"),
                                          textsize = "15px",direction = "auto")) %>%
  addLegend(pal = pct.pal, 
            values = ~df_map$birth_rate_per_1000, 
            opacity = 0.7, 
            title = 'Birth Rate (per 1000)',
            position = 'bottomright') %>%
  
  # addPopups(
  #   lng = -107.2903, lat = 43.0760,
  #   popup = "WY: Largest Margin for Trump",
  #   options = popupOptions(closeButton = TRUE))  %>%
  # 
  # addPopups(
  #   lng = -77.0369, lat = 38.9072,
  #   popup = "DC: Largest Margin for Clinton",
  #   options = popupOptions(closeButton = TRUE)) %>%
  # 
addMarkers(lat=df_map$y, lng=df_map$x,
           popup=text_for_markers, group = "Electricity Access (%)") %>%
  # 
# add layers control
addLayersControl(overlayGroups = c("Electricity Access (%)"),
                 options = layersControlOptions(collapsed = FALSE))

a_map


# to do: 
# add popups
# change colorscale
# add more to markers
# fix Congo






  
setwd('/Users/kgedney/Documents/georgetown/anly503/project/')

library(htmlwidgets)
saveWidget(n_map, file="leaflet_map.html")





