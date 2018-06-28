
#
# Join CSVs
#

ROOT <- "./outputs/csv/"

join_csvs <- function() {
    data <- NULL
    file_names <- dir(ROOT, pattern=".csv")
    for (f in file_names) {
        print(f)
        data <- rbind(data, read.csv(paste(ROOT, f, sep = "")))
    }
    return (data)
}

data <- join_csvs()
write.csv(data, file=paste("./outputs/", "skus.csv", sep = ""))

#
# Find missing landing page numbers
#

missing_landing_pages <- function(data) {
    available_range <- 1:3939
    URLs <- sort(unique(data$landing))
    landing_page_numbers <- as.integer(gsub("https://www.mcmaster.com/#", "", URLs))
    return(unique(unlist(lapply(available_range, function(page) {
        if (!(page %in% landing_page_numbers)) {
            return(page)
        }
    }))))
}

missing_landing_pages <- missing_landing_pages(data)

write.csv(missing_landing_pages, "./outputs/missing.csv", row.names = F)
