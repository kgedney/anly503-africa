# ref: https://rstudio.github.io/leaflet/choropleths.html

# libraries
library(leaflet)
library(maps)
library(mapdata)
library(maptools)
library(rgdal)
library(sp)
library(geojsonio)
library(viridis)

# set wd
setwd('/Users/kgedney/Documents/georgetown/anly503/project/data')

# import country level data
df  <- read.csv('df_leaflet.csv', stringsAsFactors = FALSE)
df$COUNTRY <- df$country
df <- df[(df$date == 2016),]

# import Africa country map data (https://www.census.gov/geo/maps-data/data/cbf/cbf_state.html)
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

# merge with centers (lat, long) of each country
library(rgeos)
library(rworldmap)

# get world map
wmap <- getMap(resolution="high")

# get centroids into dataframe
centroids <- gCentroid(wmap, byid=TRUE)
centroids <- as.data.frame(centroids)
centroids$country <- rownames(centroids)

# rename for successful merge
centroids$country[centroids$country == 'Gambia'] <- 'Gambia, The'
centroids$country[centroids$country == 'Democratic Republic of the Congo'] <- 'Congo, Dem. Rep.'
centroids$country[centroids$country == 'Republic of the Congo'] <- "Congo, Rep."
centroids$country[centroids$country == 'Ivory Coast'] <- "Cote d'Ivoire"

# filter on countries
centroids <- centroids[centroids$country %in% df_countries,]

# merge with df (now we have long=x, lat=y)
df_map <- merge(df_map, centroids, by=c("country"), duplicateGeoms = TRUE)





###### MAPPING #######

# set up colors for chloropleth
#quantile(df$birth_rate_per_1000)
pct.bins <-c(0, 25, 30, 35, 40, 45, 100)
pct.pal <- viridis(5)
pct.pal  <- colorBin(pct.pal, bins=pct.bins)

# format labels
labels <- sprintf("Country: %s <br/>Birth Rate: %s <br/>Pop Using Internet: %s <br/>Income Level: %s", 
                 df_map$country, round(df_map$birth_rate_per_1000, 0), 
                 round(df_map$internet, 1),
                 df_map$income_level) %>% lapply(htmltools::HTML)

text_for_markers <- paste0('<strong>Country: </strong>', df_map$country,
                           '<br><strong>Birth Rate: </strong>', round(df_map$birth_rate_per_1000, 0),
                           '<br><strong>Pop Using Internet: </strong>', round(df_map$internet, 1), '%',
                           '<br><strong>Income Level: </strong>', df_map$income_level)

# format icons
internet_icons <- awesomeIcons(
  icon = 'flash',
  iconColor = 'white',
  library = 'ion',
  markerColor = 'lightgray')

# format income level circles
income_levels = c("High income", "Upper middle income", "Lower middle income", "Low income")
income_pal <- colorFactor(c("#1f77b4", "#2ca02c", "#ff7f0e", "#d62728"), domain = income_levels)

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

  addPopups(lng = 29.0003377 , lat = -25.0838838,
            popup = "South Africa: Low Birth Rate, High Internet Access, <br> Upper middle income country",
            options = popupOptions(closeButton = TRUE))  %>%
  
  addPopups(lng = 40.4897 , lat = 9.1450,
            popup = "Ethiopia: Medium Birth Rate, Low Internet Access, <br> Low income country",
            options = popupOptions(closeButton = TRUE))  %>%
  
  addPopups(lng = 5.266667 , lat = 14.883333,
            popup = "Niger: High Birth Rate, Very Low Internet Access, <br> Low income country",
            options = popupOptions(closeButton = TRUE))  %>%
  
  addCircleMarkers(lat=df_map$y, lng=df_map$x,
                  fillColor = ~income_pal(df_map$income_level),
                  radius = 5,
                  fillOpacity = 1.0,
                  stroke=TRUE,
                  color='black',
                  group = 'Country Income Level') %>%

  addAwesomeMarkers(lat=df_map$y, lng=df_map$x,
           popup=text_for_markers, group = "Internet Access (%)", 
           icon=internet_icons) %>%

  # add layers control
  addLayersControl(overlayGroups = c("Internet Access (%)", "Country Income Level"),
                 options = layersControlOptions(collapsed = FALSE))

a_map

setwd('/Users/kgedney/Documents/georgetown/anly503/project/part2_website/images')

library(htmlwidgets)
saveWidget(a_map, file="leaflet_map.html")





