#
# Removed duplicated search strings between `Link` and `Spreadsheet` sources
#
data <- read.csv("../inputs/search-strings-with-duplicates.csv")
data_unique <- data[!duplicated(data$String), ]
n_removed <- nrow(data) - nrow(data_unique)
print(paste("Removed", n_removed, "dupulicates"))
write.csv(data_unique, file = "../inputs/search-strings.csv", row.names = FALSE)
